import streamlit as st
from firebase_config import register_user, login_user, db
from ai_module import generate_strategy

st.title("MetaPattern EDU System")

menu = st.sidebar.selectbox("Menu", ["Login", "Register", "Dashboard"])

# REGISTER
if menu == "Register":
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        uid = register_user(email, password)
        if uid:
            st.success("User created")
        else:
            st.error("Error creating user")

# LOGIN
elif menu == "Login":
    email = st.text_input("Email")
    
    if st.button("Login"):
        uid = login_user(email)
        if uid:
            st.session_state["user"] = uid
            st.success("Login successful")
        else:
            st.error("Invalid credentials")

# DASHBOARD
elif menu == "Dashboard":

    if "user" not in st.session_state:
        st.warning("Please login first")
    else:
        st.success("Welcome")

        st.subheader("Student Risk Input")

        student_data = st.text_area("Describe student situation")

        if st.button("Analyze Student"):
            result = generate_strategy(student_data)

            # Guardar en nube
            db.collection("risk_analysis").add({
                "user": st.session_state["user"],
                "data": student_data,
                "result": result
            })

            st.write(result)
