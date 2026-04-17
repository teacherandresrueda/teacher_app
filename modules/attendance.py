import streamlit as st
import pandas as pd
import os
from datetime import date

DATA_PATH = "data"

def attendance_ui():
    st.header("📝 Pase de Lista")

    if not st.session_state.get("grupo_activo"):
        st.warning("Selecciona un grupo primero")
        return

    ruta = f"{DATA_PATH}/{st.session_state.grupo_activo}.csv"

    if not os.path.exists(ruta):
        st.error("No hay grupo")
        return

    df = pd.read_csv(ruta)

    st.subheader(f"Grupo: {st.session_state.grupo_activo}")
    hoy = date.today()

    asistencia = {}

    for i, row in df.iterrows():
        asistencia[row["Nombre"]] = st.checkbox(row["Nombre"], value=True)

    if st.button("💾 Guardar asistencia"):
        df_asistencia = pd.DataFrame(list(asistencia.items()), columns=["Nombre", "Asistencia"])
        df_asistencia["Fecha"] = hoy
        df_asistencia.to_csv(f"data/asistencia_{hoy}.csv", index=False)
        st.success("Asistencia guardada")
