import streamlit as st

def formats_ui():
    st.header("📄 Formatos útiles")

    st.subheader("Reporte de conducta")
    st.code("""
Alumno:
Grupo:
Fecha:
Descripción:
Acción tomada:
Firma:
""")

    st.subheader("Formato de tarea")
    st.code("""
Student Name:
Date:
Topic:
Instructions:
""")

    st.subheader("Observación docente")
    st.code("""
Alumno:
Fortalezas:
Áreas de mejora:
Recomendaciones:
""")
