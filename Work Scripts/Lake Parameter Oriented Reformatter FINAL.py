"""
Module name: lake_wq_processor.py

Author: Jim Rudolph
Created: 2024-06-28
Last updated: 2025-12-10

Description:
    Processes raw lake water quality CSV files into WISKI-compatible CSVs. 
    The script unpivots wide-format data into parameter-oriented long format, validates column headers, 
    converts depth units, generates sample numbers, pulls info from `parameters.csv` (MDL, RL, units, methods),
    and outputs processed CSV files for import into WISKI.

Inputs:
    - Input folder containing raw lake water quality CSV files with expected columns
      defined in `lake_columns.py` (lists: `all_raw_csv_columns`, `param_columns`, `other_columns`).
    - `parameters.csv` file providing parameter metadata and date ranges for MDL, RL,
      units, and method names.

Outputs:
    - Two processed CSV files per input file:
        1. `{filename}_processed.csv` (includes sample numbers)
        2. `{filename}_no_sample_numbers_processed.csv` (sample numbers removed)
      Saved in the specified output folder.

Error Handling:
    - Prints warnings for unexpected columns and exits if headers do not match.
    - Logs errors during melting (unpivoting), metadata matching, or row processing.
    - Continues processing other files when possible.
"""

import os
import pandas as pd
import numpy as np
from lake_columns import *
from tqdm import tqdm

try:
    # Load parameters CSV as the single source of truth
    parameters_df = pd.read_csv("parameters.csv", encoding='latin-1')
    parameters_df['start_date'] = pd.to_datetime(parameters_df['start_date'], errors='coerce')
    parameters_df['end_date'] = pd.to_datetime(parameters_df['end_date'], errors='coerce')
    parameters_df['end_date'] = parameters_df['end_date'].fillna(pd.Timestamp('2100-01-01'))
except Exception as e:
    print(f"Error loading parameters.csv: {e}")

try:
    def process_csv(input_folder, output_folder):
        filecount = 0

        for filename in os.listdir(input_folder):
            if filename.endswith(".csv"):
                input_filepath = os.path.join(input_folder, filename)
                df = pd.read_csv(input_filepath, encoding='latin-1')

                for column in list(df.columns):
                    if column not in all_raw_csv_columns:
                        print(f"Unexpected column found in {filename}: {column}\n")
                        print(f"Expected columns: {all_raw_csv_columns}\n")
                        print(f"Actual columns: {df.columns}\n")
                        print(f"Please edit the column headers of the raw csv file to match the expected columns above")
                        # Exit the script if the column headers are not as expected
                        exit(1)

                post_rows = melt_dataframe(df, filename, output_folder)
                filecount += 1

                print(f"Successfully processed {filename}")
                print(f"Total rows before processing: {df.shape[0]}")
                print(f"Total rows after processing: {post_rows}")

        print(f"All processed data saved to: {os.path.abspath(output_folder)}")
        print(f"Total files processed: {filecount}")

except Exception as e:
    print(f"Error creating dataframe from csv file, check the process_csv function: {e}")

