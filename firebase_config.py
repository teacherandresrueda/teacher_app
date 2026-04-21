import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import json

if not firebase_admin._apps:

    firebase_dict = json.loads(st.secrets["firebase_json"])

    firebase_dict["private_key"] = firebase_dict["private_key"].replace("\\n", "\n")

    cred = credentials.Certificate(firebase_dict)

    firebase_admin.initialize_app(cred)

db = firestore.client()

# ---------------- ALUMNOS ----------------

def add_student(teacher, name):
    db.collection("students").add({
        "teacher": teacher,
        "name": name,
        "points": 0
    })


def get_students(teacher):
    docs = db.collection("students").where("teacher", "==", teacher).stream()
    return [doc.to_dict() | {"id": doc.id} for doc in docs]


def add_points(student_id, points):
    ref = db.collection("students").document(student_id)
    student = ref.get().to_dict()

    new_points = student["points"] + points
    ref.update({"points": new_points})
