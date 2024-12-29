import mysql.connector
from mysql.connector import Error

# Define connection parameters
host = 'localhost'
user = 'root'
password = 'root'
database = 'tawos'

def connect_to_database():
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        # Check if the connection was successful
        if connection.is_connected():
            print("Successfully connected to the MySQL server")
            return connection

    except Error as e:
        print("Error while connecting to MySQL", e)
        return None
