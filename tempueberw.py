"""
Programmabschnitt Temperaturüberwachung der Kühlstationen
Aufgabe 1.2
Version 0
20.8.2024
Bearbeiter: 
"""


import pyodbc
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

while True:
        # Verbindung herstellen
    conn = pyodbc.connect(conn_str)
        # Cursor erstellen
    cursor = conn.cursor()
        # SQL-Statement ausführen
    cursor.execute('SELECT * FROM coolchain1')

    transport_id = input("Enter transport ID: ")
    cursor.execute('SELECT * FROM coolchain1 WHERE transportid = ?', (transport_id,))
    row = cursor.fetchone()
    if temp:
        print(row)
    else:
        print("No row found with the given transport ID.")
    cursor.close()
    conn.close()

