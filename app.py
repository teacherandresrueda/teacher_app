import streamlit as st
import pandas as pd
from datetime import datetime
import random

st.set_page_config(layout="wide")

# =========================
# 🔐 LOGIN SIMPLE (ROL)
# =========================
role = st.sidebar.selectbox("Select Role / Seleccionar Rol", ["Teacher", "Director", "Student"])

# =========================
# 📊 DATA BASE
# =========================
students = [
    {"name": "AXEL TORRES", "group": "1A", "last_login": "2026-01-30"},
    {"name": "EDUARDO VILCHIS", "group": "1A", "last_login": "2026-03-20"},
    {"name": "MARIANA FALOFUL", "group": "1B", "last_login": "2026-04-04"},
    {"name": "ZOE RANGEL", "group": "1B", "last_login": None},
]

# =========================
# 🧠 LÓGICA
# =========================
def classify(last_login):
    if last_login is None:
        return "critical"
    days = (datetime.now() - datetime.strptime(last_login, "%Y-%m-%d")).days
    if days <= 7:
        return "active"
    elif days <= 30:
        return "risk"
    return "critical"

def metrics(status):
    if status == "active":
        return random.randint(85,100), random.randint(80,100), "Low"
    elif status == "risk":
        return random.randint(60,84), random.randint(50,79), "Medium"
    else:
        return random.randint(0,59), random.randint(10,49), "High"

data = []
for s in students:
    status = classify(s["last_login"])
    grade, participation, risk = metrics(status)

    data.append({
        "Name": s["name"],
        "Group": s["group"],
        "Status": status,
        "Grade": grade,
        "Participation": participation,
        "Fail Risk": risk
    })

df = pd.DataFrame(data)

# =========================
# 👨‍🏫 TEACHER VIEW
# =========================
if role == "Teacher":
    st.title("👨‍🏫 Teacher Dashboard")

    group = st.selectbox("Select Group", df["Group"].unique())
    df_group = df[df["Group"] == group]

    st.dataframe(df_group, use_container_width=True)

    st.subheader("⚠️ Students in Risk")
    st.write(df_group[df_group["Status"] != "active"])

# =========================
# 🧑‍💼 DIRECTOR VIEW
# =========================
elif role == "Director":
    st.title("🧑‍💼 Institutional Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", len(df))
    col2.metric("Critical", len(df[df["Status"]=="critical"]))
    col3.metric("At Risk", len(df[df["Status"]=="risk"]))

    st.bar_chart(df["Status"].value_counts())

    st.subheader("Groups Performance")
    st.dataframe(df.groupby("Group").mean(numeric_only=True))

# =========================
# 🎓 STUDENT VIEW
# =========================
else:
    st.title("🎓 Student Feedback System")

    student_name = st.selectbox("Select your name", df["Name"])
    student = df[df["Name"] == student_name].iloc[0]

    st.metric("Grade", student["Grade"])
    st.metric("Participation", student["Participation"])
    st.metric("Risk", student["Fail Risk"])

    if student["Fail Risk"] == "High":
        st.error("⚠️ You are at risk of failing. Submit pending work immediately.")
    elif student["Fail Risk"] == "Medium":
        st.warning("You need to improve your participation.")
    else:
        st.success("Great performance! Keep going.")
