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

# copy paste ids zum testen:
# 84552276793340958450995
# 34778534098134729847267
# 95662334024905944384522

while True:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    transport_id = input("Enter transport ID: ")
    cursor.execute('SELECT * FROM coolchain1 WHERE transportid = ?', (transport_id,))
    row = cursor.fetchone()
    if row:
        print(row)
    else:
        print("No row found with the given transport ID.")
    cursor.close()
    conn.close()

