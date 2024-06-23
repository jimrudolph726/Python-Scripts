import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import threading
import queue
import os
from tkcalendar import Calendar
import datetime

# Define the station map
station_map = {'Golf Course Pond': 'CRWD70',
               'Seminary Pond': 'CRWD190'}

# Function to run the script
def run_script():
    def task(q):
        try:
            # Get the selected station name
            selected_station = station_var.get()
            station_number = station_map[selected_station]

            # Construct the URL with the selected start date
            url = f"https://waterdata.capitolregionwd.org/KiWIS/KiWIS?datasource=0&service=kisters&type=queryServices&request=getWqmSampleValues&station_no={station_number}&parametertype_name=Orthophosphate%20as%20P,Total%20Phosphorus&measuringprog_name=Storm&from={start_date}&to=2023-12-31&returnfields=measuringprog_name,parametertype_name,station_name,timestamp,sample_timestamp,value,value_sign,value_quality,value_remark,unit_name,unit_symbol,method_name,sample_depth&format=csv&dateformat=yyyy-MM-dd%20HH:mm:ss&csvdiv=,&maxquality=120&orderby=timestamp"

            # Read the CSV file from the URL into a pandas DataFrame
            df = pd.read_csv(url)
            
            # Save the DataFrame as a CSV file in the same directory as the script
            script_directory = os.path.dirname(os.path.abspath(__file__))
            csv_file_path = os.path.join(script_directory, 'data.csv')
            df.to_csv(csv_file_path, index=False)
            
            parameter_list = ['Total Phosphorus', 'Orthophosphate as P']
            q.put((df, parameter_list))
        except Exception as e:
            q.put(e)

    def check_queue(q):
        if not q.empty():
            result = q.get()
            plot_data(result)
        else:
            root.after(100, check_queue, q)

    def plot_data(result):
        try:
            if isinstance(result, Exception):
                raise result
            df, parameter_list = result

            # Save the boxplots to an Excel file using xlsxwriter
            excel_file_path = 'test_boxplot.xlsx'
            with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
                workbook = writer.book
                for parameter in parameter_list:
                    # Filter the DataFrame to include only the current parameter's data
                    parameter_df = df[df['parametertype_name'] == parameter]

                    # Create a boxplot
                    plt.figure(figsize=(8, 6))
                    plt.boxplot(parameter_df['value'])
                    plt.title(f'Boxplot of {parameter}')
                    plt.ylabel(parameter)
                    plt.xlabel('Station')
                    plt.grid(True)
                    plt.tight_layout()

                    # Save the boxplot as an image
                    plot_file_path = f'{parameter}_boxplot.png'
                    plt.savefig(plot_file_path)
                    plt.close()

                    # Verify that the image was saved
                    if not os.path.exists(plot_file_path):
                        raise FileNotFoundError(f"Failed to save plot image '{plot_file_path}'")

                    # Add the boxplot image to the Excel file
                    worksheet = workbook.add_worksheet(parameter)
                    worksheet.insert_image('B2', plot_file_path)

            # Verify that the Excel file was saved
            if not os.path.exists(excel_file_path):
                raise FileNotFoundError(f"Failed to save Excel file '{excel_file_path}'")

            messagebox.showinfo("Success", f"Boxplots saved in '{excel_file_path}'")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Create a queue to communicate between the threads
    q = queue.Queue()
    # Run the data fetching task in a separate thread
    threading.Thread(target=task, args=(q,)).start()
    # Check the queue for data and plot when ready
    root.after(100, check_queue, q)

# Function to update the selected date label and store the selected date as a string
def update_selected_date():
    global start_date
    selected_date = calendar.get_date()

    # Parse the selected date string to a datetime object
    parsed_date = datetime.datetime.strptime(selected_date, "%m/%d/%y")

    # Format the datetime object to yyyy-mm-dd format and convert it to string
    start_date = str(parsed_date.strftime("%Y-%m-%d"))
    
    selected_date_label.config(text=f"Currently selected date: {start_date}")

# Create the main Tkinter window
root = tk.Tk()
root.title("Station Selector")

# Add a label for the dropdown menu
label = tk.Label(root, text="Select Station:")
label.pack(pady=10)

# Create a Tkinter variable and a dropdown menu
station_var = tk.StringVar()
station_dropdown = ttk.Combobox(root, textvariable=station_var)
station_dropdown['values'] = list(station_map.keys())
station_dropdown.pack(pady=10)

# Add a calendar widget
calendar = Calendar(root, selectmode='day', year=2024, month=5, day=24)
calendar.pack(pady=10)

# Add a button to update the selected date label and store the selected date
update_date_button = tk.Button(root, text="Update Selected Date", command=update_selected_date)
update_date_button.pack(pady=10)

# Label to display currently selected date
selected_date_label = tk.Label(root, text="Currently selected date: ")
selected_date_label.pack(pady=10)

# Add a button to run the script
run_button = tk.Button(root, text="Run", command=run_script)
run_button.pack(pady=20)

# Print the current working directory for debugging purposes
print("Current working directory:", os.getcwd())

# Run the Tkinter event loop
root.mainloop()
