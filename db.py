import mysql.connector

config = {
    'user': 'root',
    'password': '12345678',
    'host': '127.0.0.1',
    'database': 'test'
}

def connection():
    try:
        cnx = mysql.connector.connect(**config)
        print("went well")
        return cnx
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None