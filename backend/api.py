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
def get_connection():
    return create_connection(myCreds.conString,myCreds.userName,myCreds.password,myCreds.dbName,charset='utf8mb4')  # Create a helper function that creates a new one every time a request comes in.

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
    conn = get_connection() 
    user_record = execute_read_query(conn, sql, (username,))
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
    conn = get_connection() 
    projects = execute_read_query(conn, sql)
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
    conn = get_connection() 
    projects = execute_read_query(conn, sql)
    return jsonify(projects)

# ... (POST, PUT, DELETE for /api/project are fine) ...


# ==================== TESTIMONIAL ENDPOINTS (CRUD) ====================
@app.route('/api/testimonial', methods=['GET'])
def testimonial_all():
    # ... your testimonial CRUD code is fine ...
    sql = "SELECT * FROM TESTIMONIAL"
    conn = get_connection() 
    testimonials = execute_read_query(conn, sql)
    return jsonify(testimonials)

# ... (POST, PUT, DELETE for /api/testimonial are fine) ...


# ==================== PUBLIC SUBMISSIONS (THE CORRECTED SECTION) ====================
@app.route('/api/submissions', methods=['GET'])
def get_all_submissions():
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT 
                TESTIMONIAL_ID AS id,
                CONCAT(FNAME, ' ', LNAME) AS name,
                EMAIL AS email,
                COMPANY_NAME AS company,
                REVIEW AS message,
                SUBMITTED_AT AS dateSubmitted
            FROM TESTIMONIAL
        """)
        testimonials = cur.fetchall()

        cur.execute("""
            SELECT 
                TESTIMONIAL_ID AS id,
                ACTION_TYPE,
                TIME_STAMP
            FROM TESTIMONIAL_AUDIT
            ORDER BY TIME_STAMP DESC
        """)
        t_audits = cur.fetchall()

        latest_t_action = {}
        for row in t_audits:
            if row["id"] not in latest_t_action:
                latest_t_action[row["id"]] = row["ACTION_TYPE"]

        for t in testimonials:
            action = latest_t_action.get(t["id"])
            if action == "APPROVED":
                status = "approved"
            elif action == "DENIED":
                status = "denied"
            else:
                status = "waiting"

            t["type"] = "review"
            t["status"] = status

        cur.execute("""
            SELECT
                PROJECT_ID AS id,
                CONCAT(CLIENT_FNAME, ' ', CLIENT_LNAME) AS name,
                CLIENT_EMAIL AS email,
                COMPANY_NAME AS company,
                POSITION_REQ AS title,
                CONTRACT_TYPE AS projectType,
                PROJECT_DESCRIPTION AS description,
                CONTRACT_RATE AS budget,
                START_DATE AS startDate,
                DURATION AS timeline,
                SUBMITTED_AT AS dateSubmitted
            FROM PROJECT
        """)
        projects = cur.fetchall()

        cur.execute("""
            SELECT 
                PROJECT_ID AS id,
                ACTION_TYPE,
                TIME_STAMP
            FROM PROJECT_AUDIT
            ORDER BY TIME_STAMP DESC
        """)
        p_audits = cur.fetchall()

        latest_p_action = {}
        for row in p_audits:
            if row["id"] not in latest_p_action:
                latest_p_action[row["id"]] = row["ACTION_TYPE"]

        for p in projects:
            action = latest_p_action.get(p["id"])
            if action == "APPROVED":
                status = "approved"
            elif action == "DENIED":
                status = "denied"
            else:
                status = "waiting"

            p["type"] = "proposal"
            p["status"] = status

        cur.close()
        conn.close()
        return jsonify(testimonials + projects)

    except Exception as e:
        print("Error in get_all_submissions:", e)
        return jsonify({
            "success": False,
            "message": "Server error in /api/submissions"
        }), 500

# ==================== PUBLIC SUBMISSIONS (CREATE NEW SUBMISSION) ====================
@app.route('/api/submissions', methods=['POST'])
def add_submission():
    try:
        data = request.get_json() or {}
        submission_type = data.get('type')

        conn = get_connection()
        cur = conn.cursor()

        if submission_type == 'review':
            sql = """
                INSERT INTO TESTIMONIAL
                    (FNAME, LNAME, COMPANY_NAME, EMAIL, REVIEW, RATING)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            vals = (
                data.get('FNAME'),
                data.get('LNAME'),
                data.get('COMPANY_NAME'),
                data.get('EMAIL'),
                data.get('REVIEW'),
                data.get('RATING'),
            )
            cur.execute(sql, vals)
            conn.commit()
            new_id = cur.lastrowid

        elif submission_type == 'proposal':
            sql = """
                INSERT INTO PROJECT
                    (CLIENT_FNAME, CLIENT_LNAME, COMPANY_NAME, CLIENT_EMAIL, CLIENT_PHONE,
                     COMPANY_STREET, COMPANY_CITY, COMPANY_STATE, COMPANY_ZIP,
                     POSITION_REQ,
                     JOB_STREET, JOB_CITY, JOB_STATE, JOB_ZIP,
                     CONTRACT_TYPE, START_DATE, DURATION, CONTRACT_RATE,
                     MARKETING, PROJECT_DESCRIPTION)
                VALUES
                    (%s, %s, %s, %s, %s,
                     %s, %s, %s, %s,
                     %s,
                     %s, %s, %s, %s,
                     %s, %s, %s, %s,
                     %s, %s)
            """
            vals = (
                data.get('proposal_firstname'),
                data.get('proposal_lastname'),
                data.get('proposal_company'),
                data.get('proposal_email'),
                data.get('proposal_phone'),
                data.get('proposal_company_street'),
                data.get('proposal_company_city'),
                data.get('proposal_company_state'),
                data.get('proposal_company_zip'),
                data.get('proposal_position'),
                data.get('proposal_street'),
                data.get('proposal_city'),
                data.get('proposal_state'),
                data.get('proposal_zip'),
                data.get('proposal_type'),
                data.get('proposal_start_date'),
                data.get('proposal_timeline'),
                data.get('proposal_budget'),
                data.get('proposal_marketing'),
                data.get('proposal_description'),
            )
            cur.execute(sql, vals)
            conn.commit()
            new_id = cur.lastrowid

        else:
            cur.close()
            conn.close()
            return jsonify({'success': False, 'message': 'Invalid submission type'}), 400

        cur.close()
        conn.close()
        return jsonify({'success': True, 'id': new_id})

    except Exception as e:
        print("Error in add_submission:", e)
        return jsonify({'success': False, 'message': 'Internal server error'}), 500


