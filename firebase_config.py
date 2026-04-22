import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

# 🔐 Inicializar Firebase con SECRETS
if not firebase_admin._apps:
    firebase_dict = json.loads(st.secrets["firebase_json"])
    cred = credentials.Certificate(firebase_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# -------- LOGIN --------
def login_user(email, password):
    try:
        ref = db.collection("users").document(email)
        user = ref.get()

        if not user.exists:
            return False, "User not found"

        data = user.to_dict()

        if data["password"] == password:
            return True, "Login successful"
        else:
            return False, "Wrong password"

    except Exception as e:
        return False, str(e)

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
