import streamlit as st

from modules.class_manager import class_manager_ui
from modules.students import students_ui
from modules.dojo import dojo_ui
from modules.backup import backup_ui

st.set_page_config(page_title="Teacher System", layout="wide")

st.title("🎓 TEACHER SYSTEM PRO")

menu = st.sidebar.radio("Navegación", [
    "📚 Class Manager",
    "👨‍🎓 Students",
    "🔥 Dojo",
    "💾 Backup"
])

if "grupo_activo" not in st.session_state:
    st.session_state.grupo_activo = None

if menu == "📚 Class Manager":
    class_manager_ui()

elif menu == "👨‍🎓 Students":
    students_ui()

elif menu == "🔥 Dojo":
    dojo_ui()

elif menu == "💾 Backup":
    backup_ui()
