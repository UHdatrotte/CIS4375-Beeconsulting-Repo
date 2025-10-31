# This file contains a function to establish a connection to the database.

import mysql.connector
from mysql.connector import Error

def create_connection(hostname, username, password, dbname):
    """Create a database connection to the MySQL database specified by the parameters."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=hostname,
            user=username,
            passwd=password,
            database=dbname
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection