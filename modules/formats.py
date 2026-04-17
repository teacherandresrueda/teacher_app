import streamlit as st
from datetime import date

def formats_ui():
    st.header("📄 Formatos PRO MAX")

    opcion = st.selectbox("Selecciona un formato", [
        "Reporte de conducta",
        "Formato de tarea",
        "Observación docente"
    ])

    # 🧠 Autollenado inteligente
    alumno = st.text_input("Nombre del alumno (opcional)")
    grupo = st.session_state.get("grupo_activo", "")
    fecha = str(date.today())

    contenido = ""

    if opcion == "Reporte de conducta":
        contenido = f"""Alumno: {alumno}
Grupo: {grupo}
Fecha: {fecha}

Descripción:

Acción tomada:

Firma:"""

    elif opcion == "Formato de tarea":
        contenido = f"""Student Name: {alumno}
Date: {fecha}
Group: {grupo}

Topic:

Instructions:"""

    elif opcion == "Observación docente":
        contenido = f"""Alumno: {alumno}
Grupo: {grupo}
Fecha: {fecha}

Fortalezas:

Áreas de mejora:

Recomendaciones:"""

    # ✏️ Editable
    texto = st.text_area("✏️ Edita el formato", contenido, height=300)

    # 📋 Copiar visual
    st.code(texto)

    # 💾 Descargar
    st.download_button(
        label="⬇️ Descargar formato",
        data=texto,
        file_name=f"{opcion}_{alumno}.txt",
        mime="text/plain"
    )

    # 🧠 Uso rápido en clase
    st.info("💡 Puedes proyectar esto o pedir que lo copien directamente.")
