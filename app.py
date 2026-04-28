import streamlit as st

st.set_page_config(page_title="Teacher App", layout="wide")

st.title("📱 Teacher App")

# -------- SESSION STATE --------
if "students" not in st.session_state:
    st.session_state.students = []

# -------- SIDEBAR --------
st.sidebar.title("Menu")
menu = st.sidebar.radio("Go to", ["Home", "Points", "Ranking"])

# -------- HOME --------
if menu == "Home":
    st.header("➕ Add Students")

    new_student = st.text_input("Student name")

    if st.button("Add student"):
        if new_student:
            st.session_state.students.append({
                "name": new_student,
                "points": 0
            })
            st.success(f"{new_student} added!")

    st.subheader("📋 Current Students")

    if st.session_state.students:
        for s in st.session_state.students:
            st.write(f"{s['name']} - {s['points']} pts")
    else:
        st.warning("No students yet")

# -------- POINTS --------
elif menu == "Points":
    st.header("🎯 Give Points")

    if not st.session_state.students:
        st.warning("Add students first")
    else:
        for i, student in enumerate(st.session_state.students):
            col1, col2, col3, col4 = st.columns([3,1,1,1])

            col1.write(student["name"])
            col2.write(f"{student['points']} pts")

            if col3.button("+1", key=f"add_{i}"):
                st.session_state.students[i]["points"] += 1

            if col4.button("-1", key=f"sub_{i}"):
                st.session_state.students[i]["points"] -= 1

# -------- RANKING --------
elif menu == "Ranking":
    st.header("🏆 Ranking")

    if not st.session_state.students:
        st.warning("No students yet")
    else:
        sorted_students = sorted(
            st.session_state.students,
            key=lambda x: x["points"],
            reverse=True
        )

        for i, student in enumerate(sorted_students, start=1):
            st.write(f"{i}. {student['name']} - {student['points']} pts")
