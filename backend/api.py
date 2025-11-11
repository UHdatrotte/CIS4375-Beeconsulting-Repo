# app.py - Full backend with a SINGLE, CORRECT /api/submissions GET endpoint

from flask import Flask, jsonify, request, send_from_directory, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os

# --- These are your files, they are okay ---
from sql_connection import create_connection, execute_read_query, execute_write_query
import creds

# ==================== DATABASE SETUP ====================
myCreds = creds.Creds()
connection = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName, charset='utf8mb4')

# ==================== FLASK APP SETUP ====================
app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), '../frontend'),
    static_url_path=''
)
CORS(app)
app.config["DEBUG"] = True
app.secret_key = 'a_new_secret_key_for_this_fresh_start_12345'


# ==================== AUTHENTICATION ====================
@app.route('/api/login', methods=['POST'])
def login():
    # ... your login code is fine ...
    if not request.is_json:
        return jsonify({'success': False, 'message': 'Request must be JSON'}), 400
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    if not username or not password:
        return jsonify({'success': False, 'message': 'Missing username or password'}), 400
    sql = "SELECT ADMIN_ID, ADMIN_USER, ADMIN_PASS_HASH FROM ADMIN WHERE ADMIN_USER=%s"
    user_record = execute_read_query(connection, sql, (username,))
    if not user_record:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    stored_hash = user_record[0]['ADMIN_PASS_HASH'].strip()
    if check_password_hash(stored_hash, password):
        session['user'] = {'id': user_record[0]['ADMIN_ID'], 'username': user_record[0]['ADMIN_USER']}
        return jsonify({'success': True, 'user': {'username': user_record[0]['ADMIN_USER']}})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({'success': True, 'message': 'Logged out successfully'})


# ==================== PROTECTED DASHBOARD ====================
@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    # ... your dashboard code is fine ...
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized access'}), 401
    sql = "SELECT * FROM PROJECT"
    projects = execute_read_query(connection, sql)
    return jsonify({'projects': projects})


# ==================== FRONTEND ROUTES ====================
@app.route('/')
def serve_home():
    return send_from_directory(app.static_folder, 'home.html')

@app.route('/dashboard.html')
def serve_dashboard():
    # ... your route code is fine ...
    if 'user' not in session:
        return send_from_directory(app.static_folder, 'home.html')
    return send_from_directory(app.static_folder, 'dashboard.html')

@app.route('/review.html')
def serve_review():
    return send_from_directory(app.static_folder, 'review.html')

@app.route('/<path:filename>')
def serve_static(filename):
    if filename == 'dashboard.html' and 'user' not in session:
        return send_from_directory(app.static_folder, 'home.html')
    return send_from_directory(app.static_folder, filename)

# ==================== PROJECT ENDPOINTS (CRUD) ====================
@app.route('/api/project', methods=['GET'])
def project_all():
    # ... your project CRUD code is fine ...
    sql = "SELECT * FROM PROJECT"
    projects = execute_read_query(connection, sql)
    return jsonify(projects)

# ... (POST, PUT, DELETE for /api/project are fine) ...


# ==================== TESTIMONIAL ENDPOINTS (CRUD) ====================
@app.route('/api/testimonial', methods=['GET'])
def testimonial_all():
    # ... your testimonial CRUD code is fine ...
    sql = "SELECT * FROM TESTIMONIAL"
    testimonials = execute_read_query(connection, sql)
    return jsonify(testimonials)

# ... (POST, PUT, DELETE for /api/testimonial are fine) ...


# ==================== PUBLIC SUBMISSIONS (THE CORRECTED SECTION) ====================

