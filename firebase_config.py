import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

# Inicialización segura
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

# -------- USERS --------
def register_user(email, password):
    ref = db.collection("users").document(email)

    if ref.get().exists:
        return False, "User exists"

    ref.set({
        "email": email,
        "password": password
    })

    return True, "Created"


def login_user(email, password):
    ref = db.collection("users").document(email).get()

    if not ref.exists:
        return False, "Not found"

    if ref.to_dict()["password"] == password:
        return True, "Welcome"

    return False, "Wrong password"


# -------- STUDENTS --------
def add_student(teacher, name):
    db.collection("students").add({
        "teacher": teacher,
        "name": name,
        "points": 0
    })


def get_students(teacher):
    docs = db.collection("students").where("teacher", "==", teacher).stream()
    return [{**doc.to_dict(), "id": doc.id} for doc in docs]


def add_points(student_id, pts):
    ref = db.collection("students").document(student_id)
    data = ref.get().to_dict()
    ref.update({
        "points": data["points"] + pts
    })