try:
    def melt_dataframe(df, filename, output_folder):

        df['Sample depth'] = (df['Depth-m'] * 3.281).round(2)
        # Generate sample numbers
        sample_number = 0
        for idx, row in df.iterrows():
            if row['Depth-m'] in [0, 0.5, 0.6]:
                sample_number = 1
            else:
                sample_number += 1
            df.at[idx, 'Sample number'] = sample_number

        try:
            # unpivot the raw, sample oriented "wide data" to parameter oriented "long data"
            combined_df = pd.melt(
            df,
            id_vars=other_columns,
            value_vars=param_columns,
            var_name="Parameter type",
            value_name="Parameter value"
            )
        except Exception as e:
            print(f"Error unpivoting data {filename}: {e}")
            return 0

        combined_df.rename(columns={'SITE':'Sampling location', 'DATE':'DateTime'}, inplace=True)

        # create all columns necessary for WISKI
        combined_df['MDL'] = ''
        combined_df['RL'] = ''
        combined_df['Parameter status'] = ''
        combined_df['Parameter method short name'] = ''
        combined_df['Parameter unit shortname'] = ''
        combined_df['Measuring program shortname'] = 'Lake'
        
        # Generate sample and station identifiers
        combined_df['DateTime'] = pd.to_datetime(combined_df['DateTime'], errors='coerce', format="%m/%d/%Y")
        combined_df['Year'] = combined_df['DateTime'].dt.year.astype(str)
        combined_df['Month'] = combined_df['DateTime'].dt.month.astype(str).str.zfill(2)
        combined_df['Day'] = combined_df['DateTime'].dt.day.astype(str).str.zfill(2)

        year = combined_df['Year']
        month = combined_df['Month']
        day = combined_df['Day']

        reformatted_lakename_rmb = {'COMO': 'Como', 'CROSBY': 'Cros', 'Little Crosby': 'Lcros', 'LOEB': 'Loeb', 'MCCARRON': 'McCar'}
        combined_df['Reformatted LAKENAME'] = combined_df['LAKENAME'].map(reformatted_lakename_rmb)
        combined_df['Sampling number'] = year + month + day + combined_df['Reformatted LAKENAME'].astype(str) + combined_df['Sampling location'].astype(str)
        combined_df['Station number'] = combined_df['LAKENAME'].astype(str) + combined_df['Sampling location'].astype(str)
        combined_df['Station number'] = np.where(combined_df['Station number'].str.contains('Little'), 'CRWD50', combined_df['Station number'])
        combined_df['Station number'] = combined_df['Station number'].replace('MCCARRON101', 'MCCARRONS101')
    
        try:
            for i, row in tqdm(
                combined_df.iterrows(),
                total=combined_df.shape[0],
                desc=f"Processing rows in {filename}",
                unit="row"
            ):
                try:
                    match = parameters_df[
                        (parameters_df['start_date'] <= row['DateTime']) &
                        (parameters_df['end_date'] >= row['DateTime']) &
                        (parameters_df['Parameter type'] == row['Parameter type'])
                    ]

                    if not match.empty:
                        combined_df.at[i,'MDL'] = match['MDL'].iloc[0]
                        combined_df.at[i,'RL'] = match['RL'].iloc[0]
                        combined_df.at[i,'Parameter unit shortname'] = match['Parameter unit shortname'].iloc[0]
                        combined_df.at[i,'Parameter method short name'] = match['Parameter method short name'].iloc[0]
                        combined_df.at[i,'Parameter type'] = match['type'].iloc[0]
                except Exception as e:
                    print(f"Error matching parameter info for row {row}: {e}")
                    return 0

        except Exception as e:
            print(f"Error processing row {row}: {e}")
            return 0

        # Clean up
        combined_df['Parameter value'] = combined_df['Parameter value'].replace({'Y': '1', 'N': '0'})         
        combined_df['Sample id'] = combined_df['Sample number']
        combined_df['Sample datetime'] = combined_df['DateTime']
        combined_df['Sample replicate flag'] = '0'
        combined_df.drop(columns=['LAKENAME', 'Reformatted LAKENAME'], inplace=True)
        combined_df = combined_df[column_order]
        combined_df.dropna(subset=['Parameter value'], inplace=True)

        # Duplicate without sample numbers
        combined_df_no_sample_numbers = combined_df.copy()
        combined_df_no_sample_numbers['Sample number'] = ''

        # Save outputs
        base_filename = os.path.splitext(filename)[0]
        combined_df.to_csv(os.path.join(output_folder, f"{base_filename}_processed.csv"), index=False)
        combined_df_no_sample_numbers.to_csv(os.path.join(output_folder, f"{base_filename}_no_sample_numbers_processed.csv"), index=False)

        return combined_df.shape[0]
    
except Exception as e:
    print(f"Error while processing data, check the melt_dataframe function: {e}")

if __name__ == "__main__":
    input_folder = "input/"
    output_folder = "output/"
    process_csv(input_folder, output_folder)
New_Lake_Import.txt
Displaying New_Lake_Import.txt.
