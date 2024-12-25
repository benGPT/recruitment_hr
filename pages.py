import streamlit as st
from auth import login_user, register_user, initiate_password_reset, reset_password
from database import (
    get_application,
    save_application,
    get_candidate_tests,
    get_messages,
    save_message,
    delete_message,
    get_documents,
    save_document,
    get_screening_tests,
    create_screening_test,
    assign_test,
    get_test_details,
    start_test,
    submit_test,
    get_pending_edit_requests,
    update_edit_request,
    submit_edit_request,
    get_total_candidates,
    get_open_applications,
    get_scheduled_interviews,
    get_filled_positions,
    update_filled_positions,
    get_recent_activities,
    add_new_position,
    get_all_candidates,
    get_all_applications,
    get_all_documents,
    update_user_profile,
    get_user_profile,
    get_user_documents,
    delete_document,
    schedule_interview,
    get_candidate_interviews,
    update_interview_response,
    get_all_interviews,
    update_interview_status,
    reschedule_interview,
    update_application_status,
    get_candidate_details,
    search_candidates,
    get_all_positions,
    get_total_applicants,
    get_total_messages,
    get_total_documents,
    get_login_statistics,
    get_interview_statistics,
    get_file_data,
    get_application_statistics,
    get_user_activity_log,
    update_app_setting,
    get_app_setting
)
from datetime import datetime, timedelta
import json
import io
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px
import base64

