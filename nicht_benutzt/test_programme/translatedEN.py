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
        display_results(results, transport_id)
    except pyodbc.Error as e:
        messagebox.showerror("Fehler bei Datenbankzugriff. Netzwerkverbindung prüfen.", str(e))
    finally:
        if conn:
            conn.close()

# Function to display results in the GUI with time difference and error detection
def display_results(results, transport_id):
    # Vorherige Einträge leeren
    for widget in frame_results.winfo_children():
        widget.destroy()
        
    if results:
        # Create table headers
        headers = [lang["Ort"], lang["Kategorie"], lang["Richtung"], lang["Zeitstempel"], lang["Dauer"], lang["Warnung"]]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(frame_results, text=header, font=("Arial", 12, "bold"))
            label.grid(row=0, column=i, padx=10, pady=5)

        previous_datetime = None
        previous_direction = None
        first_datetime = results[0][3]  # Ersten Zeiteintrag speichern
        last_datetime = None
        previous_location = None
        
        # Schleife zum eintragen der Daten in die Tabelle
        for row_index, row in enumerate(results, start=1):
            transportstation, category, direction, current_datetime = row

            last_datetime = current_datetime  # aktuellen Zeiteintrag als letzten speichern
            warnung = " "

            # Zeitdifferenz berechnen
            if previous_datetime:
                time_difference = current_datetime - previous_datetime
                time_diff_str = str(time_difference)
                
                # Zeitstempel prüfen
                if time_difference.total_seconds() < 1:
                    warnung = lang["Nicht plausibler Zeitstempel"]

                # Übergabezeit prüfen
                if direction == "'in'" and time_difference > timedelta(minutes=10):
                    warnung = lang["Übergabezeit über 10 Minuten"]

            else:
                time_diff_str = "N/A"

            # auf doppelte oder fehlende einträge prüfen
            if previous_direction:
                if previous_direction == direction:
                    warnung = lang["Doppelter oder fehlender Eintrag"]

            previous_datetime = current_datetime
            previous_direction = direction

            # Doppelten Ort Überprüfen
            if direction == "'in'" and previous_location == transportstation:
                warnung = lang["Transportstation ist doppelt"]
                
            previous_location = transportstation
                
            # Display each column including the calculated time difference and error message
            row_data = [transportstation, category, direction, current_datetime, time_diff_str, warnung]
            for col_index, item in enumerate(row_data):
                if col_index == 5:
                    label = ctk.CTkLabel(frame_results, text=str(item), font=("Arial", 14, "bold"), text_color="red")
                    label.grid(row=row_index, column=col_index, padx=10, pady=5)
                else:
                    label = ctk.CTkLabel(frame_results, text=str(item), font=("Arial", 12))
                    label.grid(row=row_index, column=col_index, padx=10, pady=5)

        total_time_difference = last_datetime - first_datetime
        if total_time_difference > timedelta(hours=48):
            final_error_label = ctk.CTkLabel(frame_results, text=lang["Transportdauer über 48 Stunden"], font=("Arial", 14, "bold"), text_color="red")
            final_error_label.grid(row=row_index + 1, column=5, columnspan=1, pady=0)

    else:
        no_result_label = ctk.CTkLabel(frame_results, text=lang["Diese Transport ID existiert nicht: "] + entry_transport_id.get(), font=("Arial", 14, "bold"), text_color="black", fg_color="yellow")
        no_result_label.pack(pady=20)

# Function to toggle language between German and English
def toggle_language():
    global lang
    if lang == LANGUAGES["DE"]:
        lang = LANGUAGES["EN"]
        button_language.configure(text="DE")
    else:
        lang = LANGUAGES["DE"]
        button_language.configure(text="EN")
    update_gui_language()

# Function to update the GUI language dynamically
def update_gui_language():
    label_transport_id.configure(text=lang["Transport ID eingeben:"])
    button_execute.configure(text=lang["Daten prüfen"])
    # Update other elements if needed

# Language dictionaries
LANGUAGES = {
    "DE": {
        "Transport ID eingeben:": "Transport ID eingeben:",
        "Daten prüfen": "Daten prüfen",
        "Ort": "Ort",
        "Kategorie": "Kategorie",
        "Richtung": "Richtung",
        "Zeitstempel": "Zeitstempel",
        "Dauer": "Dauer",
        "Warnung": "Warnung",
        "Nicht plausibler Zeitstempel": "Nicht plausibler Zeitstempel",
        "Übergabezeit über 10 Minuten": "Übergabezeit über 10 Minuten",
        "Doppelter oder fehlender Eintrag": "Doppelter oder fehlender Eintrag",
        "Transportstation ist doppelt": "Transportstation ist doppelt",
        "Transportdauer über 48 Stunden": "Transportdauer über 48 Stunden",
        "Diese Transport ID existiert nicht: ": "Diese Transport ID existiert nicht: "
    },
    "EN": {
        "Transport ID eingeben:": "Enter Transport ID:",
        "Daten prüfen": "Check Data",
        "Ort": "Location",
        "Kategorie": "Category",
        "Richtung": "Direction",
        "Zeitstempel": "Timestamp",
        "Dauer": "Duration",
        "Warnung": "Warning",
        "Nicht plausibler Zeitstempel": "Invalid Timestamp",
        "Übergabezeit über 10 Minuten": "Handover Time over 10 Minutes",
        "Doppelter oder fehlender Eintrag": "Duplicate or Missing Entry",
        "Transportstation ist doppelt": "Duplicate Transport Station",
        "Transportdauer über 48 Stunden": "Transport Duration over 48 Hours",
        "Diese Transport ID existiert nicht: ": "This Transport ID does not exist: "
    }
}

# Set default language
lang = LANGUAGES["DE"]

# Set up the main application window with customtkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Kühlketten Überwachung")
root.geometry("900x600")

# Create a custom label and entry widget for Transport ID input
label_transport_id = ctk.CTkLabel(root, text=lang["Transport ID eingeben:"], font=("Arial", 14))
label_transport_id.pack(pady=(60, 10))  # Adjusted padding

entry_transport_id = ctk.CTkEntry(root, width=600, font=("Arial", 12))
entry_transport_id.pack(pady=(10, 20))  # Adjusted padding

# Create a button to execute the query
button_execute = ctk.CTkButton(root, text=lang["Daten prüfen"], command=fetch_data, width=200)
button_execute.pack(pady=(20, 30))  # Adjusted padding

# Create a frame to display query results in a table format
frame_results = ctk.CTkFrame(root, width=860, height=300)
frame_results.pack(pady=20, padx=20, fill="both", expand=True)

# Add a language toggle button at the top right corner
button_language = ctk.CTkButton(root, text="EN", command=toggle_language, width=50)
button_language.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=20)

# Start the GUI event loop
root.mainloop()
