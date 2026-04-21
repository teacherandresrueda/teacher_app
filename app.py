import streamlit as st
from firebase_config import register_user, login_user

st.set_page_config(page_title="Teacher App", layout="centered")

st.title("🎓 Teacher System")

menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

# ---------------- LOGIN ----------------
if menu == "Login":
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        success, message = login_user(email, password)

        if success:
            st.success(message)
            st.session_state["user"] = email
        else:
            st.error(message)

# ---------------- REGISTER ----------------
if menu == "Register":
    st.subheader("Create Account")

    email = st.text_input("New Email")
    password = st.text_input("New Password", type="password")

    if st.button("Register"):
        success, message = register_user(email, password)

        if success:
            st.success(message)
        else:
            st.error(message)


# ---------------- DASHBOARD ----------------
if "user" in st.session_state:
    st.sidebar.success(f"Logged in as {st.session_state['user']}")

    st.subheader("📊 Dashboard")

    st.write("Aquí ya empieza tu sistema real...")
