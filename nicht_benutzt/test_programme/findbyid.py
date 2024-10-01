"""
Ausgabe Daten nach ID
Aufgabe 1.2
Version 1.0
20.8.2024
Bearbeiter: Riko 
"""
import os
import pyodbc

# Verbindungsdaten
server = 'sc-db-server.database.windows.net'
database = 'supplychain'
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

def fetch_transport_data(transport_id):
    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM coolchain1 WHERE transportid = ?', (transport_id,))
            rows = cursor.fetchall()  # Fetch all matching rows
            if rows:
                for row in rows:
                    print(row)  # Print each row
            else:
                print("No rows found with the given transport ID.")
    except pyodbc.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    while True:
        transport_id = input("Enter transport ID: ")
        if transport_id.lower() == 'exit':
            print("Exiting the program.")
            break
        fetch_transport_data(transport_id)
