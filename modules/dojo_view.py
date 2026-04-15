import streamlit as st

def show_dojo(df):
    st.subheader("Vista tipo ClassDojo")

    grupos = df["Grupo"].unique()

    for grupo in grupos:
        st.markdown(f"### Grupo {grupo}")

        grupo_df = df[df["Grupo"] == grupo]

        cols = st.columns(5)

        for i, row in grupo_df.iterrows():
            # 🎯 Color basado en puntos
            if row["Puntos"] >= 7:
                color = "#00FF9C"
            elif row["Puntos"] >= 4:
                color = "#FFD700"
            else:
                color = "#FF4B4B"

            # 📦 Tarjeta visual
            with cols[i % 5]:
                st.markdown(f"""
                <div style="
                    background-color:{color};
                    padding:15px;
                    border-radius:15px;
                    text-align:center;
                    margin-bottom:10px;
                    color:black;
                    font-weight:bold;
                ">
                    {row["Nombre"]}<br>
                    ⭐ {row["Puntos"]}
                </div>
                """, unsafe_allow_html=True)
