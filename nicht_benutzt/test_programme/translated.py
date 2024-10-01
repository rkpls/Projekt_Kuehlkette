import pyodbc
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta

# --------------------- Database Connection Details --------------------- #

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

# --------------------- Language Dictionaries --------------------- #

texts = {
    "de": {
        "title": "Kühlketten Überwachung",
        "label_transport_id": "Transport ID eingeben:",
        "button_execute": "Daten prüfen",
        "headers": ["Ort", "Kategorie", "Richtung", "Zeitstempel", "Dauer", "Warnung"],
        "no_result": "Diese Transport ID existiert nicht: ",
        "error_invalid_id": "Bitte eine valide Transport ID eingeben.",
        "error_db_access": "Fehler bei Datenbankzugriff. Netzwerkverbindung prüfen.",
        "error_time_difference": "Nicht plausibler Zeitstempel",
        "error_handover_time": "Übergabezeit über 10 Minuten",
        "error_duplicate_entry": "Doppelter oder fehlender Eintrag",
        "error_duplicate_station": "Transportstation ist doppelt",
        "error_transport_duration": "Transportdauer über 48 Stunden",
        "duration_na": "Nicht verfügbar"
    },
    "en": {
        "title": "Cold Chain Monitoring",
        "label_transport_id": "Enter Transport ID:",
        "button_execute": "Check Data",
        "headers": ["Location", "Category", "Direction", "Timestamp", "Duration", "Warning"],
        "no_result": "This Transport ID does not exist: ",
        "error_invalid_id": "Please enter a valid Transport ID.",
        "error_db_access": "Database access error. Please check the network connection.",
        "error_time_difference": "Implausible timestamp",
        "error_handover_time": "Handover time over 10 minutes",
        "error_duplicate_entry": "Duplicate or missing entry",
        "error_duplicate_station": "Duplicate transport station",
        "error_transport_duration": "Transport duration over 48 hours",
        "duration_na": "N/A"
    }
}

current_language = "de"  # Default language is German

# --------------------- Global Variables for Storing State --------------------- #

header_labels = []
data_labels = []
current_results = None

# --------------------- Language Toggle Function --------------------- #

def toggle_language():
    global current_language
    current_language = "en" if current_language == "de" else "de"
    update_gui_language()
    if current_results is not None:
        display_results(current_results)

def update_gui_language():
    # Update window title
    root.title(texts[current_language]["title"])
    
    # Update labels and buttons
    label_transport_id.configure(text=texts[current_language]["label_transport_id"])
    button_execute.configure(text=texts[current_language]["button_execute"])
    button_language.configure(text=current_language.upper())
    
    # Update headers if they exist
    if header_labels:
        headers = texts[current_language]["headers"]
        for label, text in zip(header_labels, headers):
            label.configure(text=text)

    # Update data labels if they exist
    if data_labels and current_results:
        update_data_labels()

# --------------------- Fetch Transport ID --------------------- #

def get_transport_id():
    return entry_transport_id.get().strip()

# --------------------- Fetch Data from Database --------------------- #

def fetch_data():
    transport_id = get_transport_id()
    if not transport_id:
        messagebox.showerror("Error", texts[current_language]["error_invalid_id"])
        return
    
    results = query_database(transport_id)
    if results:
        global current_results
        current_results = results
        display_results(results)
    else:
        messagebox.showerror("Error", texts[current_language]["no_result"] + transport_id)

def query_database(transport_id):
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        query = '''
            SELECT transportstation, category, direction, datetime
            FROM coolchain1
            WHERE transportid = ?
            ORDER BY datetime ASC
        '''
        cursor.execute(query, (transport_id,))
        return cursor.fetchall()
    except pyodbc.Error as e:
        messagebox.showerror("Error", texts[current_language]["error_db_access"])
        print("Database error: ", str(e))
        return None
    finally:
        if 'conn' in locals():
            conn.close()

# --------------------- Display Results in GUI --------------------- #

def display_results(results):
    clear_results()
    create_table_headers()
    populate_table_data(results)
    check_total_transport_duration(results)

