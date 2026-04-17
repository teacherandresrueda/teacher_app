import streamlit as st
import pandas as pd
import os

DATA_PATH = "data"
os.makedirs(DATA_PATH, exist_ok=True)

def class_manager_ui():
    st.header("📚 Class Manager")

    # Crear grupo
    st.subheader("➕ Crear grupo")
    nuevo_grupo = st.text_input("Nombre del grupo (ej: 2A, 3B)")

    if st.button("Crear grupo"):
        ruta = f"{DATA_PATH}/{nuevo_grupo}.csv"
        if not os.path.exists(ruta):
            df = pd.DataFrame(columns=["Nombre", "Puntos"])
            df.to_csv(ruta, index=False)
            st.success(f"Grupo {nuevo_grupo} creado")
        else:
            st.warning("Ese grupo ya existe")

    # Seleccionar grupo
    st.subheader("📂 Seleccionar grupo")
    grupos = [f.replace(".csv", "") for f in os.listdir(DATA_PATH)]

    if grupos:
        grupo = st.selectbox("Grupos disponibles", grupos)

        if st.button("Activar grupo"):
            st.session_state.grupo_activo = grupo
            st.success(f"Grupo activo: {grupo}")

    # Importar lista
    if st.session_state.grupo_activo:
        st.subheader(f"📥 Importar alumnos a {st.session_state.grupo_activo}")

        archivo = st.file_uploader("Sube Excel", type=["xlsx"])

        if archivo:
            df = pd.read_excel(archivo)

            if "Nombre" not in df.columns:
                st.error("El archivo debe tener columna 'Nombre'")
            else:
                df["Puntos"] = 0
                ruta = f"{DATA_PATH}/{st.session_state.grupo_activo}.csv"
                df.to_csv(ruta, index=False)
                st.success("Lista importada correctamente")
