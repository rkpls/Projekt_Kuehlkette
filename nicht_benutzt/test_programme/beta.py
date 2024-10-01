"""
Autoren: 
David 
Riko 
Christian V. 
Lars 
Hicham 

Kurs: 
ETS23-Python-SIZ-RSE

Projekt:
ETS-CoolChainProject-1 V1.2 Phase 1
letzte Änderung: 03.09.2024
"""

import pyodbc
import customtkinter as ctk
from tkinter import messagebox
from datetime import timedelta
from PIL import Image, ImageTk  # Import PIL to handle flag images

# Verbindungsinfo
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

transport_ids = [
    # Transport IDs...
]

# Function to connect to DB
def fetch_data():
    transport_id = dropdown_transport_id.get()
    if not transport_id:
        messagebox.showerror(lang["Fehler"], lang["Bitte eine valide Transport ID eingeben."])
        return

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute('SELECT transportstation, category, direction, datetime FROM coolchain1 WHERE transportid = ?', (transport_id,))
        results = cursor.fetchall() # results hier eine Matrix aller Daten
        display_results(results, transport_id)
    except pyodbc.Error as e:  # Error handling for database connection
        messagebox.showerror(lang["Fehler bei Datenbankzugriff. Netzwerkverbindung prüfen."], str(e))
    finally:
        if conn:
            conn.close()

# Function to display results
def display_results(results, transport_id):
    # Previous code for result display...
    pass

# Language change functions
def set_german():
    global lang
    lang = LANGUAGES["DE"]
    update_gui_language()
    show_language_buttons("DE")

def set_english():
    global lang
    lang = LANGUAGES["EN"]
    update_gui_language()
    show_language_buttons("EN")

def set_arabic():
    global lang
    lang = LANGUAGES["AR"]
    update_gui_language()
    show_language_buttons("AR")

# Function to update GUI elements with selected language
def update_gui_language():
    label_transport_id.configure(text=lang["Transport ID eingeben:"])
    button_execute.configure(text=lang["Daten prüfen"])
    
# Function to toggle the visibility of the language buttons
def show_language_buttons(current_lang):
    # Reset all buttons to be hidden
    button_language_1.place_forget()
    button_language_2.place_forget()
    button_language_3.place_forget()

    # Show only two flags (excluding the current language)
    if current_lang == "DE":
        button_language_1.place(relx=1.0, rely=0.0, anchor="ne", x=-140, y=20)  # EN
        button_language_2.place(relx=1.0, rely=0.0, anchor="ne", x=-80, y=20)   # AR
    elif current_lang == "EN":
        button_language_2.place(relx=1.0, rely=0.0, anchor="ne", x=-140, y=20)  # AR
        button_language_3.place(relx=1.0, rely=0.0, anchor="ne", x=-80, y=20)   # DE
    elif current_lang == "AR":
        button_language_1.place(relx=1.0, rely=0.0, anchor="ne", x=-140, y=20)  # EN
        button_language_3.place(relx=1.0, rely=0.0, anchor="ne", x=-80, y=20)   # DE

# Language dictionary (German, English, Arabic translations)
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
        "Diese Transport ID existiert nicht: ": "Diese Transport ID existiert nicht: ",
        "Fehler": "Fehler",
        "Bitte eine valide Transport ID eingeben.": "Bitte eine valide Transport ID eingeben.",
        "Fehler bei Datenbankzugriff. Netzwerkverbindung prüfen.": "Fehler bei Datenbankzugriff. Netzwerkverbindung prüfen."
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
        "Diese Transport ID existiert nicht: ": "This Transport ID does not exist: ",
        "Fehler": "Error",
        "Bitte eine valide Transport ID eingeben.": "Please enter a valid Transport ID.",
        "Fehler bei Datenbankzugriff. Netzwerkverbindung prüfen.": "Database access error. Please check your network connection."
    },
    "AR": {
        "Transport ID eingeben:": "ادخل رقم النقل:",
        "Daten prüfen": "التحقق من البيانات",
        "Ort": "الموقع",
        "Kategorie": "الفئة",
        "Richtung": "الاتجاه",
        "Zeitstempel": "الطابع الزمني",
        "Dauer": "المدة",
        "Warnung": "تحذير",
        "Nicht plausibler Zeitstempel": "طابع زمني غير صالح",
        "Übergabezeit über 10 Minuten": "وقت التسليم تجاوز 10 دقائق",
        "Doppelter oder fehlender Eintrag": "إدخال مكرر أو مفقود",
        "Transportstation ist doppelt": "محطة النقل مكررة",
        "Transportdauer über 48 Stunden": "مدة النقل تجاوزت 48 ساعة",
        "Diese Transport ID existiert nicht: ": "رقم النقل غير معرف: ",
        "Fehler": "خطأ",
        "Bitte eine valide Transport ID eingeben.": "يرجى ادخال رقم نقل معرف.",
        "Fehler bei Datenbankzugriff. Netzwerkverbindung prüfen.": "خطأ في الوصول إلى قاعدة البيانات. يرجى التحقق من الاتصال بالشبكة."
        # Other translations...
    }
}

# Initial language
lang = LANGUAGES["DE"]

# UI Setup
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("Kühlketten Überwachung")
root.geometry("900x700")

# Load flag images
de_flag_img = ImageTk.PhotoImage(Image.open("de_flag.png").resize((50, 50)))
en_flag_img = ImageTk.PhotoImage(Image.open("en_flag.png").resize((30, 30)))
ar_flag_img = ImageTk.PhotoImage(Image.open("ar_flag.png").resize((30, 30)))

# Create language buttons (but don't place yet)
button_language_1 = ctk.CTkButton(root, text="", image=en_flag_img, compound="left", command=set_english, width=60, fg_color="transparent")
button_language_2 = ctk.CTkButton(root, text="", image=ar_flag_img, compound="left", command=set_arabic, width=60, fg_color="transparent")
button_language_3 = ctk.CTkButton(root, text="", image=de_flag_img, compound="left", command=set_german, width=60, fg_color="transparent")

# Show only two language buttons initially
show_language_buttons("DE")

# Other UI elements
label_transport_id = ctk.CTkLabel(root, text=lang["Transport ID eingeben:"], font=("Arial", 14))
label_transport_id.pack(pady=(60, 10))

dropdown_transport_id = ctk.CTkOptionMenu(
    root,
    values=transport_ids,
    font=("Arial", 12),
    width=600,
    fg_color="black",
    button_color="black",
    button_hover_color="darkgray",
    text_color="white"
)
dropdown_transport_id.pack(pady=(10, 20))

button_execute = ctk.CTkButton(root, text=lang["Daten prüfen"], command=fetch_data, width=200)
button_execute.pack(pady=(20, 30))

# Frame for displaying results
frame_results = ctk.CTkFrame(root, width=860, height=300)
frame_results.pack(pady=20, padx=20, fill="both", expand=True)

# Start the main event loop
root.mainloop()
