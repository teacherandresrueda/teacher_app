import streamlit as st
import pandas as pd
import os

DATA_PATH = "data"

def students_ui():
    st.header("👨‍🎓 Students")

    if not st.session_state.grupo_activo:
        st.warning("Selecciona un grupo primero")
        return

    ruta = f"{DATA_PATH}/{st.session_state.grupo_activo}.csv"

    if not os.path.exists(ruta):
        st.error("El grupo no tiene datos aún")
        return

    df = pd.read_csv(ruta)

    st.subheader(f"Grupo: {st.session_state.grupo_activo}")
    st.dataframe(df, use_container_width=True)

    alumno = st.selectbox("Selecciona alumno", df["Nombre"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ +10 puntos"):
            df.loc[df["Nombre"] == alumno, "Puntos"] += 10

    with col2:
        if st.button("➖ -5 puntos"):
            df.loc[df["Nombre"] == alumno, "Puntos"] -= 5

    df.to_csv(ruta, index=False)
