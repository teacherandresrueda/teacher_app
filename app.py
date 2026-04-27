import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import hashlib
import pandas as pd
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Teacher Intelligence System", layout="wide")

# ---------------- FIREBASE ----------------
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- SECURITY ----------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------- AUTH ----------------
def register_user(email, password):
    ref = db.collection("users").document(email)
    if ref.get().exists:
        return False, "User exists"
    ref.set({"email": email, "password": hash_password(password)})
    return True, "Created"

def login_user(email, password):
    ref = db.collection("users").document(email)
    user = ref.get()
    if not user.exists:
        return False, "No user"
    if user.to_dict()["password"] == hash_password(password):
        return True, "OK"
    return False, "Wrong password"

# ---------------- GROUPS ----------------
def create_group(user, name, grade):
    db.collection("groups").add({
        "user": user,
        "name": name,
        "grade": grade
    })

def get_groups(user):
    docs = db.collection("groups").where("user", "==", user).stream()
    return [{**doc.to_dict(), "id": doc.id} for doc in docs]

# ---------------- STUDENTS ----------------
def add_student(user, name, group_id):
    db.collection("students").add({
        "user": user,
        "name": name,
        "group_id": group_id,
        "points": 0
    })

def get_students(user, group_id=None):
    query = db.collection("students").where("user", "==", user)
    if group_id:
        query = query.where("group_id", "==", group_id)
    docs = query.stream()
    return [{**doc.to_dict(), "id": doc.id} for doc in docs]

# ---------------- LISTA AUTO ----------------
def load_my_students(user, group_id):
    names = [
        "Andrea López","Luis Martínez","Carlos Ramírez",
        "Sofía Hernández","Valeria Torres","Diego Castro",
        "Fernanda Ruiz","Jorge Mendoza","Camila Ortiz","Daniel Pérez"
    ]

    docs = db.collection("students").where("group_id", "==", group_id).stream()
    for d in docs:
        db.collection("students").document(d.id).delete()

    for n in names:
        db.collection("students").add({
            "user": user,
            "group_id": group_id,
            "name": n,
            "points": 0
        })

# ---------------- POINTS + LOG ----------------
def add_points(student_id, points, user, behavior):
    db.collection("students").document(student_id).update({
        "points": firestore.Increment(points)
    })

    db.collection("logs").add({
        "student_id": student_id,
        "points": points,
        "behavior": behavior,
        "user": user,
        "timestamp": datetime.now()
    })

def get_logs(user):
    docs = db.collection("logs").where("user", "==", user).stream()
    return [doc.to_dict() for doc in docs]

# ---------------- ANALYTICS ----------------
def student_summary(student_id, logs):
    total = sum(l["points"] for l in logs if l["student_id"] == student_id)
    pos = sum(1 for l in logs if l["student_id"] == student_id and l["points"] > 0)
    neg = sum(1 for l in logs if l["student_id"] == student_id and l["points"] < 0)

    return total, pos, neg

def risk_level(total, pos, neg):
    if neg > pos:
        return "🔴 High Risk"
    elif total < 5:
        return "🟡 Medium"
    return "🟢 Good"

# ---------------- UI ----------------
st.sidebar.title("🚀 Teacher Intelligence")

if st.session_state.user:
    st.sidebar.success(st.session_state.user)
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

menu = st.sidebar.radio(
    "Menu",
    ["Login","Register"] if not st.session_state.user else
    ["Dashboard","Groups","Students","Points","Analytics","Logs"]
)

# ---------------- LOGIN ----------------
if not st.session_state.user:

    if menu == "Login":
        st.title("Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            ok,_ = login_user(email,password)
            if ok:
                st.session_state.user = email
                st.rerun()
            else:
                st.error("Error")

    if menu == "Register":
        st.title("Register")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Register"):
            ok,msg = register_user(email,password)
            st.success(msg) if ok else st.error(msg)

# ---------------- APP ----------------
else:

    groups = get_groups(st.session_state.user)

    # GROUPS
    if menu == "Groups":
        st.title("Groups")
        name = st.text_input("Name")
        grade = st.selectbox("Grade", ["1","2","3"])

        if st.button("Create"):
            create_group(st.session_state.user,name,grade)
            st.rerun()

        for g in groups:
            st.write(f"{g['grade']}° {g['name']}")

    # STUDENTS
    if menu == "Students":
        st.title("Students")

        if groups:
            gdict = {f"{g['grade']}° {g['name']}": g["id"] for g in groups}
            sel = st.selectbox("Group", list(gdict.keys()))
            gid = gdict[sel]

            if st.button("🔥 Load List"):
                load_my_students(st.session_state.user,gid)
                st.rerun()

            for s in get_students(st.session_state.user,gid):
                st.write(f"{s['name']} - {s['points']}")

    # POINTS
    if menu == "Points":
        st.title("Points System")

        behaviors = {
            "Participation": 2,
            "Homework": 2,
            "Teamwork": 3,
            "Late": -1,
            "No Homework": -2
        }

        if groups:
            gdict = {f"{g['grade']}° {g['name']}": g["id"] for g in groups}
            sel = st.selectbox("Group", list(gdict.keys()))
            gid = gdict[sel]

            students = get_students(st.session_state.user,gid)

            for s in students:
                st.subheader(s["name"])
                cols = st.columns(len(behaviors))

                for i,(b,val) in enumerate(behaviors.items()):
                    if cols[i].button(f"{b} ({val})", key=f"{s['id']}_{b}"):
                        add_points(s["id"],val,st.session_state.user,b)
                        st.rerun()

    # DASHBOARD
    if menu == "Dashboard":
        st.title("Dashboard")

        if groups:
            gdict = {f"{g['grade']}° {g['name']}": g["id"] for g in groups}
            sel = st.selectbox("Group", list(gdict.keys()))
            gid = gdict[sel]

            students = get_students(st.session_state.user,gid)

            if students:
                df = pd.DataFrame(students).sort_values("points", ascending=False)
                st.bar_chart(df.set_index("name")["points"])
                st.dataframe(df)

    # ANALYTICS 🔥
    if menu == "Analytics":
        st.title("AI Behavior Analysis")

        logs = get_logs(st.session_state.user)

        students = get_students(st.session_state.user)

        for s in students:
            total,pos,neg = student_summary(s["id"], logs)
            risk = risk_level(total,pos,neg)

            st.write(f"{s['name']} | {total} pts | {risk}")

    # LOGS
    if menu == "Logs":
        st.title("Logs")

        logs = get_logs(st.session_state.user)

        if logs:
            df = pd.DataFrame(logs)
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            # FILTROS 🔥
            date_filter = st.date_input("Filter by date")

            if date_filter:
                df = df[df["timestamp"].dt.date == date_filter]

            st.dataframe(df.sort_values("timestamp", ascending=False))
