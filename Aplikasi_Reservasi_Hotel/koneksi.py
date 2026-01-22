import mysql.connector

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",      # default XAMPP
            database="db_reservasi_hotel"
        )
        return conn
    except mysql.connector.Error as e:
        print("Koneksi gagal:", e)
        return None
