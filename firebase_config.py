import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

# Inicializar Firebase UNA sola vez
if not firebase_admin._apps:

    cred = credentials.Certificate({
        "type": st.secrets["firebase"]["type"],
        "project_id": st.secrets["firebase"]["project_id"],
        "private_key_id": st.secrets["firebase"]["private_key_id"],
        "private_key": st.secrets["firebase"]["private_key"].replace("\\n", "\n"),
        "client_email": st.secrets["firebase"]["client_email"],
        "client_id": st.secrets["firebase"]["client_id"],
        "auth_uri": st.secrets["firebase"]["auth_uri"],
        "token_uri": st.secrets["firebase"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
    })

    firebase_admin.initialize_app(cred)

db = firestore.client()


# 🔹 REGISTRAR USUARIO
def register_user(email, password):
    users_ref = db.collection("users")
    user = users_ref.document(email).get()

    if user.exists:
        return False, "User already exists"

    users_ref.document(email).set({
        "email": email,
        "password": password
    })

    return True, "User created"


# 🔹 LOGIN
def login_user(email, password):
    user_ref = db.collection("users").document(email).get()

    if not user_ref.exists:
        return False, "User not found"

    user_data = user_ref.to_dict()

    if user_data["password"] == password:
        return True, "Login successful"
    else:
        return False, "Wrong password"
