import sqlite3
import streamlit as st
import logging
from contextlib import contextmanager
from datetime import datetime, timedelta
import json
import bcrypt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_NAME = 'miracle_healthcare.db'

@contextmanager
def get_db_connection():
    """Create a database connection with proper error handling"""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        yield conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {str(e)}")
        st.error(f"Database connection error: {str(e)}")
    finally:
        if conn:
            conn.close()

def execute_db_query(query, params=None, fetch=True):
    """Execute database query with proper error handling"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                result = cursor.fetchall()
            else:
                conn.commit()
                result = True
            
            return result
    except sqlite3.Error as e:
        logger.error(f"Database query error: {str(e)}")
        st.error(f"Database query error: {str(e)}")
        return None

def init_db():
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            
            # Users table
            c.execute('''CREATE TABLE IF NOT EXISTS users
                         (id INTEGER PRIMARY KEY,
                          email TEXT UNIQUE,
                          password BLOB,
                          first_name TEXT,
                          last_name TEXT,
                          mobile TEXT,
                          role TEXT,
                          registration_date TEXT,
                          last_login TEXT,
                          last_activity TEXT,
                          status TEXT DEFAULT 'active',
                          profile_locked BOOLEAN DEFAULT 0,
                          profile_picture BLOB,
                          home_address TEXT,
                          age INTEGER,
                          location TEXT,
                          country TEXT,
                          reset_token TEXT)''')
            
            # Applications table
            c.execute('''CREATE TABLE IF NOT EXISTS applications
                         (id INTEGER PRIMARY KEY,
                          user_id INTEGER,
                          application_data TEXT,
                          status TEXT,
                          submitted_date TEXT,
                          last_modified TEXT,
                          resume BLOB,
                          cover_letter BLOB,
                          FOREIGN KEY (user_id) REFERENCES users(id))''')
            
            # Documents table
            c.execute('''CREATE TABLE IF NOT EXISTS documents
                         (id INTEGER PRIMARY KEY,
                          user_id INTEGER,
                          file_name TEXT,
                          file_data BLOB,
                          file_type TEXT,
                          upload_date TEXT,
                          viewed BOOLEAN DEFAULT 0,
                          FOREIGN KEY (user_id) REFERENCES users(id))''')
            
            # Messages table
            c.execute('''CREATE TABLE IF NOT EXISTS messages
                         (id INTEGER PRIMARY KEY,
                          sender_id INTEGER,
                          recipient_id INTEGER,
                          message TEXT,
                          sent_date TEXT,
                          read_status BOOLEAN DEFAULT 0,
                          FOREIGN KEY (sender_id) REFERENCES users(id),
                          FOREIGN KEY (recipient_id) REFERENCES users(id))''')
            
            # Edit requests table
            c.execute('''CREATE TABLE IF NOT EXISTS edit_requests
                         (id INTEGER PRIMARY KEY,
                          user_id INTEGER,
                          request_reason TEXT,
                          requested_changes TEXT,
                          request_date TEXT,
                          status TEXT DEFAULT 'pending',
                          admin_response TEXT,
                          response_date TEXT,
                          FOREIGN KEY (user_id) REFERENCES users(id))''')
            
            # Screening tests table
            c.execute('''CREATE TABLE IF NOT EXISTS screening_tests
                         (id INTEGER PRIMARY KEY,
                          title TEXT,
                          description TEXT,
                          questions TEXT,
                          duration INTEGER,
                          created_by INTEGER,
                          creation_date TEXT,
                          FOREIGN KEY (created_by) REFERENCES users(id))''')
            
            # Test assignments table
            c.execute('''CREATE TABLE IF NOT EXISTS test_assignments
                         (id INTEGER PRIMARY KEY,
                          test_id INTEGER,
                          candidate_id INTEGER,
                          assigned_date TEXT,
                          start_time TEXT,
                          end_time TEXT,
                          status TEXT,
                          score INTEGER,
                          responses TEXT,
                          FOREIGN KEY (test_id) REFERENCES screening_tests(id),
                          FOREIGN KEY (candidate_id) REFERENCES users(id))''')

            # Positions table
            c.execute('''CREATE TABLE IF NOT EXISTS positions
                         (id INTEGER PRIMARY KEY,
                          title TEXT UNIQUE,
                          description TEXT,
                          required_staff INTEGER,
                          filled_staff INTEGER DEFAULT 0,
                          created_at TEXT)''')
            
            # Activities table
            c.execute('''CREATE TABLE IF NOT EXISTS activities
                         (id INTEGER PRIMARY KEY,
                          activity_type TEXT,
                          details TEXT,
                          timestamp TEXT)''')
            
            # App settings table
            c.execute('''CREATE TABLE IF NOT EXISTS app_settings
                         (key TEXT PRIMARY KEY,
                          value TEXT)''')
            
            # Interviews table
            c.execute('''CREATE TABLE IF NOT EXISTS interviews
                         (id INTEGER PRIMARY KEY,
                          candidate_id INTEGER,
                          date TEXT,
                          time TEXT,
                          type TEXT,
                          role TEXT,
                          dress_code TEXT,
                          stage TEXT,
                          status TEXT,
                          candidate_response TEXT,
                          candidate_note TEXT,
                          FOREIGN KEY (candidate_id) REFERENCES users(id))''')
            
            # Initialize filled_positions in app_settings if not exists
            c.execute("INSERT OR IGNORE INTO app_settings (key, value) VALUES ('filled_positions', '0')")
            
            # Create admin user if not exists
            c.execute("SELECT * FROM users WHERE email = 'admin@admin.com'")
            if not c.fetchone():
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                hashed_password = bcrypt.hashpw('12345'.encode(), bcrypt.gensalt())
                c.execute('''INSERT INTO users 
                             (email, password, first_name, last_name, mobile, role, 
                              registration_date, last_login, last_activity)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                             ('admin@admin.com', hashed_password, 'Admin', 'User', '1234567890', 'admin', now, now, now))
            
            conn.commit()
        return True
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {str(e)}")
        st.error(f"Database initialization error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        st.error(f"An error occurred: {str(e)}")
        return False

def get_user_by_email(email):
    query = "SELECT * FROM users WHERE email = ?"
    result = execute_db_query(query, (email,))
    return dict(result[0]) if result else None

def update_user_activity(user_id, activity_type):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = f"UPDATE users SET {activity_type} = ? WHERE id = ?"
    return execute_db_query(query, (now, user_id), fetch=False)

def get_application(user_id):
    query = """
        SELECT * FROM applications 
        WHERE user_id = ? 
        ORDER BY submitted_date DESC 
        LIMIT 1
    """
    result = execute_db_query(query, (user_id,))
    return dict(result[0]) if result else None

def save_application(user_id, application_data, resume, cover_letter):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = """
        INSERT INTO applications 
        (user_id, application_data, status, submitted_date, last_modified, resume, cover_letter)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    return execute_db_query(
        query, 
        (user_id, json.dumps(application_data), 'submitted', now, now, resume, cover_letter),
        fetch=False
    )

def get_candidate_tests(user_id):
    query = """
        SELECT t.*, ta.status, ta.score, ta.start_time, ta.end_time
        FROM screening_tests t
        JOIN test_assignments ta ON t.id = ta.test_id
        WHERE ta.candidate_id = ?
        ORDER BY ta.assigned_date DESC
    """
    return execute_db_query(query, (user_id,))

def get_messages(user_id):
    query = """
        SELECT m.*, u.first_name || ' ' || u.last_name as sender_name
        FROM messages m
        JOIN users u ON m.sender_id = u.id
        WHERE m.recipient_id = ? OR m.sender_id = ?
        ORDER BY m.sent_date DESC
    """
    return execute_db_query(query, (user_id, user_id))

def save_message(sender_id, recipient_id, message):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = """
        INSERT INTO messages 
        (sender_id, recipient_id, message, sent_date, read_status)
        VALUES (?, ?, ?, ?, ?)
    """
    return execute_db_query(
        query, 
        (sender_id, recipient_id, message, now, False),
        fetch=False
    )

def delete_message(message_id):
    query = "DELETE FROM messages WHERE id = ?"
    return execute_db_query(query, (message_id,), fetch=False)

def get_documents(user_id):
    query = """
        SELECT d.*, u.first_name || ' ' || u.last_name as sender_name
        FROM documents d
        JOIN users u ON d.user_id = u.id
        WHERE d.user_id = ?
        ORDER BY d.upload_date DESC
    """
    return execute_db_query(query, (user_id,))

def save_document(user_id, file_name, file_data, file_type):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = """
        INSERT INTO documents 
        (user_id, file_name, file_data, file_type, upload_date)
        VALUES (?, ?, ?, ?, ?)
    """
    return execute_db_query(
        query,
        (user_id, file_name, file_data, file_type, now),
        fetch=False
    )

def get_screening_tests():
    query = "SELECT * FROM screening_tests ORDER BY creation_date DESC"
    return execute_db_query(query)

def create_screening_test(title, description, questions, duration, created_by):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = """
        INSERT INTO screening_tests 
        (title, description, questions, duration, created_by, creation_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    return execute_db_query(
        query, 
        (title, description, json.dumps(questions), duration, created_by, now),
        fetch=False
    )

def assign_test(test_id, candidate_id):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = """
        INSERT INTO test_assignments 
        (test_id, candidate_id, assigned_date, status)
        VALUES (?, ?, ?, 'assigned')
    """
    return execute_db_query(query, (test_id, candidate_id, now), fetch=False)

def get_test_details(test_id):
    query = "SELECT * FROM screening_tests WHERE id = ?"
    result = execute_db_query(query, (test_id,))
    return dict(result[0]) if result else None

def start_test(test_id, user_id):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = """
        UPDATE test_assignments
        SET status = 'in_progress', start_time = ?
        WHERE test_id = ? AND candidate_id = ?
    """
    return execute_db_query(query, (now, test_id, user_id), fetch=False)

def submit_test(test_id, user_id, responses, score):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = """
        UPDATE test_assignments
        SET status = 'completed', end_time = ?, score = ?, responses = ?
        WHERE test_id = ? AND candidate_id = ?
    """
    return execute_db_query(query, (now, score, json.dumps(responses), test_id, user_id), fetch=False)

def get_pending_edit_requests():
    query = """
        SELECT er.*, u.first_name, u.last_name
        FROM edit_requests er
        JOIN users u ON er.user_id = u.id
        WHERE er.status = 'pending'
        ORDER BY er.request_date DESC
    """
    return execute_db_query(query)

def update_edit_request(request_id, status):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = """
        UPDATE edit_requests
        SET status = ?, response_date = ?
        WHERE id = ?
    """
    return execute_db_query(query, (status, now, request_id), fetch=False)

def submit_edit_request(user_id, reason, changes):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = """
        INSERT INTO edit_requests 
        (user_id, request_reason, requested_changes, request_date, status)
        VALUES (?, ?, ?, ?, 'pending')
    """
    return execute_db_query(query, (user_id, reason, changes, now), fetch=False)

def get_total_candidates():
    query = """
    SELECT COUNT(*) FROM users 
    WHERE role = 'candidate'
    """
    result = execute_db_query(query)
    return result[0]['COUNT(*)'] if result else 0

def get_open_applications():
    query = """
    SELECT COUNT(*) FROM applications 
    WHERE status IN ('under_review', 'interview_scheduled')
    """
    result = execute_db_query(query)
    return result[0]['COUNT(*)'] if result else 0

def get_scheduled_interviews():
    query = """
    SELECT COUNT(*) FROM interviews 
    WHERE status = 'scheduled'
    """
    result = execute_db_query(query)
    return result[0]['COUNT(*)'] if result else 0

def get_filled_positions():
    query = "SELECT SUM(filled_staff) FROM positions"
    result = execute_db_query(query)
    return result[0]['SUM(filled_staff)'] if result else 0

def update_filled_positions(position_id, new_filled_staff):
    query = "UPDATE positions SET filled_staff = ? WHERE id = ?"
    return execute_db_query(query, (new_filled_staff, position_id), fetch=False)

def get_recent_activities(limit=10):
    query = """
    SELECT activity_type, details, timestamp FROM activities
    ORDER BY timestamp DESC
    LIMIT ?
    """
    results = execute_db_query(query, (limit,))
    return [f"{r['activity_type']}: {r['details']} - {r['timestamp']}" for r in results] if results else []

def add_new_position(title, description, required_staff):
    query = "INSERT INTO positions (title, description, required_staff, created_at) VALUES (?, ?, ?, ?)"
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return execute_db_query(query, (title, description, required_staff, now), fetch=False)

def get_all_candidates():
    query = """
    SELECT u.id, u.first_name, u.last_name, u.email, u.registration_date, u.status
    FROM users u
    WHERE u.role = 'candidate'
    """
    results = execute_db_query(query)
    return [
        {
            'id': r['id'],
            'name': f"{r['first_name']} {r['last_name']}",
            'email': r['email'],
            'registration_date': r['registration_date'],
            'status': r['status']
        } for r in results
    ] if results else []

def get_all_applications():
    query = """
    SELECT a.id, u.first_name, u.last_name, a.application_data, a.status, a.submitted_date
    FROM applications a
    JOIN users u ON a.user_id = u.id
    """
    results = execute_db_query(query)
    return [
        {
            'id': r['id'],
            'candidate_name': f"{r['first_name']} {r['last_name']}",
            'position': json.loads(r['application_data']),
            'status': r['status'],
            'submitted_date': r['submitted_date']
        } for r in results
    ] if results else [] 

def get_all_documents():
    query = """
    SELECT d.id, u.first_name, u.last_name, d.file_name, d.file_data, d.file_type, d.upload_date
    FROM documents d
    JOIN users u ON d.user_id = u.id
    """
    results = execute_db_query(query)
    return [
        {
            'id': r['id'],
            'candidate_name': f"{r['first_name']} {r['last_name']}",
            'file_name': r['file_name'],
            'file_data': r['file_data'],
            'document_type': r['file_type'],
            'upload_date': r['upload_date']
        } for r in results
    ] if results else []

def update_user_profile(user_id, profile_data):
    query = """
        UPDATE users
        SET first_name = ?, last_name = ?, mobile = ?, home_address = ?, 
            age = ?, location = ?, country = ?, profile_picture = ?
        WHERE id = ?
    """
    return execute_db_query(
        query,
        (profile_data['first_name'], profile_data['last_name'], profile_data['mobile'],
         profile_data['home_address'], profile_data['age'], profile_data['location'],
         profile_data['country'], profile_data['profile_picture'], user_id),
        fetch=False
    )

def get_user_profile(user_id):
    query = """
        SELECT id, email, first_name, last_name, mobile, role, registration_date,
               profile_picture, home_address, age, location, country
        FROM users
        WHERE id = ?
    """
    result = execute_db_query(query, (user_id,))
    return dict(result[0]) if result else None

def get_user_documents(user_id):
    query = """
        SELECT id, file_name, file_type, upload_date
        FROM documents
        WHERE user_id = ?
        ORDER BY upload_date DESC
    """
    return execute_db_query(query, (user_id,))

def delete_document(document_id, user_id):
    query = """
        DELETE FROM documents
        WHERE id = ? AND user_id = ?
    """
    return execute_db_query(query, (document_id, user_id), fetch=False)

def schedule_interview(candidate_ids, date, time, interview_type, role, dress_code, stage):
    query = """
        INSERT INTO interviews
        (candidate_id, date, time, type, role, dress_code, stage, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'scheduled')
    """
    for candidate_id in candidate_ids:
        execute_db_query(query, (candidate_id, date, time, interview_type, role, dress_code, stage), fetch=False)
    return True

def get_candidate_interviews(candidate_id):
    query = """
        SELECT * FROM interviews
        WHERE candidate_id = ?
        ORDER BY date DESC, time DESC
    """
    return execute_db_query(query, (candidate_id,))

def update_interview_response(interview_id, response, note):
    query = """
        UPDATE interviews
        SET candidate_response = ?, candidate_note = ?
        WHERE id = ?
    """
    return execute_db_query(query, (response, note, interview_id), fetch=False)

def get_all_interviews():
    query = """
        SELECT i.*, u.first_name, u.last_name, u.email
        FROM interviews i
        JOIN users u ON i.candidate_id = u.id
        ORDER BY i.date DESC, i.time DESC
    """
    return execute_db_query(query)

def update_interview_status(interview_id, status):
    query = """
        UPDATE interviews
        SET status = ?
        WHERE id = ?
    """
    return execute_db_query(query, (status, interview_id), fetch=False)

def reschedule_interview(interview_id, new_date, new_time):
    query = """
        UPDATE interviews
        SET date = ?, time = ?, status = 'rescheduled'
        WHERE id = ?
    """
    return execute_db_query(query, (new_date, new_time, interview_id), fetch=False)

def update_application_status(application_id, status):
    query = """
        UPDATE applications
        SET status = ?, last_modified = ?
        WHERE id = ?
    """
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return execute_db_query(query, (status, now, application_id), fetch=False)

def get_candidate_details(candidate_id):
    query = """
        SELECT u.*, a.application_data, a.status as application_status, 
               a.submitted_date as application_submitted_date,
               i.date as interview_date, i.time as interview_time, i.status as interview_status,
               t.score as test_score, t.responses as test_responses
        FROM users u
        LEFT JOIN applications a ON u.id = a.user_id
        LEFT JOIN interviews i ON u.id = i.candidate_id
        LEFT JOIN test_assignments t ON u.id = t.candidate_id
        WHERE u.id = ?
    """
    result = execute_db_query(query, (candidate_id,))
    return dict(result[0]) if result else None

def search_candidates(search_term):
    query = """
        SELECT id, first_name, last_name, email
        FROM users
        WHERE role = 'candidate' AND (first_name LIKE ? OR last_name LIKE ? OR email LIKE ?)
    """
    search_term = f"%{search_term}%"
    return execute_db_query(query, (search_term, search_term, search_term))

def get_all_positions():
    query = "SELECT * FROM positions ORDER BY created_at DESC"
    return execute_db_query(query)

def get_total_applicants():
    query = "SELECT COUNT(*) FROM applications"
    result = execute_db_query(query)
    return result[0]['COUNT(*)'] if result else 0

def get_total_messages():
    query = """
    SELECT COUNT(*) as total,
           SUM(CASE WHEN read_status = 0 THEN 1 ELSE 0 END) as unread
    FROM messages
    """
    result = execute_db_query(query)
    return dict(result[0]) if result else {'total': 0, 'unread': 0}

def get_total_documents():
    query = """
    SELECT COUNT(*) as total,
           SUM(CASE WHEN viewed = 0 THEN 1 ELSE 0 END) as unviewed
    FROM documents
    """
    result = execute_db_query(query)
    return dict(result[0]) if result else {'total': 0, 'unviewed': 0}

def get_login_statistics():
    query = """
    SELECT DATE(last_login) as login_date, COUNT(*) as login_count
    FROM users
    WHERE last_login >= DATE('now', '-7 days')
    GROUP BY DATE(last_login)
    ORDER BY login_date
    """
    results = execute_db_query(query)
    return {r['login_date']: r['login_count'] for r in results} if results else {}

def get_interview_statistics():
    query = """
    SELECT status, COUNT(*) as count
    FROM interviews
    GROUP BY status
    """
    results = execute_db_query(query)
    return {r['status']: r['count'] for r in results} if results else {}

def get_file_data(file_id):
    query = """
    SELECT file_data, file_name, file_type
    FROM documents
    WHERE id = ?
    """
    result = execute_db_query(query, (file_id,))
    return dict(result[0]) if result else None

def update_user_password(user_id, new_password):
    query = "UPDATE users SET password = ? WHERE id = ?"
    return execute_db_query(query, (new_password, user_id), fetch=False)

def update_reset_token(user_id, reset_token):
    query = "UPDATE users SET reset_token = ? WHERE id = ?"
    return execute_db_query(query, (reset_token, user_id), fetch=False)

def get_user_by_reset_token(reset_token):
    query = "SELECT id, email FROM users WHERE reset_token = ?"
    result = execute_db_query(query, (reset_token,))
    return dict(result[0]) if result else None

def clear_reset_token(user_id):
    query = "UPDATE users SET reset_token = NULL WHERE id = ?"
    return execute_db_query(query, (user_id,), fetch=False)

# Additional helper functions can be added here as needed

def log_activity(activity_type, details):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = """
    INSERT INTO activities (activity_type, details, timestamp)
    VALUES (?, ?, ?)
    """
    return execute_db_query(query, (activity_type, details, now), fetch=False)

def get_application_statistics():
    query = """
    SELECT status, COUNT(*) as count
    FROM applications
    GROUP BY status
    """
    results = execute_db_query(query)
    return {r['status']: r['count'] for r in results} if results else {}

def get_user_activity_log(user_id, limit=10):
    query = """
    SELECT activity_type, details, timestamp
    FROM activities
    WHERE details LIKE ?
    ORDER BY timestamp DESC
    LIMIT ?
    """
    results = execute_db_query(query, (f"%user_id: {user_id}%", limit))
    return [dict(r) for r in results] if results else []

def update_app_setting(key, value):
    query = """
    INSERT OR REPLACE INTO app_settings (key, value)
    VALUES (?, ?)
    """
    return execute_db_query(query, (key, value), fetch=False)

def get_app_setting(key):
    query = "SELECT value FROM app_settings WHERE key = ?"
    result = execute_db_query(query, (key,))
    return result[0]['value'] if result else None

# End of database.py

