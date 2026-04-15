import streamlit as st

def show_alerts(df):
    st.subheader("🚨 Alumnos en riesgo")

    alertas = df[df["Estado"] == 0]

    if alertas.empty:
        st.success("No hay alumnos en riesgo 🎉")
    else:
        st.dataframe(alertas, use_container_width=True)
