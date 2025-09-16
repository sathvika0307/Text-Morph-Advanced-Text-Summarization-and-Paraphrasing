import streamlit as st
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your_secret_key_here"  # Replace with a secure secret key

# ---------- JWT ----------
def generate_jwt(username, hours_valid=1):
    payload = {"username": username, "exp": datetime.utcnow() + timedelta(hours=hours_valid)}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("username")
    except:
        return None

# ---------- LOGOUT ----------
def add_logout_button():
    if st.sidebar.button("🔓 Logout", type="primary", use_container_width=True):
        st.session_state.clear()
        st.query_params = {"page": "home"}
        st.stop()
