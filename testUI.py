import sqlite3
import tkinter as tk
from tkinter import messagebox

# Function to connect to the database and fetch data
def fetch_data():
    try:
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()
        query = entry_query.get()
        cursor.execute(query)
        results = cursor.fetchall()
        display_results(results)
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if conn:
            conn.close()

# Function to display results in the GUI
def display_results(results):
    text_results.delete('1.0', tk.END)  # Clear previous results
    for row in results:
        text_results.insert(tk.END, str(row) + "\n")

# Set up the main application window
root = tk.Tk()
root.title("Database Query Tool")

# Create a label and entry widget for query input
label_query = tk.Label(root, text="Enter SQL Query:")
label_query.pack(pady=10)

entry_query = tk.Entry(root, width=50)
entry_query.pack(pady=5)

# Create a button to execute the query
button_execute = tk.Button(root, text="Execute Query", command=fetch_data)
button_execute.pack(pady=10)

# Create a text widget to display query results
text_results = tk.Text(root, width=80, height=20)
text_results.pack(pady=10)

# Start the GUI event loop
root.mainloop()