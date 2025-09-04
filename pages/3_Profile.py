import streamlit as st
from user_db import update_profile, get_db
from utils import verify_jwt, add_logout_button

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Profile Management", page_icon="👤")

# ---------- LOGIN CHECK ----------
token = st.session_state.get("jwt_token")
username = verify_jwt(token)
if not username:
    st.warning("⚠ Please login to access the profile page.")
    st.query_params = {"page": "home"}  # redirect to home
    st.stop()

# ---------- LOGOUT BUTTON ----------
add_logout_button()

# ---------- FETCH USER DATA ----------
conn = get_db()
c = conn.cursor()
c.execute("SELECT * FROM users WHERE username=?", (username,))
user = c.fetchone()
conn.close()

if not user:
    st.error("❌ User not found!")
    st.stop()

st.title("👤 Profile Management")
st.subheader(f"Welcome, {username} 👋")

# ---------- PREFILL CURRENT VALUES ----------
name = st.text_input("Full Name *", value=user[4] if user[4] else "")
age = st.number_input("Age *", min_value=10, max_value=100, value=user[5] if user[5] else 18)
gender_options = ["Male", "Female", "Other"]
gender = st.selectbox(
    "Gender *",
    gender_options,
    index=gender_options.index(user[6]) if user[6] in gender_options else 0
)
language = st.text_input("Preferred Language *", value=user[7] if user[7] else "")
photo = st.file_uploader("Upload Profile Photo", type=["jpg", "jpeg", "png"])

# ---------- UPDATE PROFILE ----------
if st.button("Update Profile"):
    photo_bytes = photo.read() if photo else None
    update_profile(username, name, age, gender, language, photo_bytes)
    st.success("✅ Profile updated successfully!")

    # Refresh session user data
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    updated_user = c.fetchone()
    conn.close()
    st.session_state["user"] = updated_user

    # Trigger rerun safely with new query_params API
    st.query_params = {"page": "profile"}  # preserve current page
    st.stop()  # stops execution and reruns automatically

# ---------- DOWNLOAD UPLOADED FILE ----------
if user[9]:  # uploaded_file column index (assuming 0:id, 1:username,..., 9:uploaded_file)
    st.subheader("📄 Your Uploaded Document")
    st.download_button(
        label="Download Uploaded File",
        data=user[9],
        file_name="uploaded_document",  # optional: add original extension if stored
        mime="application/octet-stream"
    )