# ==================== UPDATE STATUS + AUDIT ====================
@app.route('/api/submissions/<int:submission_id>/status', methods=['POST'])
def update_submission_status(submission_id):
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    data = request.get_json() or {}

    raw_action = data.get('action', '')
    raw_type   = data.get('type', '')

    action = raw_action.strip().lower()   
    typ = raw_type.strip().lower()     

    print('DEBUG update_status:', data, '=> action=', action, 'type=', typ)

    admin_id = session['user']['id']

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # ---- REVIEW (TESTIMONIAL) ----
        if typ == 'review':
            cursor.execute(
                """
                INSERT INTO TESTIMONIAL_AUDIT
                    (TESTIMONIAL_ID, ADMIN_ID, TIME_STAMP, ACTION_TYPE)
                VALUES (%s, %s, NOW(), %s)
                """,
                (submission_id, admin_id, action.upper())   # APPROVED / DENIED
            )

        # ---- PROPOSAL (PROJECT) ----
        elif typ == 'proposal':
            cursor.execute(
                """
                INSERT INTO PROJECT_AUDIT
                    (PROJECT_ID, ADMIN_ID, TIME_STAMP, ACTION_TYPE)
                VALUES (%s, %s, NOW(), %s)
                """,
                (submission_id, admin_id, action.upper())
            )

        else:
            cursor.close()
            conn.close()
            return jsonify({
                'success': False,
                'message': f'Unknown type: {raw_type}'
            }), 200

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'success': True, 'status': action})

    except Exception as e:
        print('Error updating submission status:', e)
        return jsonify({
            'success': False,
            'message': 'Server error while updating status'
        }), 500


# ==================== ADMIN ACTION LOGGING HELPERS ====================

def log_testimonial_action(admin_id, testimonial_id, action_type):
    """Record administrator actions in the TESTIMONIAL_AUDIT table"""
    conn = get_connection()
    sql = """
        INSERT INTO TESTIMONIAL_AUDIT (TESTIMONIAL_ID, ADMIN_ID, ACTION_TYPE)
        VALUES (%s, %s, %s)
    """
    execute_write_query(conn, sql, (testimonial_id, admin_id, action_type))
    conn.close()


def log_project_action(admin_id, project_id, action_type):
    """Record administrator actions in the PROJECT_AUDIT table"""
    conn = get_connection()
    sql = """+
        INSERT INTO PROJECT_AUDIT (PROJECT_ID, ADMIN_ID, ACTION_TYPE)
        VALUES (%s, %s, %s)
    """
    execute_write_query(conn, sql, (project_id, admin_id, action_type))
    conn.close()

# ==================== ADMIN ACTION ROUTES (APPROVE / DENY) ====================

@app.route('/api/submissions/<int:submission_id>/approve', methods=['POST'])
def approve_submission(submission_id):
    """Approve reviews or project proposals and record them in the AUDIT table"""
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    data = request.get_json() or {}
    submission_type = data.get('type')  # 'review' or 'proposal'
    admin_id = session['user']['id']

    try:
        if submission_type == 'review':
            # REVIEW Approval Record
            log_testimonial_action(admin_id, submission_id, 'APPROVED')
        elif submission_type == 'proposal':
            # PROJECT Approval Record
            log_project_action(admin_id, submission_id, 'APPROVED')
        else:
            return jsonify({'success': False, 'message': 'Invalid submission type'}), 400

        return jsonify({'success': True})
    except Exception as e:
        print("Error in approve_submission:", e)
        return jsonify({'success': False, 'message': 'Internal server error'}), 500


@app.route('/api/submissions/<int:submission_id>/deny', methods=['POST'])
def deny_submission(submission_id):
    """Reject a review or project proposal and record it in the AUDIT table."""
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    data = request.get_json() or {}
    submission_type = data.get('type')  # 'review' or 'proposal'
    admin_id = session['user']['id']

    try:
        if submission_type == 'review':
            # REVIEW deny record
            log_testimonial_action(admin_id, submission_id, 'DENIED')
        elif submission_type == 'proposal':
            # PROJECT deny record
            log_project_action(admin_id, submission_id, 'DENIED')
        else:
            return jsonify({'success': False, 'message': 'Invalid submission type'}), 400

        return jsonify({'success': True})
    except Exception as e:
        print("Error in deny_submission:", e)
        return jsonify({'success': False, 'message': 'Internal server error'}), 500



# ==================== RUN APPLICATION ====================
if __name__ == '__main__':
    app.run(debug=True, port=5000)