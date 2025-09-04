import sys
import os
import streamlit as st
from utils import add_logout_button, generate_jwt
from user_db import init_db, add_user, get_db

# Add project root to sys.path so imports work
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Initialize database
init_db()

st.title("📝 Create New Account")

with st.form("register_form", clear_on_submit=True):
    name = st.text_input("Full Name *")
    age = st.number_input("Age *", min_value=10, max_value=100, step=1)
    gender = st.radio("Gender *", ["Male", "Female", "Others"])
    email = st.text_input("Email *")
    username = st.text_input("Username *")
    password = st.text_input("Password *", type="password")
    confirm_password = st.text_input("Re-enter Password *", type="password")
    language = st.radio("Preferred Language *", ["English", "Hindi"])
    profile_photo = st.file_uploader("Upload Profile Photo (Optional)", type=["jpg", "png", "jpeg"])

    submit = st.form_submit_button("Create Account")

    if submit:
        if not username or not email or not password:
            st.error("⚠ Username, Email, and Password are required!")
        elif password != confirm_password:
            st.error("⚠ Passwords do not match!")
        else:
            # Convert uploaded photo into binary if uploaded
            photo_data = profile_photo.read() if profile_photo else None

            # Add user into database
            success = add_user(
                username=username,
                email=email,
                password=password,
                name=name,
                age=age,
                gender=gender,
                language=language,
                photo=photo_data
            )

            if success:
                # ✅ Auto-login with JWT
                token = generate_jwt(username)
                st.session_state.jwt_token = token

                # Fetch the newly created user
                conn = get_db()
                c = conn.cursor()
                c.execute("SELECT * FROM users WHERE username=?", (username,))
                user = c.fetchone()
                conn.close()
                st.session_state.user = user

                # Show success message
                st.success("🎉 Account Created Successfully! You are now logged in.")
            else:
                st.error("⚠ Username or Email already registered! Try another one.")

# Always show logout button in sidebar
add_logout_button()
