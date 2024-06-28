import os
import pandas as pd

df_list = {}

# Mapping dictionary for column renaming
mapping = {
    'Device SN': 'Station',
    'Aqua TROLL 600 587461': '102',
    'Aqua TROLL 600 587452': '201',
    'Aqua TROLL 600 587526': '202',
    'Aqua TROLL 600 923092': '202'
}

parameter_list = ['pH', 'Total Dissolved Solids', 'Temperature', 'Barometric Pressure',
                  'Specific Conductivity', 'RDO Concentration', 'Actual Conductivity', 'Salinity', 'RDO Saturation', 'Depth']


def read_csv(input_csv_path):
    # create dataframe from csv
    df = pd.read_csv(input_csv_path, skiprows=6)
    return df


def process_data(df):
    # Apply mapping to column headers and entire dataframe
    df = df.rename(columns=mapping).replace(mapping)
    df = df[~df.apply(lambda row: 'Date Time' in row.values, axis=1)]

    # Get rid of unnecessary text in column headers
    df.columns = [col.split('(')[0].strip() for col in df.columns]
    df['Date Time'] = pd.to_datetime(df['Date Time'], format='mixed')
    df = df.dropna()

    duplicates_mask = df.duplicated(subset=['Date Time'], keep=False)
    counter = 0

    # Iterate through each row and add one second to every other duplicate
    for index, row in df[duplicates_mask].iterrows():
        if counter % 2 != 0:
            df.at[index, 'Date Time'] += pd.to_timedelta(1, unit='s')
        counter += 1
    # Format Date Time column
    df['Date Time'] = df['Date Time'].dt.strftime('%Y%m%d%H%M%S').astype(str)

    # print(df.head(50))
    df = df.iloc[:, :21]
    df = df.drop(df.filter(like='pH mV').columns, axis=1)
    df_columns_list = df.columns.tolist()
    # create list of matches between the column headers and the parameter list
    df_columns_list = ['Station'] + list(set(df_columns_list).intersection(parameter_list))
    # convert units
    if 'Barometric Pressure' in df_columns_list:
        df['Barometric Pressure'] = pd.to_numeric(df['Barometric Pressure'], errors='coerce')
        df['Barometric Pressure'] = df['Barometric Pressure'] * 0.0193368
    if 'Total Dissolved Solids' in df_columns_list:
        df['Total Dissolved Solids'] = pd.to_numeric(df['Total Dissolved Solids'], errors='coerce')
        df['Total Dissolved Solids'] = df['Total Dissolved Solids'] * 1000
        
    df = df.sort_values(by='Date Time')
    # combine columns
    for col in df_columns_list:
        if col != 'Station':
            df[col] = df['Date Time'].astype(str) + ' ' + df[col].astype(str)

    df = df[df_columns_list]
    return df

     
def create_zrxp_dataframes(df_processed):
    # Use a dictionary for storing dataframes
    
    for station in df_processed['Station'].unique():
        station_df = df_processed[df_processed['Station'] == station]
        station_df = station_df.iloc[:, 1:]

        # Iterate through columns
        for col in station_df.columns:
            # Concatenate data to the corresponding dataframe in df_list
            key = f'{station}_{col}'
            if key not in df_list:
                df_list[key] = pd.DataFrame()
            df_list[key] = pd.concat([df_list[key], station_df[[col]]], ignore_index=True)
    
    return df_list

def save_zrxp_files(df_list, output_dir):
    for key, dataframe in df_list.items():
        # print(df_list.items())
        dataframe = dataframe.dropna()
        output_path = os.path.join(output_dir, f"{key}.zrxp")
        parameter_name = key.split("_")[1]
        parameter_name = parameter_name.replace(' ', '_') if ' ' in parameter_name else parameter_name
        dataframe = dataframe.rename(
            columns={col: f'#REXCHANGEComo_Profile_{key.split("_")[0]}_{parameter_name}|*|RINVAL-777|*|RSTATEW6|*|'
                     for col in dataframe.columns})
        dataframe.to_csv(output_path, index=False)

        print(f"Saved {key} dataframe to {output_path}")

def create_zrxp_files(input_dir, output_dir):
    file_count = 0
    created_count = 0
    err_count = 0
    
    # create list of files from input directory and iterate through each file
    for filename in os.listdir(input_dir):
        try:
            if filename.endswith(".csv"):
                input_csv_path = os.path.join(input_dir, filename)
                df = read_csv(input_csv_path)
                df_processed = process_data(df)
                df_list = create_zrxp_dataframes(df_processed)
                                    
            file_count += 1
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
            err_count += 1
    # Save dataframes in df_list to CSV files
    try:
        save_zrxp_files(df_list, output_dir)
        print(err_count)
        print(f'\nSuccessfully processed {file_count} file(s)')
        print(f'Successfully created {len(df_list)} ZRXP files')
        print(f'Could not process {err_count} file(s)\n')
    except Exception as e:
            print(f"Error saving ZRXP file: {e}")

# Define directories
input_directory = '0. to process/'
output_directory = 'C:/kisters/wiski/services/kiiosys/temp/import/ZRXPV2R2'

create_zrxp_files(input_directory, output_directory)