r"""
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
    - Note: WISKI does not allow for the import of processed lake CSVs with sample numbers immediately, so 
      data with sample numbers removed have to be imported first, then the CSV with sample numbers can be imported.
      See Python SOP spreadsheet for details here: 
      W:\07 Programs\Monitoring & Data Acquisition\0 WISKI\Script and Process Development\Python Script and Environment Metadata.xlsx

ERROR Handling:
    - Prints warnings for unexpected columns and exits if headers do not match.
    - Logs ERRORs during melting (unpivoting), metadata matching, or row processing.
    - Continues processing other files when possible.
    - Functions wrapped in try/except blocks to allow for narrowing down of ERRORs.
"""

import os
import pandas as pd
import numpy as np
from lake_columns import (
    all_raw_csv_columns, 
    param_columns, 
    other_columns, 
    column_order
    )

filecount = 0
input_folder = "input/"
output_folder = "output/"

def import_parameters_csv()-> pd.DataFrame:
    try:
        # Load parameters CSV as the single source of truth
        parameters_df = pd.read_csv("parameters.csv", encoding='latin-1')
        parameters_df['start_date'] = pd.to_datetime(parameters_df['start_date'], errors='coerce')
        parameters_df['end_date'] = pd.to_datetime(parameters_df['end_date'], errors='coerce')
        parameters_df['end_date'] = parameters_df['end_date'].fillna(pd.Timestamp('2100-01-01'))
    except Exception as e:
        print(f"ERROR importing parameters.csv: {e}")
    return parameters_df

def import_and_check_raw_lake_data_csv(input_folder: str, 
                                       filename: str, 
                                       all_raw_csv_columns: list)-> pd.DataFrame:
    if not filename.endswith(".csv"):
        raise ValueError(f"Not a CSV file: {filename}")

    input_filepath = os.path.join(input_folder, filename)

    try:
        df = pd.read_csv(input_filepath, encoding="latin-1")
    except Exception as e:
        raise RuntimeError(f"ERROR: Failed to read CSV: {filename}") from e

    # Validate columns
    unexpected_columns = set(df.columns) - set(all_raw_csv_columns)
    if unexpected_columns:
        raise ValueError(
            f"The following columns were unexpected or misnamed in {filename}: {unexpected_columns}\n\n"
            f"Expected columns: {all_raw_csv_columns}\n\n"
            f"Actual columns in raw CSV: {list(df.columns)}\n\n"
            f"Please edit columns in raw CSV to match expected columns listed above."
        )

    return df

