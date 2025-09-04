import streamlit as st
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your_secret_key_here"  # Replace with your secure secret key

# ---------- JWT GENERATION ----------
def generate_jwt(username, hours_valid=1):
    """
    Generate a JWT token for the given username with expiration time in hours.
    """
    payload = {
        "username": username,
        "exp": datetime.utcnow() + timedelta(hours=hours_valid)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# ---------- JWT VERIFICATION ----------
def verify_jwt(token):
    """
    Verify JWT token. Returns username if valid, else None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("username")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# ---------- LOGOUT BUTTON ----------
def add_logout_button():
    """
    Adds a logout button in the sidebar.
    Clears session and redirects to home page using st.stop() for rerun.
    """
    if st.sidebar.button("🔓 Logout", type="primary", use_container_width=True):
        # Clear all session state
        st.session_state.clear()
        # Redirect to home
        st.query_params = {"page": "home"}  # modern replacement for deprecated API
        # Stop execution to trigger rerun
        st.stop()
