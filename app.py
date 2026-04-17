import streamlit as st
import pandas as pd

st.title("📚 Class Manager")

opcion = st.selectbox("Selecciona una opción", [
    "Crear clase",
    "Importar lista",
    "Ver alumnos"
])

if opcion == "Crear clase":
    nombre_clase = st.text_input("Nombre de la clase")
    if st.button("Crear"):
        st.success(f"Clase '{nombre_clase}' creada")

elif opcion == "Importar lista":
    archivo = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

    if archivo:
        df = pd.read_excel(archivo)
        st.write("Vista previa:")
        st.dataframe(df)

        if st.button("Guardar lista"):
            st.success("Lista importada correctamente")

elif opcion == "Ver alumnos":
    st.info("Aquí se mostrarán los alumnos guardados")
