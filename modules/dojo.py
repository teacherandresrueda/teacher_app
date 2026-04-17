import streamlit as st
import pandas as pd
import os

DATA_PATH = "data"

def dojo_ui():
    st.header("🔥 DOJO - Ranking")

    if not st.session_state.grupo_activo:
        st.warning("Selecciona un grupo primero")
        return

    ruta = f"{DATA_PATH}/{st.session_state.grupo_activo}.csv"

    if not os.path.exists(ruta):
        st.error("No hay datos")
        return

    df = pd.read_csv(ruta)

    ranking = df.sort_values(by="Puntos", ascending=False)

    st.subheader("🏆 Ranking del grupo")
    st.dataframe(ranking, use_container_width=True)

    # Inteligencia básica
    st.subheader("🧠 Alertas inteligentes")

    inactivos = df[df["Puntos"] == 0]

    if not inactivos.empty:
        st.warning("Alumnos sin puntos (posible falta de participación)")
        st.dataframe(inactivos)
