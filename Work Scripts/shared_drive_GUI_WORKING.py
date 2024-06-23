import tkinter as tk
from tkinter import filedialog
import os
import webbrowser

def open_file(file_path):
    try:
        # Use the Windows file explorer to open directories
        if os.path.isdir(file_path):
            os.startfile(file_path)
        else:
            webbrowser.open(f'"{file_path}"')
    except Exception as e:
        print("Error opening file:", e)

def search_files():
    search_query = entry_search.get()
    results.delete(1.0, tk.END)

    if not search_query:
        results.insert(tk.END, "Please enter a search query.")
        return

    search_directory = filedialog.askdirectory(title="Select Shared Drive Directory")
    if not search_directory:
        results.insert(tk.END, "No directory selected.")
        return

    search_results = []

    for root, dirs, files in os.walk(search_directory):
        for file in files:
            if search_query.lower() in file.lower():
                file_path = os.path.join(root, file)  # Use os.path.join() to ensure backslashes on Windows
                search_results.append(file_path)

    if search_results:
        results.insert(tk.END, "Search Results:\n")
        for result in search_results:
            link = tk.Label(results, text=result, fg="blue", cursor="hand2")
            link.pack()
            link.bind("<Button-1>", lambda event, path=result: open_file(path))
    else:
        results.insert(tk.END, "No matching files found.")

# Create the main application window
app = tk.Tk()
app.title("Shared Drive Search")

# Create and place widgets
label_search = tk.Label(app, text="Enter search query:")
label_search.pack(pady=10)

entry_search = tk.Entry(app)
entry_search.pack()

btn_search = tk.Button(app, text="Search", command=search_files)
btn_search.pack(pady=10)

results = tk.Text(app, wrap=tk.WORD)
results.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Start the application event loop
app.mainloop()
