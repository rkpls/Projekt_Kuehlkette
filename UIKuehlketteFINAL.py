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
ETS-CoolChainProject-1 V1.3 Phase 1
letzte Änderung: 17.09.2024
"""

import pyodbc
import customtkinter as ctk
from tkinter import messagebox
from datetime import timedelta, datetime

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
    "72359278599178561029675",
    "15668407856331648336231",
    "73491878556297128760578",
    "99346757838434834886542",
    "46204863139457546291334",
    "77631003455214677542311",
    "34778534098134729847267",
    "64296734612883933474299",
    "84356113249506843372979",
    "23964376768701928340034",
    "55638471099438572108556",
    "84552276793340958450995",
    "96853785349211053482893",
    "68345254400506854834562",
    "67424886737245693583645",
    "85746762813849598680239",
    "56993454245564893300000",
    "95662334024905944384522",
    "13456783852887496020345",
    "76381745965049879836902"
]

# Def Verbindung Datenbank
def fetch_data():
    transport_id = dropdown_transport_id.get()
    if not transport_id:
        messagebox.showerror(lang["Fehler"], lang["Bitte eine valide Transport ID eingeben."])
        return

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute('SELECT transportstation, category, direction, datetime FROM coolchain1 WHERE transportid = ?', (transport_id,))
        results = cursor.fetchall() # results: hier eine Matrix aller Daten
        display_results(results, transport_id)
    except pyodbc.Error as e: #Fehlerabfang, Meldung im Fenster ausgeben
        messagebox.showerror(lang["Fehler bei Datenbankzugriff. Netzwerkverbindung prüfen."], str(e))
    finally:
        if conn:
            conn.close()


# Def Daten Anzeigen
def display_results(results, transport_id):

    for widget in frame_results.winfo_children():
        widget.destroy()

    if results:

        headers = [lang["Ort"], lang["Kategorie"], lang["Richtung"], lang["Zeitstempel"], lang["Dauer"], lang["Warnung"]]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(frame_results, text=header, font=("Arial", 12, "bold"))
            label.grid(row=0, column=i, padx=10, pady=5)

        previous_datetime = None
        previous_direction = None
        first_datetime = results[0][3]
        last_datetime = None
        previous_location = None

        for row_index, row in enumerate(results, start=1):
            transportstation, category, direction, current_datetime = row

            last_datetime = current_datetime
            last_direction = direction
            warnung = " "

            if previous_datetime:
                time_difference = current_datetime - previous_datetime
                time_diff_str = str(time_difference)

                if time_difference.total_seconds() < 1:
                    warnung = lang["Nicht plausibler Zeitstempel"]

                if direction == "'in'" and time_difference > timedelta(minutes=10):
                    warnung = lang["Übergabezeit über 10 Minuten"]

            else:
                time_diff_str = "N/A"

            if previous_direction:
                if previous_direction == direction:
                    warnung = lang["Doppelter oder fehlender Eintrag"]

            previous_datetime = current_datetime
            previous_direction = direction

            if direction == "'in'" and previous_location == transportstation:
                warnung = lang["Transportstation ist doppelt"]

            previous_location = transportstation

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

        if last_direction == "'in'":
            delta_to_present = datetime.now() - last_datetime
            days = delta_to_present.days
            hours = delta_to_present.seconds // 3600    
            final_error_label = ctk.CTkLabel(frame_results, text=lang ["Lieferung nicht vollständig. Zeit seit letztem Eintrag: "] + '\u200e' + f" {days}d {hours}h", font=("Arial", 14, "bold"), text_color="red")
            final_error_label.grid(row=row_index + 2, column=5, columnspan=1, pady=0)

    else:
        no_result_label = ctk.CTkLabel(frame_results, text=lang["Diese Transport ID existiert nicht: "] + transport_id, font=("Arial", 14, "bold"), text_color="black", fg_color="yellow")
        no_result_label.pack(pady=20)
        
# lokalisierung DE
def set_german():
    global lang
    lang = LANGUAGES["DE"]
    update_gui_language()

# lokalisierung EN
def set_english():
    global lang
    lang = LANGUAGES["EN"]
    update_gui_language()

# lokalisierung AR
def set_arabic():
    global lang
    lang = LANGUAGES["AR"]
    update_gui_language()

# update lokalisierung Button
def update_gui_language():
    label_transport_id.configure(text=lang["Transport ID eingeben:"])

    if lang == LANGUAGES["DE"]:
        button_language_1.configure(text="EN", command=set_english)
        button_language_2.configure(text="AR", command=set_arabic)
    elif lang == LANGUAGES["EN"]:
        button_language_1.configure(text="DE", command=set_german)
        button_language_2.configure(text="AR", command=set_arabic)
    elif lang == LANGUAGES["AR"]:
        button_language_1.configure(text="DE", command=set_german)
        button_language_2.configure(text="EN", command=set_english)
        
    fetch_data()

# hinterlegung der Sprachen
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
        "Fehler bei Datenbankzugriff. Netzwerkverbindung prüfen.": "Fehler bei Datenbankzugriff. Netzwerkverbindung prüfen.",
        "Lieferung nicht vollständig. Zeit seit letztem Eintrag: ": "Lieferung nicht vollständig. Zeit seit letztem Eintrag: "
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
        "Fehler bei Datenbankzugriff. Netzwerkverbindung prüfen.": "Database access error. Please check your network connection.",
        "Lieferung nicht vollständig. Zeit seit letztem Eintrag: ": "Delivery incomplete. Time since last entry: "
    },
    "AR": {
        "Transport ID eingeben:": "أدخل معرف النقل:",
        "Daten prüfen": "تحقق من البيانات",
        "Ort": "الموقع",
        "Kategorie": "الفئة",
        "Richtung": "الاتجاه",
        "Zeitstempel": "الطابع الزمني",
        "Dauer": "المدة",
        "Warnung": "تحذير",
        "Nicht plausibler Zeitstempel": "طابع زمني غير صالح",
        "Übergabezeit über 10 Minuten": "وقت التسليم أكثر من 10 دقائق",
        "Doppelter oder fehlender Eintrag": "إدخال مكرر أو مفقود",
        "Transportstation ist doppelt": "محطة النقل مكررة",
        "Transportdauer über 48 Stunden": "مدة النقل أكثر من 48 ساعة",
        "Diese Transport ID existiert nicht: ": "معرف النقل هذا غير موجود: ",
        "Fehler": "خطأ",
        "Bitte eine valide Transport ID eingeben.": "يرجى إدخال معرف نقل صالح.",
        "Fehler bei Datenbankzugriff. Netzwerkverbindung prüfen.": "خطأ في الوصول إلى قاعدة البيانات. يرجى التحقق من اتصال الشبكة.",
        "Lieferung nicht vollständig. Zeit seit letztem Eintrag: ": "التسليم غير مكتمل. الوقت منذ آخر تسجيل: "
    }
}

# Sprache bei Start 
lang = LANGUAGES["DE"]

# UI Fenster aufsetzen: Dark mode, blaue Akzente, Name, Größe
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("Kühlketten Überwachung")
root.geometry("1200x700") 

# Überschrift Eingabebox Knopf
label_transport_id = ctk.CTkLabel(root, text=lang["Transport ID eingeben:"], font=("Arial", 14))
label_transport_id.pack(pady=(60, 10))
dropdown_transport_id = ctk.CTkOptionMenu(
    root,
    values=transport_ids,
    font=("Arial", 12),
    width=600,
    fg_color="black",  # Hintergrundfarbe des drop down menu
    button_color="black",  # Farbe des Schalters
    button_hover_color="darkgray",  # Farbe wenn über den Schalter/Knopf gefahren wird
    text_color="white",  # Textfarbe
    command=lambda choice: fetch_data()  # Direkte Aufruf der Funktion nach Auswahl
)
dropdown_transport_id.pack(pady=(10, 20))

# Rahmen für Liste
frame_results = ctk.CTkFrame(root, width=860, height=300)
frame_results.pack(pady=20, padx=20, fill="both", expand=True)

# Knöpfe für Lokalisierung
button_language_1 = ctk.CTkButton(root, text="EN", command=set_english, width=50)
button_language_1.place(relx=1.0, rely=0.0, anchor="ne", x=-80, y=20)

button_language_2 = ctk.CTkButton(root, text="AR", command=set_arabic, width=50)
button_language_2.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=20)

# Programmstart
root.mainloop()



"""
Copy Paste IDs mit Fehlern:

15668407856331648336231                 >10min
99346757838434834886542                 >48h
77631003455214677542311                 >10min
23964376768701928340034                 kein auscheck
55638471099438572108556                 - Zeit
84552276793340958450995                 >10min
68345254400506854834562                 selbes lager
67424886737245693583645                 doppelt auscheck
56993454245564893300000                 kein Eintrag
"""