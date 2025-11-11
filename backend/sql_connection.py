# This file contains a function to establish a connection to the database.

import mysql.connector
from mysql.connector import Error

def create_connection(hostname, username, userpw, dbname, **kwargs):
    """Create a database connection to the MySQL database specified by the parameters."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=hostname,
            user=username,
            password=userpw,
            database=dbname,
            **kwargs  # This will pass along any extra arguments like charset
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_read_query(connection, query, params=None):
    """Execute a SELECT query and return the results."""
    cursor = connection.cursor(dictionary=True)
    result = None
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()

def execute_write_query(connection, query, params=None):
    """Execute an INSERT, UPDATE, or DELETE query."""
    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
        return cursor.lastrowid  # Returns the ID of the last inserted row
    except Error as e:
        print(f"The error '{e}' occurred")
        connection.rollback()
        return None
    finally:
        cursor.close()