def clear_results():
    # Clear header labels
    for label in header_labels:
        label.destroy()
    header_labels.clear()
    
    # Clear data labels
    for label in data_labels:
        label.destroy()
    data_labels.clear()

def create_table_headers():
    headers = texts[current_language]["headers"]
    for i, header in enumerate(headers):
        label = ctk.CTkLabel(frame_results, text=header, font=("Arial", 12, "bold"))
        label.grid(row=0, column=i, padx=10, pady=5, sticky="nsew")
        header_labels.append(label)

def populate_table_data(results):
    previous_datetime = None
    previous_direction = None
    previous_location = None

    for row_index, row in enumerate(results, start=1):
        transportstation, category, direction, current_datetime = row
        warnung = ""
        time_diff_str = texts[current_language]["duration_na"]

        # Calculate time difference
        if previous_datetime:
            time_difference = current_datetime - previous_datetime
            time_diff_seconds = time_difference.total_seconds()
            time_diff_str = str(time_difference)
            
            # Check timestamp plausibility
            if time_diff_seconds < 1:
                warnung = texts[current_language]["error_time_difference"]
            
            # Check handover time
            if direction.strip().lower() == "in" and time_difference > timedelta(minutes=10):
                warnung = texts[current_language]["error_handover_time"]
        else:
            first_datetime = current_datetime

        # Check for duplicate or missing entries
        if previous_direction and previous_direction == direction:
            warnung = texts[current_language]["error_duplicate_entry"]
        
        # Check for duplicate location
        if direction.strip().lower() == "in" and previous_location == transportstation:
            warnung = texts[current_language]["error_duplicate_station"]
        
        # Format datetime for display
        datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        
        # Create row data
        row_data = [
            transportstation,
            category,
            direction,
            datetime_str,
            time_diff_str,
            warnung
        ]
        
        # Create and store labels for each cell
        for col_index, item in enumerate(row_data):
            if col_index == 5 and warnung:
                label = ctk.CTkLabel(
                    frame_results,
                    text=item,
                    font=("Arial", 12, "bold"),
                    text_color="red"
                )
            else:
                label = ctk.CTkLabel(
                    frame_results,
                    text=item,
                    font=("Arial", 12)
                )
            label.grid(row=row_index, column=col_index, padx=10, pady=5, sticky="nsew")
            data_labels.append(label)
        
        previous_datetime = current_datetime
        previous_direction = direction
        previous_location = transportstation

def check_total_transport_duration(results):
    start_time = results[0][3]
    end_time = results[-1][3]
    total_duration = end_time - start_time
    
    if total_duration > timedelta(hours=48):
        warning_text = texts[current_language]["error_transport_duration"]
        label = ctk.CTkLabel(
            frame_results,
            text=warning_text,
            font=("Arial", 12, "bold"),
            text_color="red"
        )
        label.grid(
            row=len(results) + 1,
            column=0,
            columnspan=6,
            padx=10,
            pady=10,
            sticky="nsew"
        )
        data_labels.append(label)

# --------------------- Initialize and Run GUI --------------------- #

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title(texts[current_language]["title"])
root.geometry("900x600")

# Language Toggle Button
button_language = ctk.CTkButton(
    root,
    text="EN",
    width=50,
    command=toggle_language
)
button_language.pack(pady=10, padx=10, anchor='ne')

# Transport ID Label and Entry
label_transport_id = ctk.CTkLabel(
    root,
    text=texts[current_language]["label_transport_id"],
    font=("Arial", 14)
)
label_transport_id.pack(pady=(20, 5))

entry_transport_id = ctk.CTkEntry(
    root,
    width=300,
    font=("Arial", 12)
)
entry_transport_id.pack(pady=5)

# Execute Button
button_execute = ctk.CTkButton(
    root,
    text=texts[current_language]["button_execute"],
    command=fetch_data,
    width=150
)
button_execute.pack(pady=20)

# Results Frame
frame_results = ctk.CTkFrame(root)
frame_results.pack(pady=10, padx=10, fill="both", expand=True)

# Run the Application
root.mainloop()
