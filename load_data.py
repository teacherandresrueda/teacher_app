import pandas as pd

def load_data():
    df = pd.read_csv("data/Log_Unificado.csv")
    df["Estado"] = df["Estado"].astype(int)
    return df
  import pandas as pd

def load_data():
    df = pd.read_csv("data/Log_Unificado.csv")
    df["Estado"] = df["Estado"].astype(int)
    return df
  import streamlit as st

def show_metrics(df):
    col1, col2, col3 = st.columns(3)

    total = df["Alumno"].nunique()
    activos = df["Estado"].sum()
    riesgo = len(df[df["Estado"] == 0])

    col1.metric("👥 Total", total)
    col2.metric("✅ Activos", activos)
    col3.metric("🚨 Riesgo", riesgo)
  import streamlit as st

def show_dashboard(df):
    st.subheader("📊 Rendimiento por grupo")
    data = df.groupby("Grupo")["Estado"].mean()
    st.bar_chart(data)
  import streamlit as st

def show_alerts(df):
    st.subheader("🚨 Alertas")

    alertas = df[df["Estado"] == 0]

    st.dataframe(alertas, use_container_width=True)
import streamlit as st

def show_dojo(df):
    st.subheader("🎮 ClassDojo View")

    for grupo in df["Grupo"].unique():
        st.markdown(f"### 📘 Grupo {grupo}")

        grupo_df = df[df["Grupo"] == grupo]

        cols = st.columns(5)

        for i, row in grupo_df.iterrows():
            color = "#00ff88" if row["Estado"] == 1 else "#ff4b4b"

            cols[i % 5].markdown(
                f"""
                <div style="
                    background-color: {color};
                    padding: 10px;
                    border-radius: 12px;
                    text-align: center;
                    color: black;
                ">
                    <strong>{row['Alumno']}</strong><br>
                    ⭐ {row['Puntos']}
                </div>
                """,
                unsafe_allow_html=True
            )
          body {
    background-color: #0e1117;
    color: white;
}
body {
    background-color: #0e1117;
    color: white;
}APP_NAME = "Teacher Control Pro"
MAX_POINTS = 12
RISK_THRESHOLD = 3
