import streamlit as st
import base64
from user_db import init_db, check_user, reset_password, get_db
from utils import add_logout_button, generate_jwt, verify_jwt

# ---------- BACKGROUND FUNCTION ----------
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background: 
            linear-gradient(rgba(0, 0, 0, 0.55), rgba(0, 0, 0, 0.55)),
            url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    h1, h2, h3, h4, h5, h6, p, label {{
        color: white !important;
    }}
    .stTextInput > div > div > input {{
        color: black;
        background-color: #ffffffcc;
    }}
    div.stButton > button {{
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 6px;
        font-weight: bold;
        cursor: pointer;
        transition: 0.3s;
    }}
    div.stButton > button:hover {{
        background-color: #45a049;
        transform: scale(1.05);
    }}
    </style>
    """
    return page_bg_img

# ---------- CONFIG ----------
st.set_page_config(page_title="AI Text Tool", page_icon="🤖", layout="centered")
st.markdown(add_bg_from_local("Background_Image.jpg"), unsafe_allow_html=True)

# Initialize DB
init_db()

# ---------- SESSION STATES ----------
for key in ["forgot_mode", "reset_mode", "user", "new_pw", "confirm_pw", "jwt_token"]:
    if key not in st.session_state:
        st.session_state[key] = None if key in ["user", "jwt_token"] else False if "mode" in key else ""

# ---------- MAIN PAGE ----------
st.title("🔐 AI-Based Text Summarization and Paraphrasing")

# ---------- JWT Verification ----------
if st.session_state.jwt_token:
    username = verify_jwt(st.session_state.jwt_token)
    if username:
        st.success(f"🎉 You are logged in as {username}")
        add_logout_button()
        st.stop()  # Stop further login UI
    else:
        st.session_state.jwt_token = None  # Clear expired/invalid token

# ---------- LOGIN ----------
if not st.session_state.forgot_mode:
    st.subheader("Login to Continue")
    identifier = st.text_input("Email or Username *")
    password = st.text_input("Password *", type="password")
    remember = st.checkbox("Remember Me")  # ✅ Remember Me option

    col1, col2 = st.columns([1,1])
    with col1:
        login_btn = st.button("Sign In")
    with col2:
        st.page_link("pages/1_Create_Account.py", label="Create Account", icon="📝")

    if st.button("Forgot Password?"):
        st.session_state.forgot_mode = True
        st.stop()

    if login_btn:
        user = check_user(identifier, password)
        if user:
            # JWT expiration: 1 hour if not remembered, 7 days if remembered
            hours_valid = 168 if remember else 1
            token = generate_jwt(user[1], hours_valid=hours_valid)

            st.session_state.jwt_token = token
            st.session_state.user = user
            st.success(f"✅ Welcome {user[4]}!")  # user[4] = name
            st.rerun()  # modern alternative for rerun
        else:
            st.error("❌ Invalid email or password.")

# ---------- FORGOT PASSWORD ----------
elif st.session_state.forgot_mode:
    st.subheader("🔑 Forgot Password")
    reset_identifier = st.text_input("Enter your registered Email or Username", key="reset_identifier")

    if not st.session_state.reset_mode:
        if st.button("Recover Account"):
            conn = get_db()
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE email=? OR username=?", (reset_identifier, reset_identifier))
            user = c.fetchone()
            conn.close()

            if user:
                st.success("✅ User found. Please set a new password.")
                st.session_state.reset_mode = True
                st.stop()
            else:
                st.error("❌ Email/Username not found.")

    if st.session_state.reset_mode:
        st.session_state.new_pw = st.text_input("Enter New Password", type="password", value=st.session_state.new_pw)
        st.session_state.confirm_pw = st.text_input("Confirm New Password", type="password", value=st.session_state.confirm_pw)

        if st.button("Update Password"):
            if st.session_state.new_pw == st.session_state.confirm_pw and st.session_state.new_pw != "":
                reset_password(reset_identifier, st.session_state.new_pw)
                st.success("🔒 Password updated successfully! Please login again.")
                st.session_state.reset_mode = False
                st.session_state.forgot_mode = False
                st.session_state.new_pw = ""
                st.session_state.confirm_pw = ""
            else:
                st.error("❌ Passwords do not match or are empty.")

    if st.button("⬅ Back to Login"):
        st.session_state.update({
            "forgot_mode": False,
            "reset_mode": False,
            "new_pw": "",
            "confirm_pw": ""
        })
        st.stop()

# ---------- Sidebar Logout Style ----------
st.markdown("""
    <style>
    div[data-testid="stSidebar"] button[kind="primary"] {
        background-color: #28a745 !important;
        color: white !important;
    }
    div[data-testid="stSidebar"] button[kind="primary"]:hover {
        background-color: #218838 !important;
    }
    </style>
""", unsafe_allow_html=True)
add_logout_button()