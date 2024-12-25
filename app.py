import streamlit as st
from database import init_db
from auth import load_css, check_session_timeout, update_last_activity
from pages import (
    show_landing_page,
    show_login_page,
    show_registration_page,
    show_admin_dashboard,
    show_candidate_dashboard,
    show_password_recovery_page
)

def main():
    st.set_page_config(
        page_title="Miracle Healthcare Recruitment",
        page_icon="https://www.miraclehealthcarerecruitment.co.uk/wp-content/uploads/2023/05/cropped-favicon-32x32.png",
        layout="wide"
    )

    # Initialize the database
    if not init_db():
        st.error("Failed to initialize database. Please check the logs.")
        return

    # Custom theme and CSS
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    :root {
        --primary-color: #006400;
        --secondary-color: #8B4513;
        --accent-color-1: #8B0000;
        --accent-color-2: #4B0082;
        --text-color: #333333;
        --background-color: #f0f918ff;
    }

    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
        color: var(--text-color);
    }

    .stApp {
        background-color: var(--background-color);
    }

    .stButton > button {
        background-color: var(--primary-color);
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: var(--secondary-color);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .stTextInput > div > div > input {
        border-color: var(--primary-color);
        border-radius: 5px;
        color: var(--text-color);
        background-color: white;
    }

    h1, h2, h3 {
        color: var(--primary-color);
    }

    .sidebar .sidebar-content {
        background-color: var(--secondary-color);
        color: white;
    }

    .sidebar .sidebar-content .stButton > button {
        width: 100%;
        margin-bottom: 0.5rem;
        background-color: var(--accent-color-1);
    }

    .card {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .accent-text {
        color: var(--accent-color-1);
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    load_css()

    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = 'landing'

    # Route to appropriate page
    if 'user' in st.session_state:
        if check_session_timeout():
            return
        update_last_activity()
        if st.session_state.user['role'] == 'admin':
            show_admin_dashboard()
        else:
            show_candidate_dashboard()
    elif st.session_state.page == 'login':
        show_login_page()
    elif st.session_state.page == 'register':
        show_registration_page()
    elif st.session_state.page == 'password_recovery':
        show_password_recovery_page()
    else:
        show_landing_page()

if __name__ == "__main__":
    main()

