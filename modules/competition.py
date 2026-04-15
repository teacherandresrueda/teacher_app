import streamlit as st

def show_ranking(df):
    st.subheader("🥇 Top Alumnos")

    ranking = df.sort_values(by="Puntos", ascending=False).head(5)

    for i, row in ranking.iterrows():
        st.write(f"{row['Alumno']} → ⭐ {row['Puntos']}")

def show_competition(df):
    st.subheader("🏆 Marcador por Equipos")

    scores = df.groupby("Equipo")["Puntos"].sum().sort_values(ascending=False)

    for equipo, puntos in scores.items():
        st.markdown(f"### {equipo} → ⭐ {puntos}")

    st.bar_chart(scores)
