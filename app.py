import streamlit as st
import pandas as pd

st.title("⚡ Academic Intelligence System")

# CARGA DE DATOS
uploaded_file = st.file_uploader("Upload ClassDojo report", type=["csv", "xlsx"])

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("Data loaded successfully")

    col1, col2 = st.columns(2)

    col1.metric("Students", len(df))
    col2.metric("Columns", len(df.columns))

    st.dataframe(df)

else:
    st.warning("Upload your student file to begin")