def unpivot_data(df: pd.DataFrame, 
                 column_order: list, 
                 parameters_df: pd.DataFrame)-> pd.DataFrame:
    
    # make a Sample depth column in feet from meters
    df['Sample depth'] = (df['Depth-m'] * 3.281).round(2)

    # Generate sample numbers. To account for winter sampling, label the sample numbers of any samples with 
    # depths of 0.5 or 0.6 as 1
    sample_number = 0 
    for idx, row in df.iterrows(): 
        if row['Depth-m'] in [0, 0.5, 0.6]: 
            sample_number = 1 
        else:
            sample_number += 1 
        df.at[idx, 'Sample number'] = sample_number

    try:
        # unpivot the raw, sample oriented "wide data" to parameter oriented "long data"
        processed_df = pd.melt(
        df,
        id_vars=other_columns,
        value_vars=param_columns,
        var_name="Parameter type",
        value_name="Parameter value"
        )
    except Exception as e:
        print(f"ERROR unpivoting data {filename}: {e}")
        return 0

    processed_df.rename(columns={'SITE':'Sampling location', 'DATE':'DateTime'}, inplace=True)

    try:
        # create all columns necessary for WISKI
        processed_df['MDL'] = ''
        processed_df['RL'] = ''
        processed_df['Parameter status'] = ''
        processed_df['Parameter method short name'] = ''
        processed_df['Parameter unit shortname'] = ''
        processed_df['Measuring program shortname'] = 'Lake'
        
        # Generate sample and station identifiers
        processed_df['DateTime'] = pd.to_datetime(processed_df['DateTime'], errors='coerce', format="%m/%d/%Y")
        processed_df['Year'] = processed_df['DateTime'].dt.year.astype(str)
        processed_df['Month'] = processed_df['DateTime'].dt.month.astype(str).str.zfill(2)
        processed_df['Day'] = processed_df['DateTime'].dt.day.astype(str).str.zfill(2)

        year = processed_df['Year']
        month = processed_df['Month']
        day = processed_df['Day']

        reformatted_lakename_rmb = {'COMO': 'Como', 'CROSBY': 'Cros', 'Little Crosby': 'Lcros', 'LOEB': 'Loeb', 'MCCARRON': 'McCar'}
        processed_df['Reformatted LAKENAME'] = processed_df['LAKENAME'].map(reformatted_lakename_rmb)
        processed_df['Sampling number'] = year + month + day + processed_df['Reformatted LAKENAME'].astype(str) + processed_df['Sampling location'].astype(str)
        processed_df['Station number'] = processed_df['LAKENAME'].astype(str) + processed_df['Sampling location'].astype(str)
        processed_df['Station number'] = np.where(processed_df['Station number'].str.contains('Little'), 'CRWD50', processed_df['Station number'])
        processed_df['Station number'] = processed_df['Station number'].replace('MCCARRON101', 'MCCARRONS101')
    except Exception as e:
        print(f"ERROR creating rows for processed CSV")

    try:
        total = len(processed_df)
        for idx, row in processed_df.iterrows():
            if idx % 500 == 0 or idx == total:
                print(f"Processed {idx}/{total} rows ({idx/total:.1%})")

            # for each row in the raw data, try to find a match on start date, end date, and parameter type in the parameters CSV.
            # if a match is found, grab the MDL, RL, Parameter unit shortname, Parameter method short name, and Parameter type
            # and insert in the row that is currently being analyzed
            try:
                match = parameters_df[
                    (parameters_df['start_date'] <= row['DateTime']) &
                    (parameters_df['end_date'] >= row['DateTime']) &
                    (parameters_df['Parameter type'] == row['Parameter type'])
                ]

                if not match.empty:
                    processed_df.at[idx,'MDL'] = match['MDL'].iloc[0]
                    processed_df.at[idx,'RL'] = match['RL'].iloc[0]
                    processed_df.at[idx,'Parameter unit shortname'] = match['Parameter unit shortname'].iloc[0]
                    processed_df.at[idx,'Parameter method short name'] = match['Parameter method short name'].iloc[0]
                    processed_df.at[idx,'Parameter type'] = match['type'].iloc[0]
                else:
                    print(f"\nNo matching parameter info found for "
                            f"Parameter: {row['Parameter type']} "
                            f"Date: {row['DateTime']}\n ")
                    # break out of for loop and skip to next file if no match is found
                    break
                    
            except Exception as e:
                print(f"ERROR matching parameter info for row {row}: {e}")
                return 0

    except Exception as e:
        print(f"ERROR processing row {row}: {e}")
        return 0

    # Clean up
    processed_df['Parameter value'] = processed_df['Parameter value'].replace({'Y': '1', 'N': '0'})         
    processed_df['Sample id'] = processed_df['Sample number']
    processed_df['Sample datetime'] = processed_df['DateTime']
    processed_df['Sample replicate flag'] = '0'
    processed_df.drop(columns=['LAKENAME', 'Reformatted LAKENAME'], inplace=True)
    processed_df = processed_df[column_order]
    processed_df.dropna(subset=['Parameter value'], inplace=True)

    return processed_df

def save_processed_csv(processed_df: pd.DataFrame, 
                       post_rows: int)-> int:
    try:
        # Duplicate without sample numbers
        processed_df_no_sample_numbers = processed_df.copy()
        processed_df_no_sample_numbers['Sample number'] = ''

        # Save outputs
        base_filename = os.path.splitext(filename)[0]
        processed_df.to_csv(os.path.join(output_folder, f"{base_filename}_processed.csv"), index=False)
        processed_df_no_sample_numbers.to_csv(os.path.join(output_folder, f"{base_filename}_no_sample_numbers_processed.csv"), index=False)

        print(f"\nSuccessfully processed {filename}")
        print(f"Total rows before processing: {df.shape[0]}")
        print(f"Total rows after processing: {post_rows}\n")

        print(f"All processed data saved to: {os.path.abspath(output_folder)}")

    except Exception as e:
        print(f"ERROR while saving CSV: {e}")

    return processed_df.shape[0]

if __name__ == "__main__":
    
    # iterate through every file in the input folder and call functions
    for filename in os.listdir(input_folder):
        try:
            parameters_df: pd.DataFrame = import_parameters_csv()
            df: pd.DataFrame = import_and_check_raw_lake_data_csv(input_folder=input_folder, 
                                                                 filename=filename, 
                                                                 all_raw_csv_columns=all_raw_csv_columns)
            processed_df: pd.DataFrame = unpivot_data(df=df, 
                                                      column_order=column_order, 
                                                      parameters_df=parameters_df)
            post_rows = processed_df.shape[0]
            save_processed_csv(processed_df, post_rows)
        except Exception as e:
            print(f"ERROR processing {filename}: {e}")
            continue

        filecount += 1
    print(f"Total files processed: {filecount}")
