import tkinter as tk
import pandas as pd

# Load the Excel spreadsheet using Pandas
data = pd.read_csv("CRWD Site-Station & Data Summary_TEST.csv", encoding='ISO-8859-1')

def search():
    search_term = entry.get()
    search_type = search_var.get()

    if search_type == 'Monitoring Station Name':
        result = data[data['Monitoring Station Name'] == search_term]['Info']
    elif search_type == 'Station Number':
        result = data[data['Station Number'] == int(search_term)]['Info']
    elif search_type == 'Site Name':
        result = data[data['Site Name'] == search_term]['Info']
    else:
        result = "No results found."

    result_label.config(text=result)

# Create the main window
root = tk.Tk()
root.title("Search App")

# Create and place widgets
search_var = tk.StringVar(root)
search_var.set('Monitoring Station Name')  # Default search type
search_option_menu = tk.OptionMenu(root, search_var, 'Monitoring Station Name', 'Station Number', 'Site Name')
search_option_menu.pack(pady=10)

entry = tk.Entry(root)
entry.pack(pady=5)

search_button = tk.Button(root, text="Search", command=search)
search_button.pack(pady=5)

result_label = tk.Label(root, text="", wraplength=300, justify="left")
result_label.pack(pady=10)

root.mainloop()