# THIS IS THE ONLY FUNCTION FOR GETTING ALL SUBMISSIONS FOR THE DASHBOARD
@app.route('/api/submissions', methods=['GET'])
def get_all_submissions():
    cursor = connection.cursor(dictionary=True)
    
    # Testimonials - Select the new SUBMITTED_AT column
    cursor.execute("""
        SELECT 
            TESTIMONIAL_ID AS id, CONCAT(FNAME,' ',LNAME) AS name, EMAIL AS email, 
            COMPANY_NAME AS company, REVIEW AS message, SUBMITTED_AT AS dateSubmitted
        FROM TESTIMONIAL
    """)
    testimonials = cursor.fetchall()
    for t in testimonials:
        t['type'] = 'review'
        t['status'] = 'waiting'
    
    # Projects - Select the new SUBMITTED_AT column
    cursor.execute("""
        SELECT 
            PROJECT_ID AS id, CONCAT(CLIENT_FNAME,' ',CLIENT_LNAME) AS name, CLIENT_EMAIL AS email, 
            COMPANY_NAME AS company, POSITION_REQ AS title, CONTRACT_TYPE AS projectType, 
            PROJECT_DESCRIPTION AS description, CONTRACT_RATE AS budget, START_DATE AS startDate, 
            DURATION AS timeline, SUBMITTED_AT AS dateSubmitted
        FROM PROJECT
    """)
    projects = cursor.fetchall()
    for p in projects:
        p['type'] = 'proposal'
        p['status'] = 'waiting'
    
    return jsonify(testimonials + projects)

# THIS IS THE ONLY FUNCTION FOR ADDING NEW SUBMISSIONS
@app.route('/api/submissions', methods=['POST'])
def add_submission():
    data = request.get_json()
    submission_type = data.get('type')
    try:
        if submission_type == 'review':
            # --- FIX IS HERE ---
            # Match the keys sent from the frontend JavaScript exactly.
            keys = ['FNAME', 'LNAME', 'COMPANY_NAME', 'EMAIL', 'REVIEW', 'RATING']
            values = [
                data.get('FNAME'),          # Changed from 'firstname'
                data.get('LNAME'),          # Changed from 'lastname'
                data.get('COMPANY_NAME'),   # Changed from 'company'
                data.get('EMAIL'),          # Changed from 'email'
                data.get('REVIEW'),         # Changed from 'message'
                data.get('RATING')          # Changed from 'rating'
            ]
            
            # Check if any required fields are missing
            if not all([data.get('FNAME'), data.get('LNAME'), data.get('EMAIL'), data.get('REVIEW'), data.get('RATING')]):
                return jsonify({'success': False, 'message': 'Missing required fields'}), 400

            sql = f"INSERT INTO TESTIMONIAL ({','.join(keys)}) VALUES ({','.join(['%s']*len(keys))})"
            testimonial_id = execute_write_query(connection, sql, tuple(values))
            return jsonify({'success': True, 'message': 'Review submitted successfully', 'id': testimonial_id})

        elif submission_type == 'proposal':
            # (Your proposal logic seems okay, but double-check its keys as well)
            keys = [
                'CLIENT_FNAME', 'CLIENT_LNAME', 'COMPANY_NAME', 'CLIENT_EMAIL', 'CLIENT_PHONE',
                'COMPANY_STREET', 'COMPANY_CITY', 'COMPANY_STATE', 'COMPANY_ZIP', 'POSITION_REQ',
                'JOB_STREET', 'JOB_CITY', 'JOB_STATE', 'JOB_ZIP', 'CONTRACT_TYPE', 'START_DATE',
                'DURATION', 'CONTRACT_RATE', 'MARKETING', 'PROJECT_DESCRIPTION'
            ]
            values = [
                data.get('proposal_firstname'), data.get('proposal_lastname'), data.get('proposal_company'),
                data.get('proposal_email'), data.get('proposal_phone'), data.get('proposal_company_street'),
                data.get('proposal_company_city'), data.get('proposal_company_state'), data.get('proposal_company_zip'),
                data.get('proposal_position'), data.get('proposal_street'), data.get('proposal_city'),
                data.get('proposal_state'), data.get('proposal_zip'), data.get('proposal_type'),
                data.get('proposal_start_date'), data.get('proposal_timeline'), data.get('proposal_budget'),
                data.get('proposal_marketing'), data.get('proposal_description')
            ]
            sql = f"INSERT INTO PROJECT ({','.join(keys)}) VALUES ({','.join(['%s']*len(keys))})"
            project_id = execute_write_query(connection, sql, tuple(values))
            return jsonify({'success': True, 'message': 'Proposal submitted successfully', 'id': project_id})
        else:
            return jsonify({'success': False, 'message': 'Invalid submission type'}), 400
    except Exception as e:
        print(f"Error in add_submission: {e}")
        return jsonify({'success': False, 'message': 'An internal server error occurred'}), 500
# ... (Your Approve / Deny submission routes are fine) ...


# ==================== RUN APPLICATION ====================
if __name__ == '__main__':
    app.run(debug=True, port=5000)