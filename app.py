import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import hashlib
import pandas as pd

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Teacher SaaS", layout="wide")

# ---------------- FIREBASE INIT ----------------
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
        return False, "User already exists"

    ref.set({
        "email": email,
        "password": hash_password(password)
    })

    return True, "Account created"

def login_user(email, password):
    ref = db.collection("users").document(email)
    user = ref.get()

    if not user.exists:
        return False, "User not found"

    data = user.to_dict()

    if data["password"] == hash_password(password):
        return True, "Login successful"
    else:
        return False, "Incorrect password"

# ---------------- GROUPS ----------------
def create_group(user, group_name):
    db.collection("groups").add({
        "user": user,
        "name": group_name
    })

def get_groups(user):
    docs = db.collection("groups").where("user", "==", user).stream()
    groups = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        groups.append(data)
    return groups

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
    students = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        students.append(data)
    return students

def add_points(student_id, points):
    db.collection("students").document(student_id).update({
        "points": firestore.Increment(points)
    })

# ---------------- DEMO DATA ----------------
def load_demo_data(user, group_id):
    demo_students = [
        {"name": "Ana", "points": 5},
        {"name": "Luis", "points": 2},
        {"name": "Carlos", "points": -1},
        {"name": "Sofía", "points": 8},
    ]

    docs = db.collection("students").where("group_id", "==", group_id).stream()
    for doc in docs:
        db.collection("students").document(doc.id).delete()

    for s in demo_students:
        db.collection("students").add({
            "user": user,
            "group_id": group_id,
            "name": s["name"],
            "points": s["points"]
        })

# ---------------- UPLOAD EXCEL ----------------
def upload_students_from_excel(user, group_id, file):
    df = pd.read_excel(file)

    if "name" not in df.columns:
        return False, "El archivo debe tener una columna llamada 'name'"

    docs = db.collection("students").where("group_id", "==", group_id).stream()
    for doc in docs:
        db.collection("students").document(doc.id).delete()

    for _, row in df.iterrows():
        db.collection("students").add({
            "user": user,
            "group_id": group_id,
            "name": row["name"],
            "points": 0
        })

    return True, "Carga masiva exitosa 🚀"

# ---------------- SIDEBAR ----------------
st.sidebar.title("📚 Teacher SaaS")

if st.session_state.user:
    st.sidebar.success(f"👤 {st.session_state.user}")

    if st.sidebar.button("Cerrar sesión", key="logout_btn"):
        st.session_state.user = None
        st.rerun()

menu = st.sidebar.selectbox("Navigation", ["Login", "Register"])

# =========================================================
# ---------------- AUTH SCREENS ----------------
# =========================================================
if not st.session_state.user:

    if menu == "Login":
        st.title("🔐 Login")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login", key="login_btn"):
            if email and password:
                ok, msg = login_user(email, password)
                if ok:
                    st.session_state.user = email
                    st.success("Welcome 🔥")
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.warning("Fill all fields")

    elif menu == "Register":
        st.title("🆕 Create Account")

        email = st.text_input("New email")
        password = st.text_input("New password", type="password")

        if st.button("Create account", key="register_btn"):
            if email and password:
                ok, msg = register_user(email, password)
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)
            else:
                st.warning("Fill all fields")

# =========================================================
# ---------------- MAIN APP ----------------
# =========================================================
else:
    st.title("📊 Classroom SaaS Panel")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Students", "Points", "Dashboard", "Groups"]
    )

    groups = get_groups(st.session_state.user)

    # ---------------- GROUPS TAB ----------------
    with tab4:
        st.subheader("👥 Manage Groups")

        group_name = st.text_input("New group name")

        if st.button("Create group", key="create_group_btn"):
            if group_name:
                create_group(st.session_state.user, group_name)
                st.success("Group created")
                st.rerun()

        st.divider()

        if groups:
            group_options = {g["name"]: g["id"] for g in groups}
            selected_group = st.selectbox(
                "Select group", list(group_options.keys())
            )

            group_id = group_options[selected_group]

            st.markdown("### 📂 Upload students (Excel)")
            file = st.file_uploader("Upload Excel file", type=["xlsx"])

            if file:
                ok, msg = upload_students_from_excel(
                    st.session_state.user, group_id, file
                )
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

            st.markdown("### 🧪 Demo data")
            if st.button("Load demo students", key="demo_btn"):
                load_demo_data(st.session_state.user, group_id)
                st.success("Demo cargado 🚀")
                st.rerun()

            st.markdown("### 👀 Students")
            students = get_students(st.session_state.user, group_id)

            for s in students:
                st.write(f"👤 {s['name']} — ⭐ {s['points']}")

        else:
            st.info("Create a group first")

    # ---------------- STUDENTS TAB ----------------
    with tab1:
        st.subheader("Add student manually")

        if groups:
            group_options = {g["name"]: g["id"] for g in groups}
            selected_group = st.selectbox(
                "Select group", list(group_options.keys()),
                key="students_group"
            )

            group_id = group_options[selected_group]

            name = st.text_input("Student name")

            if st.button("Add student", key="add_student_btn"):
                if name:
                    add_student(st.session_state.user, name, group_id)
                    st.success("Student added")
                    st.rerun()
                else:
                    st.warning("Enter a name")
        else:
            st.info("Create a group first")

    # ---------------- POINTS TAB ----------------
    with tab2:
        st.subheader("Manage points")

        if groups:
            group_options = {g["name"]: g["id"] for g in groups}
            selected_group = st.selectbox(
                "Select group", list(group_options.keys()),
                key="points_group"
            )

            group_id = group_options[selected_group]
            students = get_students(st.session_state.user, group_id)

            for s in students:
                col1, col2, col3 = st.columns([3, 1, 1])

                col1.write(f"{s['name']} ({s['points']})")

                if col2.button("+1", key=f"plus_{s['id']}"):
                    add_points(s["id"], 1)
                    st.rerun()

                if col3.button("-1", key=f"minus_{s['id']}"):
                    add_points(s["id"], -1)
                    st.rerun()
        else:
            st.info("Create a group first")

    # ---------------- DASHBOARD TAB ----------------
    with tab3:
        st.subheader("📊 Dashboard")

        if groups:
            group_options = {g["name"]: g["id"] for g in groups}
            selected_group = st.selectbox(
                "Select group", list(group_options.keys()),
                key="dashboard_group"
            )

            group_id = group_options[selected_group]
            students = get_students(st.session_state.user, group_id)

            if students:
                df = pd.DataFrame(students)
                df = df.sort_values(by="points", ascending=False)

                st.markdown("### 🏆 Top Students")
                for _, row in df.head(3).iterrows():
                    st.success(f"{row['name']} — {row['points']} pts")

                st.markdown("### ⚠ Students at Risk")
                risk = df[df["points"] <= 0]

                if not risk.empty:
                    for _, row in risk.iterrows():
                        st.warning(f"{row['name']} — {row['points']} pts")
                else:
                    st.info("No students at risk")

                st.markdown("### 📊 Chart")
                chart_df = df[["name", "points"]].set_index("name")
                st.bar_chart(chart_df)

                st.markdown("### 📋 Table")
                st.dataframe(df)
            else:
                st.info("No students in this group")
        else:
            st.info("Create a group first")
