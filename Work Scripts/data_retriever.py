import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import threading
import queue
import os
from tkcalendar import Calendar
import datetime
from scipy.stats import ttest_ind
from maps import *

# Function to run the script
def retrieve_data():
    
    def task(q):    
        try:
            parameters = get_selected()
            mapped_parameters = []
            stations = []
            dfs= []
            
            for parameter in parameters:
                parameter = parameter_map[parameter]
                mapped_parameters.append(parameter)

            url_parameters = ','.join([p for p in mapped_parameters if p])

            if len(station_var1.get()) > 0:
                selected_station1 = station_var1.get()
                stations.append(selected_station1)
            if len(station_var2.get()) > 0:
                selected_station2 = station_var2.get()
                stations.append(selected_station2)
            
            for station in stations:
                # Choose measuring program based on selected station
                if "Lake" in station:
                    measuring_program = "Lake"
                else:
                    measuring_program = "Storm"

                station_number = station_map[station]
                
                # get start date
                start_date = calendar1.get_date()
                # Parse the selected date string to a datetime object
                start_date = datetime.datetime.strptime(start_date, "%m/%d/%y")
                # Format the datetime object to yyyy-mm-dd format
                start_date_string = str(start_date.strftime("%Y-%m-%d"))
                today = datetime.date.today()
                if start_date.date() >= today:
                    messagebox.showwarning("Invalid Date", "Please choose an earlier start date")
                    q.put(None)
                    return

                # get end date
                end_date = calendar2.get_date()
                # Parse the selected date string to a datetime object
                end_date = datetime.datetime.strptime(end_date, "%m/%d/%y")
                # Format the datetime object to yyyy-mm-dd format
                end_date_string = str(end_date.strftime("%Y-%m-%d"))
                today = datetime.date.today()
                if end_date.date() <= start_date.date():
                    messagebox.showwarning("Invalid Date", "Please choose a later end date")
                    q.put(None)
                    return
                
                # URL of the CSV file
                url = f"https://waterdata.capitolregionwd.org/KiWIS/KiWIS?datasource=0&service=kisters&type=queryServices&request=getWqmSampleValues&station_no={station_number}&parametertype_name={url_parameters}&measuringprog_name={measuring_program}&from={start_date_string}&to={end_date_string}&returnfields=measuringprog_name,parametertype_name,station_name,timestamp,sample_timestamp,value,value_sign,value_quality,value_remark,unit_name,unit_symbol,method_name,sample_depth&format=csv&dateformat=yyyy-MM-dd%20HH:mm:ss&csvdiv=,&maxquality=120&orderby=timestamp"

                # Read the CSV file from the URL into a pandas DataFrame
                df = pd.read_csv(url)
                script_directory = os.path.dirname(os.path.abspath(__file__))
                csv_directory = os.path.join(script_directory, 'csvs')
                os.makedirs(csv_directory, exist_ok=True)
                csv_file_path = os.path.join(csv_directory, f'{df["station_name"][0]}.csv')
                df.to_csv(csv_file_path, index=False)

                # Make a list of dataframes
                dfs.append(df)
            
            q.put((dfs, csv_directory))
            
        except Exception as e:    
            q.put(e)
            
    def check_queue(q):
        if not q.empty():
            result = q.get()
            
            if isinstance(result, Exception):
                messagebox.showerror("Error", str(result))
            elif result is not None:
                dfs, csv_directory = result
                
                generate_report(dfs, csv_directory)
        else:
            root.after(100, check_queue, q)

    # Create a queue to communicate between the threads
    q = queue.Queue()
    # Run the data fetching task in a separate thread
    threading.Thread(target=task, args=(q,)).start()
    # Check the queue for data and plot when ready
    root.after(100, check_queue, q)

