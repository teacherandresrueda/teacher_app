from firebase_config import add_student, get_students, add_points

if "user" in st.session_state:

    st.sidebar.success(f"Teacher: {st.session_state['user']}")

    st.title("📊 Class Control Panel")

    tab1, tab2, tab3 = st.tabs(["Students", "ClassDojo+", "Strategy"])

    # -------- STUDENTS --------
    with tab1:
        st.subheader("Add Student")

        name = st.text_input("Student name")

        if st.button("Add"):
            add_student(st.session_state["user"], name)
            st.success("Student added")

        st.subheader("Student List")

        students = get_students(st.session_state["user"])

        for s in students:
            st.write(f"👤 {s['name']} | ⭐ {s['points']}")

    # -------- CLASSDOJO+ --------
    with tab2:
        st.subheader("Give Points")

        students = get_students(st.session_state["user"])

        for s in students:
            col1, col2, col3 = st.columns([3,1,1])

            col1.write(f"{s['name']} ({s['points']})")

            if col2.button(f"+1 {s['id']}"):
                add_points(s["id"], 1)

            if col3.button(f"-1 {s['id']}"):
                add_points(s["id"], -1)

    # -------- STRATEGY --------
    with tab3:
        st.subheader("Strategic Insight")

        students = get_students(st.session_state["user"])

        if students:
            best = max(students, key=lambda x: x["points"])
            worst = min(students, key=lambda x: x["points"])

            st.success(f"Top student: {best['name']} ⭐ {best['points']}")
            st.warning(f"Needs attention: {worst['name']} ⚠ {worst['points']}")

        st.info("This is your behavioral control system.")
