import streamlit as st

def apply_filters(df):
    st.sidebar.header("Filtros")

    # 🎯 Filtro por estado
    estado = st.sidebar.selectbox("Estado", ["Todos", "Activos", "Riesgo"])

    if estado == "Activos":
        df = df[df["Estado"] == 1]
    elif estado == "Riesgo":
        df = df[df["Estado"] == 0]

    # 🎯 Filtro por grupo
    grupos = sorted(df["Grupo"].dropna().unique())
    grupo = st.sidebar.selectbox("Grupo", ["Todos"] + list(grupos))

    if grupo != "Todos":
        df = df[df["Grupo"] == grupo]

    # 🔍 Búsqueda
    buscar = st.sidebar.text_input("Buscar alumno")

    if buscar:
        df = df[df["Nombre"].str.contains(buscar, case=False, na=False)]

    return df

    return df
