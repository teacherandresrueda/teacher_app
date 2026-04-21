import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
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
