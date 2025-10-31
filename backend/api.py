# Backend team
# This file contains the API endpoints for the backend of the application. 
# It will handle all the requests from the frontend and return the appropriate responses.

import creds
from sql_connection import create_connection
import flask
from flask import request, jsonify

myCreds = creds.Creds() # Storing the credentials in a variable to use later for the database connection.
connection = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName) # Establishing a connection to the database using the credentials stored in the variable.

# Setting up the Flask application
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/api/data', methods=['GET'])
def get_data():