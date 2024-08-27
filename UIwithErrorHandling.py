import pyodbc
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta

# Connection details
server = 'sc-db-server.database.windows.net'
database = 'supplychain'
username = 'rse'
password = 'Pa$$w0rd'

conn_str = (
    f'DRIVER={{ODBC Driver 18 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password}'
)

# Function to connect to the database and fetch data based on transport_id
def fetch_data():
    transport_id = entry_transport_id.get()  # Get the transport_id from the entry widget
    if not transport_id:
        messagebox.showerror("Fehler", "Bitte eine valide Transport ID eingeben.")
        return

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute('SELECT transportstation, category, direction, datetime FROM coolchain1 WHERE transportid = ?', (transport_id,))
        results = cursor.fetchall()
        display_results(results)
    except pyodbc.Error as e:
        messagebox.showerror("Fehler bei Datenbankzugriff. Netzwerkverbindung prüfen.", str(e))
    finally:
        if conn:
            conn.close()

# Function to display results in the GUI with time difference and error detection
def display_results(results):
    # Clear previous results
    for widget in frame_results.winfo_children():
        widget.destroy()

    if results:
        # Create table headers
        headers = ["Ort", "Kategorie", "richtung", "Zeitstempel", "Dauer", "Warnung"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(frame_results, text=header, font=("Arial", 12, "bold"))
            label.grid(row=0, column=i, padx=10, pady=5)

        previous_datetime = None
        previous_direction = None

        # Insert results into the table
        for row_index, row in enumerate(results, start=1):
            transportstation, category, direction, current_datetime = row

            # Initialize error message
            warnung = " "

            # Zeitdifferenz berechnen
            if previous_datetime:
                time_difference = current_datetime - previous_datetime
                time_diff_str = str(time_difference)
                
                # Zeitstempel prüfen
                if time_difference.total_seconds() < 10:
                    warnung += "Implausibler Zeitstempel. "

                # Übergabezeit prüfen
                if  direction == 'in' and time_difference > timedelta(minutes=10):
                    warnung += "Übergabezeit über 10 minuten. "

                # Fahrzeit prüfen
                if  category == 'KT' and direction == 'out' and time_difference > timedelta(minutes=10):
                    warnung += "Transportzeit über 48h. "

            else:
                time_diff_str = "N/A"

            # auf doppelte oder fehlende einträge prüfen
            if previous_direction:
                if previous_direction == direction:
                    warnung += "Doppelter oder fehlender Eintrag. "

            previous_datetime = current_datetime
            previous_direction = direction

            # Display each column including the calculated time difference and error message
            row_data = [transportstation, category, direction, current_datetime, time_diff_str, warnung]
            for col_index, item in enumerate(row_data):
                label = ctk.CTkLabel(frame_results, text=str(item), font=("Arial", 12))
                label.grid(row=row_index, column=col_index, padx=10, pady=5)
    else:
        no_result_label = ctk.CTkLabel(frame_results, text="Diese Transport ID existiert nicht: " + entry_transport_id.get(), font=("Arial", 12))
        no_result_label.pack(pady=20)

# Set up the main application window with customtkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Database Query Tool")
root.geometry("900x600")

# Create a custom label and entry widget for Transport ID input
label_transport_id = ctk.CTkLabel(root, text="Enter Transport ID:", font=("Arial", 14))
label_transport_id.pack(pady=20)

entry_transport_id = ctk.CTkEntry(root, width=600, font=("Arial", 12))
entry_transport_id.pack(pady=10)

# Create a button to execute the query
button_execute = ctk.CTkButton(root, text="Fetch Data", command=fetch_data, width=200)
button_execute.pack(pady=20)

# Create a frame to display query results in a table format
frame_results = ctk.CTkFrame(root, width=860, height=300)
frame_results.pack(pady=20, padx=20, fill="both", expand=True)

# Start the GUI event loop
root.mainloop()
