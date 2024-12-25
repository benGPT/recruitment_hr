import streamlit as st
import bcrypt
from database import get_user_by_email, update_user_activity, update_user_password, update_reset_token, get_user_by_reset_token, clear_reset_token
from datetime import datetime, timedelta
import secrets
import string

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    body {
        font-family: 'Roboto', sans-serif;
        background-color: #f0f8ff;
        color: #333333;
    }

    .stApp {
        background-image: url('https://www.miraclehealthcarerecruitment.co.uk/wp-content/uploads/2023/05/miracle-healthcare-recruitment-home-banner.jpg');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    .auth-container {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        max-width: 400px;
        margin: auto;
        
    }

    .stButton > button {
        background-color: #006400;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        border: none;
        transition: background-color 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #008000;
    }

    .stTextInput > div > div > input {
        border-color: #006400;
        border-radius: 5px;
    }

    h1, h2, h3 {
        color: #006400;
    }
    </style>
    """, unsafe_allow_html=True)

def login_user(email, password):
    user = get_user_by_email(email)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        update_user_activity(user['id'], 'last_login')
        return user
    return None

def register_user(email, password, first_name, last_name, mobile):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_data = {
        'email': email,
        'password': hashed_password,
        'first_name': first_name,
        'last_name': last_name,
        'mobile': mobile,
        'role': 'candidate',
        'registration_date': now,
        'last_login': now,
        'last_activity': now
    }
    from database import execute_db_query
    query = """
    INSERT INTO users (email, password, first_name, last_name, mobile, role, registration_date, last_login, last_activity)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    result = execute_db_query(query, tuple(user_data.values()), fetch=False)
    return result is not None

def check_session_timeout():
    if 'last_activity' not in st.session_state:
        st.session_state.last_activity = datetime.now()
        return False
    
    if datetime.now() - st.session_state.last_activity > timedelta(minutes=30):
        st.warning("Your session has expired. Please log in again.")
        st.session_state.clear()
        return True
    
    return False

def update_last_activity():
    st.session_state.last_activity = datetime.now()

def generate_reset_token():
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))

def send_reset_email(email, reset_token):
    # In a real application, you would send an email here
    # For this example, we'll just print the reset link
    reset_link = f"http://yourdomain.com/reset_password?token={reset_token}"
    print(f"Password reset link for {email}: {reset_link}")

def initiate_password_reset(email):
    user = get_user_by_email(email)
    if user:
        reset_token = generate_reset_token()
        update_reset_token(user['id'], reset_token)
        send_reset_email(email, reset_token)
        return True
    return False

def reset_password(reset_token, new_password):
    user = get_user_by_reset_token(reset_token)
    if user:
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        if update_user_password(user['id'], hashed_password):
            clear_reset_token(user['id'])
            return True
    return False

