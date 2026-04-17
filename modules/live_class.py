import streamlit as st
import pandas as pd
import os

DATA_PATH = "data"

def live_class_ui():
    st.title("🎯 MODO CLASE EN VIVO")

    if not st.session_state.get("grupo_activo"):
        st.warning("⚠️ Selecciona un grupo primero en Class Manager")
        return

    ruta = f"{DATA_PATH}/{st.session_state.grupo_activo}.csv"

    if not os.path.exists(ruta):
        st.error("No hay datos del grupo")
        return

    df = pd.read_csv(ruta)

    st.subheader(f"📘 Grupo: {st.session_state.grupo_activo}")

    # 🔍 BUSCADOR RÁPIDO
    busqueda = st.text_input("🔍 Buscar alumno rápido")

    if busqueda:
        df = df[df["Nombre"].str.contains(busqueda, case=False)]

    # 🧠 TOP 3 VISUAL
    st.subheader("🏆 Top 3")
    top3 = df.sort_values(by="Puntos", ascending=False).head(3)

    cols = st.columns(3)
    for i, (_, row) in enumerate(top3.iterrows()):
        with cols[i]:
            st.metric(label=row["Nombre"], value=row["Puntos"])

    st.divider()

    # 👨‍🎓 LISTA INTERACTIVA
    st.subheader("👨‍🎓 Control de alumnos")

    for i, row in df.iterrows():
        col1, col2, col3, col4 = st.columns([3,1,1,1])

        with col1:
            st.write(f"**{row['Nombre']}**")

        with col2:
            if st.button(f"➕", key=f"plus_{i}"):
                df.loc[i, "Puntos"] += 10

        with col3:
            if st.button(f"➖", key=f"minus_{i}"):
                df.loc[i, "Puntos"] -= 5

        with col4:
            st.write(f"🏆 {row['Puntos']}")

    # 💾 Guardar automático
    df.to_csv(ruta, index=False)
