import pyodbc
import customtkinter as ctk
from tkinter import messagebox

    # Verbindungsdaten
server = 'sc-db-server.database.windows.net'
database = 'supplychain' # Setze den Namen deiner Datenbank hier ein
username = 'rse'
password = 'Pa$$w0rd'
    # Verbindungsstring
conn_str = (
    f'DRIVER={{ODBC Driver 18 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password}'
)

# Function to connect to the database and fetch data
def fetch_data():
    transport_id = entry_transport_id.get()  # Get the transport_id from the entry widget
    if not transport_id:
        messagebox.showerror("Input Error", "Please enter a valid Transport ID.")
        return
    try:
        # Replace the following connection details with your own
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM coolchain1 WHERE transportid = ?', (transport_id,))
        results = cursor.fetchall()
        display_results(results)
    except pyodbc.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if conn:
            conn.close()

# Function to display results in the GUI
def display_results(results):
    text_results.delete('1.0', ctk.END)  # Clear previous results
    if results:
        for row in results:
            text_results.insert(ctk.END, str(row) + "\n")
    else:
        text_results.insert(ctk.END, "No results found for Transport ID: " + entry_transport_id.get() + "\n")

# Set up the main application window with customtkinter
ctk.set_appearance_mode("Dark")  # Modes: "Dark", "Light", "System"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

root = ctk.CTk()
root.title("Database Query Tool")
root.geometry("800x600")

# Create a custom label and entry widget for Transport ID input
label_transport_id = ctk.CTkLabel(root, text="Enter Transport ID:", font=("Arial", 14))
label_transport_id.pack(pady=20)

entry_transport_id = ctk.CTkEntry(root, width=600, font=("Arial", 12))
entry_transport_id.pack(pady=10)

# Create a button to execute the query
button_execute = ctk.CTkButton(root, text="Fetch Data", command=fetch_data, width=200)
button_execute.pack(pady=20)

# Create a text widget to display query results
text_results = ctk.CTkTextbox(root, width=760, height=300, font=("Arial", 12))
text_results.pack(pady=20)

# Start the GUI event loop
root.mainloop()