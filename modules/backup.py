import streamlit as st
import shutil
import os

DATA_PATH = "data"
BACKUP_PATH = "backups"

os.makedirs(BACKUP_PATH, exist_ok=True)

def backup_ui():
    st.header("💾 Backup & Recovery")

    # Backup
    if st.button("📦 Crear respaldo"):
        for archivo in os.listdir(DATA_PATH):
            shutil.copy(f"{DATA_PATH}/{archivo}", f"{BACKUP_PATH}/{archivo}")
        st.success("Backup creado")

    # Restaurar
    if st.button("♻️ Restaurar datos"):
        for archivo in os.listdir(BACKUP_PATH):
            shutil.copy(f"{BACKUP_PATH}/{archivo}", f"{DATA_PATH}/{archivo}")
        st.success("Datos restaurados")

    # Reset
    if st.button("🔄 Reset total"):
        for archivo in os.listdir(DATA_PATH):
            os.remove(f"{DATA_PATH}/{archivo}")
        st.warning("Sistema reiniciado")
