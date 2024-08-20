"""
Programmabschnitt Lieferdatenverschlüsselung
Aufgabe 1.3
Version 0
20.8.2024
Bearbeiter: 
"""


from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import pyodbc
import base64


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

password_enc = b'mysecretpassword'
iv_enc = b'passwort-salzen!'

def decrypt_data(encrypted_data):
    encrypted_data_bytes = base64.b64decode(encrypted_data)
    cipher = AES.new(password_enc, AES.MODE_CBC, iv_enc)
    decrypted_data = cipher.decrypt(encrypted_data_bytes)
    unpadded_data = decrypted_data.rstrip(b'\x00')
    return unpadded_data.decode('utf-8')

# copy paste ids zum testen:
# 84552276793340958450995
# 34778534098134729847267
# 95662334024905944384522

while True:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    transport_id = input("Enter transport ID: ")
    cursor.execute('SELECT * FROM v_coolchain_crypt WHERE transportID = ?', (transport_id,))
    row = cursor.fetchone()
    if row:
        decrypted_row = []
        for value in row:
            if isinstance(value, str) and value.startswith('ENC:'):  # Assuming encrypted data is prefixed with 'ENC:'
                encrypted_part = value[4:]  # Remove the 'ENC:' prefix
                decrypted_part = decrypt_data(encrypted_part)
                decrypted_row.append(decrypted_part)
            else:
                decrypted_row.append(value)
        
        print(decrypted_row)
    else:
        print("No row found with the given transport ID.")
            
    cursor.close()
    conn.close()

