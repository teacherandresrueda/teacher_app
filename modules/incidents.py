import streamlit as st
import pandas as pd
from datetime import datetime
import os

def incidents_ui():
    st.header("📋 Cuaderno de Incidencias")

    nombre = st.text_input("Alumno")
    descripcion = st.text_area("Descripción")
    fecha = datetime.now()

    if st.button("Registrar incidencia"):
        data = {
            "Alumno": nombre,
            "Descripcion": descripcion,
            "Fecha": fecha
        }

        df = pd.DataFrame([data])

        if os.path.exists("data/incidencias.csv"):
            df_old = pd.read_csv("data/incidencias.csv")
            df = pd.concat([df_old, df])

        df.to_csv("data/incidencias.csv", index=False)
        st.success("Incidencia registrada")

    if os.path.exists("data/incidencias.csv"):
        st.subheader("Historial")
        st.dataframe(pd.read_csv("data/incidencias.csv"))