def show_landing_page():

    st.markdown("""
    <style>
    .hero {
        background-image: url('https://www.miraclehealthcarerecruitment.co.uk/wp-content/uploads/2023/05/miracle-healthcare-recruitment-home-banner.jpg');
        background-size: cover;
        background-position: center;
        color: blue;
        text-align: center;
        padding: 4rem 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .hero h1 {
        font-size: 5rem;
        margin-bottom: 2rem;
        color: black;
        text-shadow: 5px 2px 4px rgba(0,0,0,0.5);
    }
    .hero p {
        font-size: 1.7rem;
        margin-bottom: 0rem;
        text-align: right;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
                
    }
    .cta-button {
        background-color: var(--accent-color-1);
        color: white;
        padding: 0.75rem 1.5rem;
        font-size: 1.1rem;
        border-radius: 5px;
        text-decoration: none;
        transition: background-color 0.3s ease;
    }
    .cta-button:hover {
        background-color: var(--accent-color-2);
    }
    .feature-card {
        background-color: rgba(77, 255, 0, 0.1);
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 1.5rem;
        text-align: center;
        height: 100%;
    }
    .feature-card img {
        width: 80px;
        height: 80px;
        margin-bottom: 1rem;
    }
    .feature-card h3 {
        color: var(--accent-color-1);
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero">
        <h1>Welcome to Miracle Healthcare Recruitment</h1>
        <p>Your Gateway to Exceptional Healthcare Careers</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("LOGIN/SIGNUP TO EMPLOYMENT"):
        st.session_state.page = 'login'
        st.rerun()



    st.markdown("<h2 style='text-align: center; margin-bottom: 2rem;'>Our Services</h2>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <img src="https://www.miraclehealthcarerecruitment.co.uk/wp-content/uploads/2023/05/expertise.png" alt="Permanent Recruitment">
            <h3>Permanent Recruitment</h3>
            <p>Find your perfect long-term role in healthcare</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <img src="https://www.miraclehealthcarerecruitment.co.uk/wp-content/uploads/2023/05/personalized.png" alt="Temporary Staffing">
            <h3>Temporary Staffing</h3>
            <p>Flexible healthcare positions to suit your needs</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <img src="https://www.miraclehealthcarerecruitment.co.uk/wp-content/uploads/2023/05/compliance.png" alt="Executive Search">
            <h3>Executive Search</h3>
            <p>Connecting top talent with leadership roles</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="feature-card">
            <img src="https://www.miraclehealthcarerecruitment.co.uk/wp-content/uploads/2023/05/support.png" alt="Compliance Support">
            <h3>Compliance Support</h3>
            <p>Ensuring all placements meet industry standards</p>
        </div>
        """, unsafe_allow_html=True)

        
    if st.button("LOGIN INTO MIRACLE HR"):
        st.session_state.page = 'login'
        st.rerun()


    st.markdown("<h2 style='text-align: center; margin-top: 3rem; margin-bottom: 2rem;'>Why Choose Miracle Healthcare Recruitment?</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
            <h3>For Candidates</h3>
            <ul>
                <li>Access to top healthcare positions</li>
                <li>Personalized career guidance</li>
                <li>Ongoing support throughout your job search</li>
                <li>Exclusive job opportunities</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <h3>For Employers</h3>
            <ul>
                <li>Access to a pool of qualified healthcare professionals</li>
                <li>Tailored recruitment solutions</li>
                <li>Rigorous candidate screening process</li>
                <li>Ongoing support and follow-up</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def show_login_page():
    st.markdown("""
    <style>
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
    .auth-container h1 {
        color: #006400;
    }
    .stButton > button {
        background-color: #006400;
        color: white;
    }
    .stButton > button:hover {
        background-color: #008000;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.image("https://www.miraclehealthcarerecruitment.co.uk/wp-content/uploads/2023/05/cropped-Miracle-Healthcare-Recruitment-Logo-1.png", width=200)
    st.title("Login")
    
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            user = login_user(email, password)
            if user:
                st.session_state.user = user
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid email or password")
    
    if st.button("Don't have an account? Register here"):
        st.session_state.page = 'register'
        st.rerun()
    
    if st.button("Forgot Password?"):
        st.session_state.page = 'password_recovery'
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

def show_registration_page():
    st.markdown("""
    <style>
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
    .auth-container h1 {
        color: #006400;
    }
    .stButton > button {
        background-color: #006400;
        color: white;
    }
    .stButton > button:hover {
        background-color: #008000;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.image("https://www.miraclehealthcarerecruitment.co.uk/wp-content/uploads/2023/05/cropped-Miracle-Healthcare-Recruitment-Logo-1.png", width=200)
    st.title("Register")
    
    with st.form("registration_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        mobile = st.text_input("Mobile")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Register")
        
        if submitted:
            if password != confirm_password:
                st.error("Passwords do not match")
            elif register_user(email, password, first_name, last_name, mobile):
                st.success("Registered successfully! Please log in.")
                st.session_state.page = 'login'
                st.rerun()
            else:
                st.error("Registration failed. Please try again.")
    
    if st.button("Already have an account? Login here"):
        st.session_state.page = 'login'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def show_password_recovery_page():
    st.title("Password Recovery")

    email = st.text_input("Enter your email address")
    if st.button("Send Reset Link"):
        if initiate_password_reset(email):
            st.success("Password reset link has been sent to your email. Please check your inbox.")
        else:
            st.error("Email not found. Please check the email address and try again.")

    st.markdown("---")
    st.subheader("Reset Password")
    reset_token = st.text_input("Enter Reset Token")
    new_password = st.text_input("Enter New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")

    if st.button("Reset Password"):
        if new_password != confirm_password:
            st.error("Passwords do not match. Please try again.")
        elif reset_password(reset_token, new_password):
            st.success("Password has been reset successfully. You can now log in with your new password.")
            st.session_state.page = 'login'
        else:
            st.error("Invalid or expired reset token. Please request a new password reset.")

    if st.button("Back to Login"):
        st.session_state.page = 'login'
        st.rerun()

def show_admin_dashboard():
    st.title("Admin Dashboard")
    st.write("Welcome to the admin dashboard. Here you can manage users, applications, and other administrative tasks.")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    admin_page = st.sidebar.radio("Go to", ["Overview", "Candidates", "Applications", "Interviews", "Positions", "Documents", "Messages", "Screening Tests"])

    if admin_page == "Overview":
        show_admin_overview()
    elif admin_page == "Candidates":
        show_admin_candidates()
    elif admin_page == "Applications":
        show_admin_applications()
    elif admin_page == "Interviews":
        show_admin_interviews()
    elif admin_page == "Positions":
        show_admin_positions()
    elif admin_page == "Documents":
        show_admin_documents()
    elif admin_page == "Messages":
        show_admin_messages()
    elif admin_page == "Screening Tests":
        show_admin_screening_tests()

def show_admin_overview():
    st.header("Overview")
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Candidates", get_total_candidates())
    col2.metric("Open Applications", get_open_applications())
    col3.metric("Scheduled Interviews", get_scheduled_interviews())
    col4.metric("Filled Positions", get_filled_positions())

    # Recent Activities
    st.subheader("Recent Activities")
    activities = get_recent_activities()
    for activity in activities:
        st.write(activity)

    # Login Statistics
    st.subheader("Login Statistics (Last 7 Days)")
    login_stats = get_login_statistics()
    fig = go.Figure(data=go.Bar(x=list(login_stats.keys()), y=list(login_stats.values())))
    fig.update_layout(title="Daily Logins", xaxis_title="Date", yaxis_title="Number of Logins")
    st.plotly_chart(fig)

    # Interview Statistics
    st.subheader("Interview Statistics")
    interview_stats = get_interview_statistics()
    fig = px.pie(values=list(interview_stats.values()), names=list(interview_stats.keys()), title="Interview Status Distribution")
    st.plotly_chart(fig)

    # Application Statistics
    st.subheader("Application Statistics")
    application_stats = get_application_statistics()
    fig = px.pie(values=list(application_stats.values()), names=list(application_stats.keys()), title="Application Status Distribution")
    st.plotly_chart(fig)

    # Positions Management
    st.subheader("Positions Management")
    with st.form("new_position"):
        title = st.text_input("Position Title")
        description = st.text_area("Position Description")
        required_staff = st.number_input("Required Staff", min_value=1, value=1)
        if st.form_submit_button("Add New Position"):
            if add_new_position(title, description, required_staff):
                st.success("New position added successfully!")
            else:
                st.error("Failed to add new position. Please try again.")

    # Update Filled Positions
    st.subheader("Update Filled Positions")
    positions = get_all_positions()
    for position in positions:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**{position['title']}**")
        with col2:
            st.write(f"Required: {position['required_staff']}")
        with col3:
            new_filled = st.number_input(f"Filled ({position['filled_staff']})", min_value=0, value=position['filled_staff'], key=f"filled_{position['id']}")
            if new_filled != position['filled_staff']:
                if update_filled_positions(position['id'], new_filled):
                    st.success(f"Updated filled staff for {position['title']}")
                else:
                    st.error(f"Failed to update filled staff for {position['title']}")

def show_admin_candidates():
    st.header("Candidate Management")
    
    # Search functionality
    search_term = st.text_input("Search Candidates", "")
    if search_term:
        candidates = search_candidates(search_term)
    else:
        candidates = get_all_candidates()

    # Display candidates
    for candidate in candidates:
        with st.expander(f"{candidate['name']} - {candidate['email']}"):
            st.write(f"Registration Date: {candidate['registration_date']}")
            st.write(f"Status: {candidate['status']}")
            if st.button(f"View Details for {candidate['name']}"):
                show_candidate_details(candidate['id'])

def show_candidate_details(candidate_id):
    details = get_candidate_details(candidate_id)
    st.subheader(f"Details for {details['first_name']} {details['last_name']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Email: {details['email']}")
        st.write(f"Mobile: {details['mobile']}")
        st.write(f"Registration Date: {details['registration_date']}")
        st.write(f"Age: {details['age']}")
        st.write(f"Location: {details['location']}")
        st.write(f"Country: {details['country']}")
    
    with col2:
        if details['profile_picture']:
            st.image(details['profile_picture'], caption="Profile Picture", use_column_width=True)
        else:
            st.write("No profile picture uploaded")
    
    if details['application_status']:
        st.subheader("Application Information")
        st.write(f"Application Status: {details['application_status']}")
        st.write(f"Application Submitted: {details['application_submitted_date']}")
        st.write("Application Data:")
        st.json(json.loads(details['application_data']))
    
    if details['interview_date']:
        st.subheader("Interview Information")
        st.write(f"Interview Scheduled: {details['interview_date']} at {details['interview_time']}")
        st.write(f"Interview Status: {details['interview_status']}")
    
    if details['test_score'] is not None:
        st.subheader("Screening Test Information")
        st.write(f"Test Score: {details['test_score']}")
        st.write("Test Responses:")
        st.json(json.loads(details['test_responses']))
    
    st.subheader("Documents")
    documents = get_user_documents(candidate_id)
    for doc in documents:
        st.write(f"{doc['file_name']} - {doc['file_type']} - {doc['upload_date']}")
        if st.button(f"View {doc['file_name']}"):
            file_data = get_file_data(doc['id'])
            if file_data:
                file_type = file_data['file_type']
                if file_type.startswith('image'):
                    st.image(file_data['file_data'])
                elif file_type == 'application/pdf':
                    base64_pdf = base64.b64encode(file_data['file_data']).decode('utf-8')
                    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
                    st.markdown(pdf_display, unsafe_allow_html=True)
                else:
                    st.download_button("Download File", file_data['file_data'], file_name=file_data['file_name'])

    st.subheader("Messages")
    messages = get_messages(candidate_id)
    for message in messages:
        st.write(f"From: {message['sender_name']} - {message['sent_date']}")
        st.write(message['message'])
        st.markdown("---")

def show_admin_applications():
    st.header("Application Management")
    
    applications = get_all_applications()
    for app in applications:
        with st.expander(f"{app['candidate_name']} - {app['position']}"):
            st.write(f"Status: {app['status']}")
            st.write(f"Submitted: {app['submitted_date']}")
            new_status = st.selectbox("Update Status", ["under_review", "interview_scheduled", "rejected", "accepted"], key=f"status_{app['id']}")
            if st.button("Update", key=f"update_{app['id']}"):
                if update_application_status(app['id'], new_status):
                    st.success("Application status updated successfully!")
                else:
                    st.error("Failed to update application status. Please try again.")
            
            if st.button("View Full Application", key=f"view_{app['id']}"):
                show_full_application(app['id'])

def show_full_application(application_id):
    application = get_application(application_id)
    if application:
        st.subheader("Full Application Details")
        st.json(json.loads(application['application_data']))
        
        if application['resume']:
            st.download_button("Download Resume", application['resume'], file_name="resume.pdf")
        
        if application['cover_letter']:
            st.download_button("Download Cover Letter", application['cover_letter'], file_name="cover_letter.pdf")
    else:
        st.error("Application not found")

def show_admin_interviews():
    st.header("Interview Management")
    
    # Schedule new interview
    st.subheader("Schedule New Interview")
    with st.form("schedule_interview"):
        candidates = get_all_candidates()
        candidate_options = {f"{c['name']} ({c['email']})": c['id'] for c in candidates}
        selected_candidates = st.multiselect("Select Candidates", options=list(candidate_options.keys()))
        date = st.date_input("Interview Date")
        time = st.time_input("Interview Time")
        interview_type = st.selectbox("Interview Type", ["In-person", "Phone", "Video"])
        role = st.text_input("Role")
        dress_code = st.text_input("Dress Code")
        stage = st.selectbox("Interview Stage", ["First", "Second", "Final"])
        
        if st.form_submit_button("Schedule Interview"):
            candidate_ids = [candidate_options[c] for c in selected_candidates]
            if schedule_interview(candidate_ids, date.strftime('%Y-%m-%d'), time.strftime('%H:%M:%S'), interview_type, role, dress_code, stage):
                st.success("Interview scheduled successfully!")
            else:
                st.error("Failed to schedule interview. Please try again.")
    
    # Manage existing interviews
    st.subheader("Manage Interviews")
    interviews = get_all_interviews()
    for interview in interviews:
        with st.expander(f"{interview['first_name']} {interview['last_name']} - {interview['date']} {interview['time']}"):
            st.write(f"Type: {interview['type']}")
            st.write(f"Role: {interview['role']}")
            st.write(f"Status: {interview['status']}")
            new_status = st.selectbox("Update Status", ["scheduled", "completed", "cancelled", "postponed"], key=f"status_{interview['id']}")
            if st.button("Update Status", key=f"update_status_{interview['id']}"):
                if update_interview_status(interview['id'], new_status):
                    st.success("Interview status updated successfully!")
                else:
                    st.error("Failed to update interview status. Please try again.")
            
            new_date = st.date_input("Reschedule Date", key=f"date_{interview['id']}")
            new_time = st.time_input("Reschedule Time", key=f"time_{interview['id']}")
            if st.button("Reschedule", key=f"reschedule_{interview['id']}"):
                if reschedule_interview(interview['id'], new_date.strftime('%Y-%m-%d'), new_time.strftime('%H:%M:%S')):
                    st.success("Interview rescheduled successfully!")
                else:
                    st.error("Failed to reschedule interview. Please try again.")

def show_admin_positions():
    st.header("Position Management")
    
    # Add new position
    st.subheader("Add New Position")
    with st.form("new_position"):
        title = st.text_input("Position Title")
        description = st.text_area("Position Description")
        required_staff = st.number_input("Required Staff", min_value=1, value=1)
        if st.form_submit_button("Add Position"):
            if add_new_position(title, description, required_staff):
                st.success("New position added successfully!")
            else:
                st.error("Failed to add new position. Please try again.")

    # Display and manage existing positions
    st.subheader("Existing Positions")
    positions = get_all_positions()
    for position in positions:
        with st.expander(f"{position['title']} (Required: {position['required_staff']}, Filled: {position['filled_staff']})"):
            st.write(f"Description: {position['description']}")
            new_filled = st.number_input("Update Filled Staff", min_value=0, value=position['filled_staff'], key=f"filled_{position['id']}")
            if st.button("Update", key=f"update_{position['id']}"):
                if update_filled_positions(position['id'], new_filled):
                    st.success("Position updated successfully!")
                else:
                    st.error("Failed to update position. Please try again.")

def show_admin_documents():
    st.header("Document Management")
    
    documents = get_all_documents()
    for doc in documents:
        with st.expander(f"{doc['candidate_name']} - {doc['file_name']}"):
            st.write(f"Type: {doc['document_type']}")
            st.write(f"Uploaded: {doc['upload_date']}")
            if st.button("View Document", key=f"view_{doc['id']}"):
                file_data = get_file_data(doc['id'])
                if file_data:
                    file_type = file_data['file_type']
                    if file_type.startswith('image'):
                        st.image(file_data['file_data'])
                    elif file_type == 'application/pdf':
                        base64_pdf = base64.b64encode(file_data['file_data']).decode('utf-8')
                        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
                        st.markdown(pdf_display, unsafe_allow_html=True)
                    else:
                        st.download_button("Download File", file_data['file_data'], file_name=file_data['file_name'])

def show_admin_messages():
    st.header("Message Management")
    
    # Display all messages
    messages = get_messages(None)  # None to get all messages
    for message in messages:
        with st.expander(f"From: {message['sender_name']} - To: {message['recipient_name']} - {message['sent_date']}"):
            st.write(message['message'])
            if st.button("Delete", key=f"delete_{message['id']}"):
                if delete_message(message['id']):
                    st.success("Message deleted successfully!")
                    st.rerun()
                else:
                    st.error("Failed to delete message. Please try again.")
    
    # Send a new message
    st.subheader("Send a New Message")
    candidates = get_all_candidates()
    recipient = st.selectbox("Select Recipient", [f"{c['name']} ({c['email']})" for c in candidates])
    message_content = st.text_area("Message")
    if st.button("Send Message"):
        recipient_id = next(c['id'] for c in candidates if f"{c['name']} ({c['email']})" == recipient)
        if save_message(st.session_state.user['id'], recipient_id, message_content):
            st.success("Message sent successfully!")
            st.rerun()
        else:
            st.error("Failed to send message. Please try again.")

def show_admin_screening_tests():
    st.header("Screening Test Management")
    
    # Create new screening test
    st.subheader("Create New Screening Test")
    with st.form("new_test"):
        title = st.text_input("Test Title")
        description = st.text_area("Test Description")
        duration = st.number_input("Test Duration (minutes)", min_value=1, value=60)
        num_questions = st.number_input("Number of Questions", min_value=1, value=5)
        
        questions = []
        for i in range(num_questions):
            st.write(f"Question {i+1}")
            question_text = st.text_input(f"Question {i+1} Text", key=f"q{i}")
            question_type = st.selectbox(f"Question {i+1} Type", ["Multiple Choice", "Text"], key=f"qt{i}")
            if question_type == "Multiple Choice":
                options = st.text_input(f"Options (comma-separated)", key=f"qo{i}")
                correct_answer = st.text_input(f"Correct Answer", key=f"qa{i}")
                questions.append({
                    "text": question_text,
                    "type": "multiple_choice",
                    "options": options.split(","),
                    "correct_answer": correct_answer
                })
            else:
                questions.append({
                    "text": question_text,
                    "type": "text"
                })
        
        if st.form_submit_button("Create Test"):
            if create_screening_test(title, description, questions, duration, st.session_state.user['id']):
                st.success("Screening test created successfully!")
            else:
                st.error("Failed to create screening test. Please try again.")
    
    # Manage existing tests
    st.subheader("Existing Screening Tests")
    tests = get_screening_tests()
    for test in tests:
        with st.expander(f"{test['title']} - Created on {test['creation_date']}"):
            st.write(f"Description: {test['description']}")
            st.write(f"Duration: {test['duration']} minutes")
            st.write("Questions:")
            for i, question in enumerate(json.loads(test['questions'])):
                st.write(f"Q{i+1}: {question['text']}")
            
            # Assign test to candidates
            candidates = get_all_candidates()
            selected_candidates = st.multiselect("Assign to Candidates", [f"{c['name']} ({c['email']})" for c in candidates])
            if st.button("Assign Test", key=f"assign_{test['id']}"):
                for candidate in selected_candidates:
                    candidate_id = next(c['id'] for c in candidates if f"{c['name']} ({c['email']})" == candidate)
                    if assign_test(test['id'], candidate_id):
                        st.success(f"Test assigned to {candidate}")
                    else:
                        st.error(f"Failed to assign test to {candidate}")

def show_candidate_dashboard():
    st.title(f"Welcome, {st.session_state.user['first_name']}!")
    st.write("Here you can manage your profile, applications, and messages.")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    candidate_page = st.sidebar.radio("Go to", ["Profile", "Application", "Messages", "Documents", "Interviews", "Tests"])

    # Company contact details in the sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("Contact Us")
    st.sidebar.write("Phone: +44 123 456 7890")
    st.sidebar.write("Email: info@miraclehealthcare.co.uk")
    st.sidebar.write("Website: www.miraclehealthcarerecruitment.co.uk")

    if candidate_page == "Profile":
        show_candidate_profile()
    elif candidate_page == "Application":
        show_candidate_application()
    elif candidate_page == "Messages":
        show_candidate_messages()
    elif candidate_page == "Documents":
        show_candidate_documents()
    elif candidate_page == "Interviews":
        show_candidate_interviews()
    elif candidate_page == "Tests":
        show_candidate_tests()

def show_candidate_profile():
    st.header("Your Profile")
    
    user_id = st.session_state.user['id']
    profile = get_user_profile(user_id)
    
    with st.form("update_profile"):
        col1, col2 = st.columns(2)
        with col1:
            
            if profile['profile_picture']:
                image = Image.open(io.BytesIO(profile['profile_picture']))
                st.image(image, caption="Profile Picture", use_column_width=True)
            else:
                st.info("No profile picture uploaded")

            first_name = st.text_input("First Name", value=profile['first_name'])
            last_name = st.text_input("Last Name", value=profile['last_name'])
            email = st.text_input("Email", value=profile['email'], disabled=True)
            mobile = st.text_input("Mobile", value=profile['mobile'], disabled=True)
            age = st.number_input("Age", value=profile['age'] if profile['age'] else 0)
        with col2:
            home_address = st.text_input("Home Address", value=profile['home_address'])
            location = st.text_input("Location", value=profile['location'])
            country = st.text_input("Country", value=profile['country'])
            registration_date = st.text_input("Registration Date", value=profile['registration_date'], disabled=True)
        
        uploaded_file = st.file_uploader("Choose a profile picture", type=["jpg", "png", "jpeg"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True,  width=50)
        
        if st.form_submit_button("Update Profile"):
            profile_data = {
                'first_name': first_name,
                'last_name': last_name,
                'mobile': mobile,
                'home_address': home_address,
                'age': age,
                'location': location,
                'country': country,
                'profile_picture': uploaded_file.getvalue() if uploaded_file else profile['profile_picture']
            }
            if update_user_profile(user_id, profile_data):
                st.success("Profile updated successfully!")
            else:
                st.error("Failed to update profile. Please try again.")
    
    # Edit Request for Email and Mobile
    st.subheader("Request to Edit Email or Mobile")
    edit_type = st.radio("Select what you want to edit", ["Email", "Mobile"])
    new_value = st.text_input(f"New {edit_type}")
    reason = st.text_area("Reason for change")
    if st.button("Submit Edit Request"):
        if submit_edit_request(user_id, f"Change {edit_type}", f"New {edit_type}: {new_value}\nReason: {reason}"):
            st.success("Edit request submitted successfully!")
        else:
            st.error("Failed to submit edit request. Please try again.")

def show_candidate_application():
    st.header("Your Application")
    
    user_id = st.session_state.user['id']
    application = get_application(user_id)
    
    if application:
        st.write(f"Status: {application['status']}")
        st.write(f"Submitted: {application['submitted_date']}")
        st.json(json.loads(application['application_data']))
        
        if st.button("Request to Edit Application"):
            reason = st.text_area("Reason for editing")
            if submit_edit_request(user_id, "Edit Application", reason):
                st.success("Edit request submitted successfully!")
            else:
                st.error("Failed to submit edit request. Please try again.")
    else:
        st.write("You haven't submitted an application yet.")
        
        with st.form("submit_application"):
            st.subheader("Healthcare Professional Application Form")
            
            # Personal Information
            st.write("Personal Information")
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone Number")
            address = st.text_area("Home Address")
            dob = st.date_input("Date of Birth")
            
            # Professional Information
            st.write("Professional Information")
            position = st.selectbox("Position Applying For", ["Registered Nurse", "Doctor", "Physiotherapist", "Occupational Therapist", "Healthcare Assistant", "Other"])
            if position == "Other":
                other_position = st.text_input("Please specify")
            
            years_experience = st.number_input("Years of Experience", min_value=0, max_value=50)
            current_employer = st.text_input("Current Employer")
            
            # Education
            st.write("Education")
            highest_degree = st.selectbox("Highest Degree Obtained", ["High School", "Bachelor's", "Master's", "Ph.D.", "Other"])
            institution = st.text_input("Institution Name")
            graduation_year = st.number_input("Year of Graduation", min_value=1950, max_value=datetime.now().year)
            
            # Certifications
            st.write("Certifications")
            certifications = st.text_area("List your relevant certifications (one per line)")
            
            # Skills
            st.write("Skills")
            skills = st.text_area("List your key skills (one per line)")
            
            # Work Authorization
            st.write("Work Authorization")
            work_auth = st.radio("Are you authorized to work in the UK?", ("Yes", "No"))
            if work_auth == "Yes":
                visa_type = st.selectbox("Visa Type", ["British Citizen", "EU Settlement Scheme", "Skilled Worker Visa", "Health and Care Worker Visa", "Other"])
            
            # References
            st.write("References")
            ref1_name = st.text_input("Reference 1 Name")
            ref1_relation = st.text_input("Reference 1 Relationship")
            ref1_contact = st.text_input("Reference 1 Contact Information")
            
            ref2_name = st.text_input("Reference 2 Name")
            ref2_relation = st.text_input("Reference 2 Relationship")
            ref2_contact = st.text_input("Reference 2 Contact Information")
            
            # Additional Information
            st.write("Additional Information")
            start_date = st.date_input("Earliest Start Date")
            preferred_schedule = st.multiselect("Preferred Work Schedule", ["Full-time", "Part-time", "Weekends", "Nights"])
            willing_to_relocate = st.radio("Are you willing to relocate?", ("Yes", "No"))
            
            # File Uploads
            resume = st.file_uploader("Upload your resume (PDF)", type="pdf")
            cover_letter = st.file_uploader("Upload your cover letter (PDF)", type="pdf")
            
            if st.form_submit_button("Submit Application"):
                if not (first_name and last_name and email and phone and position and resume and cover_letter):
                    st.error("Please fill in all required fields and upload all required documents.")
                else:
                    application_data = {
                        'personal_info': {
                            'first_name': first_name,
                            'last_name': last_name,
                            'email': email,
                            'phone': phone,
                            'address': address,
                            'dob': str(dob)
                        },
                        'professional_info': {
                            'position': position if position != "Other" else other_position,
                            'years_experience': years_experience,
                            'current_employer': current_employer
                        },
                        'education': {
                            'highest_degree': highest_degree,
                            'institution': institution,
                            'graduation_year': graduation_year
                        },
                        'certifications': certifications.split('\n'),
                        'skills': skills.split('\n'),
                        'work_authorization': {
                            'authorized': work_auth == "Yes",
                            'visa_type': visa_type if work_auth == "Yes" else None
                        },
                        'references': [
                            {'name': ref1_name, 'relation': ref1_relation, 'contact': ref1_contact},
                            {'name': ref2_name, 'relation': ref2_relation, 'contact': ref2_contact}
                        ],
                        'additional_info': {
                            'start_date': str(start_date),
                            'preferred_schedule': preferred_schedule,
                            'willing_to_relocate': willing_to_relocate == "Yes"
                        }
                    }
                    if save_application(user_id, application_data, resume.getvalue(), cover_letter.getvalue()):
                        st.success("Application submitted successfully!")
                    else:
                        st.error("Failed to submit application. Please try again.")

def show_candidate_messages():
    st.header("Your Messages")
    
    user_id = st.session_state.user['id']
    messages = get_messages(user_id)
    
    for message in messages:
        with st.expander(f"From: {message['sender_name']} - {message['sent_date']}"):
            st.write(message['message'])
            if st.button("Delete", key=f"delete_{message['id']}"):
                if delete_message(message['id']):
                    st.success("Message deleted successfully!")
                    st.rerun()
                else:
                    st.error("Failed to delete message. Please try again.")
    
    st.subheader("Send a Message")
    recipient = st.text_input("Recipient Email")
    message_content = st.text_area("Message")
    if st.button("Send"):
        if save_message(user_id, recipient, message_content):
            st.success("Message sent successfully!")
            st.empty()  # Clear the input fields
        else:
            st.error("Failed to send message. Please try again.")

def show_candidate_documents():
    st.header("Your Documents")
    
    user_id = st.session_state.user['id']
    documents = get_user_documents(user_id)
    
    for doc in documents:
        with st.expander(f"{doc['file_name']} - {doc['upload_date']}"):
            st.write(f"Type: {doc['file_type']}")
            if st.button("Delete", key=f"delete_{doc['id']}"):
                if delete_document(doc['id'], user_id):
                    st.success("Document deleted successfully!")
                    st.rerun()
                else:
                    st.error("Failed to delete document. Please try again.")
    
    st.subheader("Upload New Document")
    file_type = st.selectbox("Document Type", [
        "Degree Certificate", "Other Certificate", "Passport Photograph",
        "Facial Expression Video", "Resume", "Government ID", "Address Proof",
        "Job Experience Evidence"
    ])
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "doc", "docx", "jpg", "png", "mp4"])
    if uploaded_file is not None:
        file_size = uploaded_file.size / (1024 * 1024)  # Convert to MB
        if file_size > 5:
            st.error("File size exceeds 5MB limit. Please upload a smaller file.")
        else:
            if st.button("Upload"):
                if save_document(user_id, uploaded_file.name, uploaded_file.getvalue(), file_type):
                    st.success("Document uploaded successfully!")
                else:
                    st.error("Failed to upload document. Please try again.")

def show_candidate_interviews():
    st.header("Your Interviews")
    
    user_id = st.session_state.user['id']
    interviews = get_candidate_interviews(user_id)
    
    for interview in interviews:
        with st.expander(f"{interview['date']} {interview['time']} - {interview['type']}"):
            st.write(f"Role: {interview['role']}")
            st.write(f"Dress Code: {interview['dress_code']}")
            st.write(f"Stage: {interview['stage']}")
            st.write(f"Status: {interview['status']}")
            
            if interview['status'] == 'scheduled':
                response = st.radio("Will you attend?", ["Yes", "No", "Reschedule Request"], key=f"response_{interview['id']}")
                note = st.text_area("Additional Notes", key=f"note_{interview['id']}")
                if st.button("Submit Response", key=f"submit_{interview['id']}"):
                    if update_interview_response(interview['id'], response, note):
                        st.success("Response submitted successfully!")
                    else:
                        st.error("Failed to submit response. Please try again.")

def show_candidate_tests():
    st.header("Your Tests")
    
    user_id = st.session_state.user['id']
    tests = get_candidate_tests(user_id)
    
    for test in tests:
        with st.expander(f"{test['title']} - {test['status']}"):
            st.write(f"Description: {test['description']}")
            st.write(f"Duration: {test['duration']} minutes")
            
            if test['status'] == 'assigned':
                if st.button("Start Test", key=f"start_{test['id']}"):
                    if start_test(test['id'], user_id):
                        st.success("Test started. Good luck!")
                        st.rerun()
                    else:
                        st.error("Failed to start test. Please try again.")
            elif test['status'] == 'in_progress':
                st.warning("You have an ongoing test. Please complete it.")
                if st.button("Resume Test", key=f"resume_{test['id']}"):
                    show_test(test['id'], user_id)
            elif test['status'] == 'completed':
                st.write(f"Score: {test['score']}")
                st.write(f"Completed on: {test['end_time']}")

def show_test(test_id, user_id):
    test_details = get_test_details(test_id)
    questions = json.loads(test_details['questions'])
    
    st.title(test_details['title'])
    st.write(test_details['description'])
    
    responses = {}
    for i, question in enumerate(questions):
        st.subheader(f"Question {i+1}")
        st.write(question['text'])
        if question['type'] == 'multiple_choice':
            response = st.radio(f"Select an answer for Question {i+1}", question['options'], key=f"q_{i}")
        elif question['type'] == 'text':
            response = st.text_area(f"Your answer for Question {i+1}", key=f"q_{i}")
        responses[i] = response
    
    if st.button("Submit Test"):
        score = calculate_score(questions, responses)
        if submit_test(test_id, user_id, responses, score):
            st.success("Test submitted successfully!")
            st.rerun()
        else:
            st.error("Failed to submit test. Please try again.")

def calculate_score(questions, responses):
    score = 0
    for i, question in enumerate(questions):
        if question['type'] == 'multiple_choice':
            if responses[i] == question['correct_answer']:
                score += 1
    return (score / len(questions)) * 100

# Main function to route to appropriate page
def main():
    if 'page' not in st.session_state:
        st.session_state.page = 'landing'

    if 'user' in st.session_state:
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

