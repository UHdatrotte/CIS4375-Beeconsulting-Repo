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

# Endpoint for projects

# This API will be called in the dashboard page of the frontend so admin can see all projects.
@app.route('/api/project', methods=['GET'])
def project_all(): # Return all projects
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM PROJECT"
    cursor.execute(query)
    project = cursor.fetchall()
    return jsonify(project)

# This API will be called on the form submission page of the frontend
@app.route('/api/project', methods=['POST'])
def add_project(): # Adds a new project to the database.
    request_data = request.get_json() # This is a payload that is sent from the frontend when a new project is created.
    
    new_client_fname = request_data['CLIENT_FNAME']
    new_client_lname = request_data['CLIENT_LNAME']
    new_company_name = request_data['COMPANY_NAME']
    new_client_email = request_data['CLIENT_EMAIL']
    new_client_phone = request_data['CLIENT_PHONE']
    new_company_street = request_data['COMPANY_STREET']
    new_company_city = request_data['COMPANY_CITY']
    new_company_state = request_data['COMPANY_STATE']
    new_company_zip = request_data['COMPANY_ZIP']
    new_contract_type = request_data['CONTRACT_TYPE']
    new_start_date = request_data['START_DATE']
    new_duration = request_data['DURATION']
    new_contract_rate = request_data['CONTRACT_RATE']
    new_position_req = request_data['POSITION_REQ']
    new_job_street = request_data['JOB_STREET']
    new_job_city = request_data['JOB_CITY']
    new_job_state = request_data['JOB_STATE']
    new_job_zip = request_data['JOB_ZIP']
    new_marketing = request_data['MARKETING']

    cursor = connection.cursor(dictionary=True)

    query = f"""INSERT INTO PROJECT (CLIENT_FNAME, CLIENT_LNAME, COMPANY_NAME, CLIENT_EMAIL, CLIENT_PHONE, COMPANY_STREET, COMPANY_CITY, COMPANY_STATE, COMPANY_ZIP, CONTRACT_TYPE, START_DATE, DURATION, CONTRACT_RATE, POSITION_REQ, JOB_STREET, JOB_CITY, JOB_STATE, JOB_ZIP, MARKETING) 
    VALUES ('{new_client_fname}', '{new_client_lname}', '{new_company_name}', '{new_client_email}', '{new_client_phone}', '{new_company_street}', '{new_company_city}', '{new_company_state}', '{new_company_zip}', '{new_contract_type}', '{new_start_date}', '{new_duration}', '{new_contract_rate}', '{new_position_req}', '{new_job_street}', '{new_job_city}', '{new_job_state}', '{new_job_zip}', '{new_marketing}')"""

    cursor.execute(query)
    return f"Project added successfully by {new_client_fname} {new_client_lname} from {new_company_name}"

# This API will be called in the dashboard page of the frontend for the admin.
@app.route('/api/project', methods=['PUT'])
def update_project(): # Updates a current project in the database.
    request_data = request.get_json() # Payload protected by the frontend.
    
    idtoUpdate = request_data['PROJECT_ID'] # This is the ID of the project that needs to be updated.

    new_client_fname = request_data['CLIENT_FNAME']
    new_client_lname = request_data['CLIENT_LNAME']
    new_company_name = request_data['COMPANY_NAME']
    new_client_email = request_data['CLIENT_EMAIL']
    new_client_phone = request_data['CLIENT_PHONE']
    new_company_street = request_data['COMPANY_STREET']
    new_company_city = request_data['COMPANY_CITY']
    new_company_state = request_data['COMPANY_STATE']
    new_company_zip = request_data['COMPANY_ZIP']
    new_contract_type = request_data['CONTRACT_TYPE']
    new_start_date = request_data['START_DATE']
    new_duration = request_data['DURATION']
    new_contract_rate = request_data['CONTRACT_RATE']
    new_position_req = request_data['POSITION_REQ']
    new_job_street = request_data['JOB_STREET']
    new_job_city = request_data['JOB_CITY']
    new_job_state = request_data['JOB_STATE']
    new_job_zip = request_data['JOB_ZIP']
    new_marketing = request_data['MARKETING']

    cursor = connection.cursor(dictionary=True)

    query = f"""UPDATE PROJECT SET CLIENT_FNAME = '{new_client_fname}', CLIENT_LNAME = '{new_client_lname}', COMPANY_NAME = '{new_company_name}', CLIENT_EMAIL = '{new_client_email}', CLIENT_PHONE = '{new_client_phone}', 
    COMPANY_STREET = '{new_company_street}', COMPANY_CITY = '{new_company_city}', COMPANY_STATE = '{new_company_state}', COMPANY_ZIP = '{new_company_zip}',
    CONTRACT_TYPE = '{new_contract_type}', START_DATE = '{new_start_date}', DURATION = '{new_duration}', CONTRACT_RATE = '{new_contract_rate}', POSITION_REQ = '{new_position_req}', 
    JOB_STREET = '{new_job_street}', JOB_CITY = '{new_job_city}', JOB_STATE = '{new_job_state}', JOB_ZIP = '{new_job_zip}', MARKETING = '{new_marketing}' 
    WHERE PROJECT_ID = {idtoUpdate}"""

    cursor.execute(query)
    return f"Project {idtoUpdate} has been updated successfully by TCI Admin"

# This API will be called in the dashboard page of the frontend for the admin.
# Note: Make sure the project is deleted from other tables first! Will come back to this later...
"""@app.route('/api/project', methods=['DELETE']) # Deletes a current project stored in the database.
def delete_project():
    request_data = request.get_json() # Payload protected by the frontend.
    
    idtoDelete = request_data['PROJECT_ID'] # This is the ID of the project that needs to be deleted.

    cursor = connection.cursor(dictionary=True)

    query = f"DELETE FROM PROJECT WHERE PROJECT_ID = {idtoDelete}"

    cursor.execute(query)
    return f"Project {idtoDelete} has been deleted successfully by TCI Admin"
"""
app.run()