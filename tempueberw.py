"""
Programmabschnitt Temperaturüberwachung der Kühlstationen
Aufgabe 1.2
Version 1.0
20.8.2024
Bearbeiter: Lars 
"""

import time
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
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute('SELECT transportstationID, temperature FROM tempdata')

        rows = cursor.fetchall()
        
        for row in rows:
            temp = row.temperature
            id = row.transportstationID

            if temp > 4:
                idhigh = id
            elif temp < 2:
                idlow = id    
            else:
                pass
            
        print(f"Temperatur überschritten bei ID: {idhigh}")
        print(f"Temperatur unterschritten bei ID: {idlow}")
                
    except pyodbc.Error as e:
        print(f"Database error occurred: {e}")
    finally:
        cursor.close()
        conn.close()
        
    time.sleep(900)