# Function to concatenate CSV files and create box plots with t-test results
def generate_report(dfs,csv_directory):
    
    try:
        # execute following code if user chose more than one station
        if len(dfs) > 1:
            
            # create a dataframe for each station
            df1 = dfs[0][['parametertype_name', 'station_name', 'timestamp', 'value']]
            df2 = dfs[1][['parametertype_name', 'station_name', 'timestamp', 'value']]

            # Create an Excel writer object
            excel_file_path = os.path.join(csv_directory, f'{df1["station_name"].iloc[0]}-{df2["station_name"].iloc[0]} Analysis Summary.xlsx')
            with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
                workbook = writer.book

                # Add a single worksheet for all boxplots
                boxplot_worksheet = workbook.add_worksheet('Boxplots')
                ttest_worksheet = workbook.add_worksheet('Stats')

                # Variables to keep track of image and stats positions
                row = 2
                col = 2
                stats_row = 2

                for parameter in df1['parametertype_name'].unique():
                    df1_data = df1[df1['parametertype_name'] == parameter]
                    df2_data = df2[df2['parametertype_name'] == parameter]

                    # Perform a t-test
                    t_stat, p_value = ttest_ind(df1_data['value'], df2_data['value'], equal_var=False)

                    # Create a box plot
                    plt.figure(figsize=(10, 6))
                    plt.boxplot([df1_data['value'], df2_data['value']], labels=[df1_data['station_name'].iloc[0], df2_data['station_name'].iloc[0]])
                    plt.title(f'Boxplot of {parameter}')
                    plt.ylabel('Value')
                    plt.xlabel('Station')
                    plt.grid(True)

                    # Save the plot as an image
                    plot_file_path = os.path.join(csv_directory, f'{parameter}_boxplot.png')
                    plt.savefig(plot_file_path)
                    plt.close()

                    # Insert the box plot image into the worksheet
                    boxplot_worksheet.insert_image(row, col, plot_file_path)

                    # Write t-test results to the worksheet
                    ttest_worksheet.write(f'B{stats_row}', f'T-test results for {parameter}:')
                    ttest_worksheet.write(f'B{stats_row + 1}', f'T-statistic: {t_stat}')
                    ttest_worksheet.write(f'B{stats_row + 2}', f'P-value: {p_value}')

                    # Increment rows to prevent overlap
                    row += 30
                    stats_row += 4

        # execute following code if user chose one station
        else:
            df = dfs[0]
            col = 2
            df = df[df['station_name'] == df['station_name'].unique()[0]]
            df = df[['parametertype_name', 'station_name', 'timestamp', 'value']]

            # Create an Excel writer object
            excel_file_path = os.path.join(csv_directory, f'{df["station_name"].iloc[0]} boxplots.xlsx')
            with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
                workbook = writer.book

                # Add a single worksheet for all boxplots
                boxplot_worksheet = workbook.add_worksheet('Boxplots')

                # Variable to keep track of image positions
                row = 2

                for parameter in df['parametertype_name'].unique():
                    df1_data = df[df['parametertype_name'] == parameter]

                    # Create a box plot
                    plt.figure(figsize=(10, 6))
                    plt.boxplot([df1_data['value']], labels=[df1_data['station_name'].iloc[0]])
                    plt.title(f'Boxplot of {parameter}')
                    plt.ylabel('Value')
                    plt.xlabel('Station')
                    plt.grid(True)

                    # Save the plot as an image
                    plot_file_path = os.path.join(csv_directory, f'{parameter}_boxplot.png')
                    plt.savefig(plot_file_path)
                    plt.close()

                    # Insert the box plot image into the worksheet
                    boxplot_worksheet.insert_image(row, col, plot_file_path)

                    # Increment rows to prevent overlap
                    row += 30

        messagebox.showinfo("Success", f"Data analysis summary saved in: '{excel_file_path}'")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main Tkinter window
root = tk.Tk()

# Lift the window to the top
root.lift()

# Set the window to always stay on top
root.attributes("-topmost", True)
def center_window(window, width, height):
  # Get screen width and height
  screen_width = window.winfo_screenwidth()
  screen_height = window.winfo_screenheight()

  # Calculate center coordinates
  x = (screen_width - width) // 2
  y = (screen_height - height) // 2

  # Set window geometry (widthxheight+Xoffset+Yoffset)
  window.geometry(f"{width}x{height}+{x}+{y}")

# Set window size (replace with your desired dimensions)
window_width = 400
window_height = 300

# Center the window
center_window(root, window_width, window_height)

root.title("Data Analysis Summary Generator")

# Set the size of the window
root.geometry("400x850")

# Add a label for the dropdown menu
label = tk.Label(root, text="Select Stations:", font=("Arial",16))
label.pack()

# Create a Tkinter variable and a dropdown menu
station_var1 = tk.StringVar()
station_dropdown = ttk.Combobox(root, textvariable=station_var1, width=40)
station_dropdown['values'] = list(station_map.keys())
station_dropdown.pack()

# Create a Tkinter variable and a dropdown menu
station_var2 = tk.StringVar()
station_dropdown = ttk.Combobox(root, textvariable=station_var2, width=40)
station_dropdown['values'] = list(station_map.keys())
station_dropdown.pack()

# Add a label for the calendar
calendar_label = tk.Label(root, text="Select a Start Date:", font=("Arial",16))
calendar_label.pack()

# Add the calendar widget
calendar1 = Calendar(root, selectmode="day", year=2023, month=1, day=1, date_pattern='mm/dd/yy')
calendar1.pack()

# Add a label for the calendar
calendar_label = tk.Label(root, text="Select an End Date:", font=("Arial",16))
calendar_label.pack()

# Add the calendar widget
calendar2 = Calendar(root, selectmode="day", year=2023, month=1, day=1, date_pattern='mm/dd/yy')
calendar2.pack()

# Add a label for the checkboxes
label = tk.Label(root, text="Select Parameters:", font=("Arial",16))
label.pack()

# Define list items
parameters = ["Total Phosphorus", "Dissolved Phosphorus", "Orthophosphate as P", "Total Suspended Solids", "Cadmium", "Calcium", "Chloride"]

# Create the listbox with multiple selection mode
listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, font=("Arial", 12))
listbox.pack()

# Add list items to the listbox
for parameter in parameters:
    listbox.insert(tk.END, parameter)

# Function to get selected items
def get_selected():
  selected_indices = listbox.curselection()
  parameters = [listbox.get(index) for index in selected_indices]
  return parameters

# Add a button to run the script
run_button = ttk.Button(root, text="Generate Data Analysis Summary", command=retrieve_data)
run_button.pack(pady=30)

# Start the Tkinter event loop
root.mainloop()