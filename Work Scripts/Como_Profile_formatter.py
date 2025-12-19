"""
Module name: Lake_Profile_formatter.py

Author: Jim Rudolph
Created: 2024-02-05
Last updated: 2025-12-16

Description:
    Converts raw Vu Situ CSV snapshot files from Aqua TROLL sondes into ZRXP files
    for WISKI import. The script normalizes column names, maps device serial numbers
    to station IDs, removes duplicate metadata rows, resolves duplicate columns,
    coerces and formats timestamps, applies unit conversions (barometric pressure,
    total dissolved solids), and writes station-parameter ZRXP files with WISKI-
    compliant headers.

Inputs:
    - Input directory containing raw Vu Situ CSV files.
    - Expected columns include 'Date Time', 'Device SN', and sensor parameters
      such as Temperature, pH, Conductivity, RDO Concentration, Depth, etc.

Outputs:
    - ZRXP files named as '{station}_{parameter}.zrxp' written to the specified
      output directory, each containing date-stamped values formatted for WISKI
      (#REXCHANGEProfile headers).

Assumptions:
    - 'Date Time' format is either 'MM/DD/YYYY HH:MM' or 'YYYY-MM-DD HH:MM:SS'.
    - Duplicate timestamps within the same minute are adjusted by +1 second
      to avoid WISKI import collisions.
    - Device serial numbers are mapped to station IDs via the `mapping` dictionary.

Error handling:
    - Errors are counted in `err_count` and filenames are appended to `error_files`.
    - Warning is printed when expected columns are missing; the script proceeds
      with available columns.
"""

import os
import pandas as pd

# Global error counter and error log list
global err_count
err_count = 0
error_files = []

# Mapping dictionary for column renaming
mapping = {
    'Device SN': 'Station',
    'Aqua TROLL 600 587461': '102',
    'Aqua TROLL 600 587452': '201',
    'Aqua TROLL 600 587526': '202',
    'Aqua TROLL 600 923092': '202'
}

column_order = ['Date Time', 'Station', 'pH', 'Total Dissolved Solids', 'Temperature', 'Barometric Pressure',
                  'Specific Conductivity', 'RDO Concentration', 'Actual Conductivity',
                  'Salinity', 'RDO Saturation', 'Depth']

def format_csv_dataframe(df, filename="unknown"):
    global err_count
    try:
        # drop empty rows, rename columns, apply serial number to station number mapping
        df = df.dropna(how='all')
        df = df.rename(columns=mapping).replace(mapping)

        # get rid of duplicate Date Time rows
        df = df[~df.apply(lambda row: 'Date Time' in row.values, axis=1)]

        # get rid of second Barometric Pressure and Temperature columns
        def drop_second_matching_column(df, substring):
            matches = [col for col in df.columns if substring in col]
            if len(matches) >= 2:
                df = df.drop(columns=matches[1])
            return df

        df = drop_second_matching_column(df, "Barometric")
        df = drop_second_matching_column(df, "Temperature")

        # for all columns, delete characters after "("
        df.columns = [col.split('(')[0].strip() for col in df.columns]

        # sondes either have a "/" or "-" separating month, day, and year, determine and set correct format
        if '/' in str(df['Date Time'].iloc[0]):
            date_format = '%m/%d/%Y %H:%M'
        else:
            date_format = '%Y-%m-%d %H:%M:%S'

        df['Date Time'] = pd.to_datetime(df['Date Time'], format=date_format, errors='coerce')
        df.columns = df.columns.str.strip()

        # some sonde samples are taken within the same minute, add 1 second to duplicate date time so all data are imported into WISKI
        duplicates_mask = df.duplicated(subset=['Date Time'], keep=False)
        counter = 0
        for index, row in df[duplicates_mask].iterrows():
            if counter % 2 != 0:
                df.at[index, 'Date Time'] += pd.to_timedelta(1, unit='s')
            counter += 1

        df['Date Time'] = df['Date Time'].dt.strftime('%Y%m%d%H%M%S').astype(str)

        # add columns to df in the specified order in column_order, but only if df contains the column in column_order
        df = df[[col for col in column_order if col in df.columns]]

        missing_columns = [col for col in column_order if col not in df.columns]
        if len(missing_columns) > 0:
            print(f"Warning: the following parameter(s) for {filename} were not found and will not be imported: {missing_columns}. If these parameters are expected, check CSV file column headers.\n")

        # Convert units
        if 'Barometric Pressure' in df.columns:
            df['Barometric Pressure'] = pd.to_numeric(df['Barometric Pressure'], errors='coerce') * 0.0193368
        if 'Total Dissolved Solids' in df.columns:
            df['Total Dissolved Solids'] = pd.to_numeric(df['Total Dissolved Solids'], errors='coerce') * 1000

        df = df.sort_values(by='Date Time')

        # add "Date Time" string to each value so values are in the correct ZRXP format
        for col in df.columns:
            if col != 'Station' and col != 'Date Time':
                df[col] = df['Date Time'].astype(str) + ' ' + df[col].astype(str)

        return df

    except Exception as e:
        print(f"[ERROR] occurred in format_csv_dataframe function, file '{filename}' -  failed: {e}")
        err_count += 1
        error_files.append(filename)
        return pd.DataFrame()

