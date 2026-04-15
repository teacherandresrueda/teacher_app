import streamlit as st

def show_metrics(df):
    col1, col2, col3 = st.columns(3)

    total = df["Alumno"].nunique()
    activos = int(df["Estado"].sum())
    riesgo = int((df["Estado"] == 0).sum())

    col1.metric("Alumnos", total)
    col2.metric("Activos", activos)
    col3.metric("Riesgo", riesgo)
