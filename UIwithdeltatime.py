import pyodbc
import customtkinter as ctk
from tkinter import messagebox


# test ID:
# 99346757838434834886542


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

# Funktion zum verbinden zur Datenbank und fetch anhand ID
def fetch_data():
    transport_id = entry_transport_id.get()  #ID anfragen in der GUI
    if not transport_id:
        messagebox.showerror("Input Error", "Please enter a valid Transport ID.")
        return

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute('SELECT transportstation, category, direction, datetime FROM coolchain1 WHERE transportid = ?', (transport_id,))
        results = cursor.fetchall()
        display_results(results)
    except pyodbc.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if conn:
            conn.close()

# Funktion zum Anzeigen der GUI
def display_results(results):
    # Leeren
    for widget in frame_results.winfo_children():
        widget.destroy()

    if results:
        # Tabellen Überschriften Setsen
        headers = ["Ort", "Art der Station", "Ein- oder Ausgehend", "Datum und Uhrzeit"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(frame_results, text=header, font=("Arial", 12, "bold"))
            label.grid(row=0, column=i, padx=10, pady=5)

        # Daten in Tabelle einfügen
        for row_index, row in enumerate(results, start=1):
            for col_index, item in enumerate(row):
                label = ctk.CTkLabel(frame_results, text=str(item), font=("Arial", 12))
                label.grid(row=row_index, column=col_index, padx=10, pady=5)
    else:
        no_result_label = ctk.CTkLabel(frame_results, text="No results found for Transport ID: " + entry_transport_id.get(), font=("Arial", 12))
        no_result_label.pack(pady=20)

#GUI Fenster setup
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Coolchain Projekt 1 Interface")
root.geometry("800x600")

# Input Widget Setup
label_transport_id = ctk.CTkLabel(root, text="Transport ID:", font=("Arial", 14))
label_transport_id.pack(pady=20)

entry_transport_id = ctk.CTkEntry(root, width=600, font=("Arial", 12))
entry_transport_id.pack(pady=10)

# Button
button_execute = ctk.CTkButton(root, text="Anfragen", command=fetch_data, width=200)
button_execute.pack(pady=20)

# GUI Frame
frame_results = ctk.CTkFrame(root, width=760, height=300)
frame_results.pack(pady=20, padx=20, fill="both", expand=True)

# Start the GUI event loop
root.mainloop()