def create_station_parameter_dataframes(df_processed, df_dict, filename="unknown"):
    global err_count
    try:
        # filter for each station
        for station in df_processed['Station'].unique():
            station_df = df_processed[df_processed['Station'] == station].iloc[:, 2:]

            # for each column, create dictionary key out of station number and parameter
            for col in station_df.columns:
                key = f'{station}_{col}'
                if key not in df_dict:
                    df_dict[key] = pd.DataFrame()

                # create dataframe of station/parameter data and concatenate to dataframe in the df_dict dictionary
                df_dict[key] = pd.concat([df_dict[key], station_df[[col]]], ignore_index=True)
        return df_dict
    except Exception as e:
        print(f"[ERROR] File '{filename}' - create_station_parameter_dataframes failed: {e}")
        err_count += 1
        error_files.append(filename)
        return df_dict

def save_zrxp_files(df_dict, output_dir):
    global err_count
    try:
        # iterate through dataframes in df_dict
        for key, dataframe in df_dict.items():
            dataframe = dataframe.dropna()
            output_path = os.path.join(output_dir, f"{key}.zrxp")

            # replace spaces in parameter with underscores
            parameter_name = key.split("_")[1].replace(' ', '_')

            # rename column header to proper ZRXP import format for WISKI
            dataframe = dataframe.rename(
                columns={col: f'#REXCHANGEProfile_{key.split("_")[0]}_{parameter_name}|*|RINVAL-777|*|RSTATEW6|*|'
                         for col in dataframe.columns})
            
            # save ZRXP to ZRXPV2R2 folder
            dataframe.to_csv(output_path, index=False)
            print(f"Saved {key} dataframe to {output_path}")
    except Exception as e:
        print(f"[ERROR] Error saving ZRXP files for output_dir '{output_dir}': {e}")
        err_count += 1
        error_files.append("Saving ZRXP files")

def start_script_create_csv_dataframes(input_dir, output_dir):
    global err_count
    file_count = 0
    df_dict = {}

    # iterate through input folder and process each raw sonde CSV. We usually only process and import one CSV at a time, 
    # but this script is written to allow for processing of as many CSVs as you'd like
    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            input_csv_path = os.path.join(input_dir, filename)
            try:
                # create
                df = pd.read_csv(input_csv_path, skiprows=6)
                df_processed = format_csv_dataframe(df, filename=filename)
                if not df_processed.empty:
                    df_dict = create_station_parameter_dataframes(df_processed, df_dict, filename=filename)
                    file_count += 1
            except Exception as e:
                print(f"[ERROR] Could not process file '{filename}': {e}")
                err_count += 1
                error_files.append(filename)

    save_zrxp_files(df_dict, output_dir)

    print(f"\nNumber of errors that occurred during processing: {err_count}")
    print(f"Successfully processed {file_count} file(s)")
    print(f"Successfully created {len(df_dict)} ZRXP files")
    if err_count > 0:
        print("\nFiles with errors:")
        for f in error_files:
            print(f" - {f}")

# Define directories
input_directory = '0. to process'
output_directory = 'C:/kisters/wiski/services/kiiosys/temp/import/ZRXPV2R2'

if __name__ == "__main__":
    start_script_create_csv_dataframes(input_directory, output_directory)
Lake_Sondes_Prepro.txt
Displaying Lake_Sondes_Prepro.txt.
