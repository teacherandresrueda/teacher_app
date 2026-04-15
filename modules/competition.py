import streamlit as st

def show_competition(df):
    st.subheader("🏆 Marcador por Equipos")

    scores = df.groupby("Equipo")["Puntos"].sum().sort_values(ascending=False)

    for equipo, puntos in scores.items():
        st.markdown(f"### {equipo} → ⭐ {puntos}")

    st.bar_chart(scores)
