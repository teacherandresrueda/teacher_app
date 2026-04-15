import streamlit as st

def show_dojo(df):
    st.subheader("🎮 Modo Clase en Vivo")

    # 🎨 colores por equipo
    color_equipo = {
        "🔥 Rojo": "#FF4B4B",
        "💧 Azul": "#4B8BFF",
        "🌱 Verde": "#00FF9C",
        "⚡ Amarillo": "#FFD700"
    }

    # 🔥 estado persistente
    if "data" not in st.session_state:
        st.session_state.data = df.copy()

    data = st.session_state.data

    grupos = data["Grupo"].unique()

    for grupo in grupos:
        st.markdown(f"### 📘 Grupo {grupo}")

        grupo_df = data[data["Grupo"] == grupo]

        for i, row in grupo_df.iterrows():

            col1, col2, col3, col4 = st.columns([4,1,1,1])

            # 👤 nombre + color equipo
            with col1:
                bg = color_equipo.get(row["Equipo"], "#CCCCCC")
                st.markdown(f"""
                <div style="background-color:{bg}; padding:8px; border-radius:8px;">
                {row['Alumno']}
                </div>
                """, unsafe_allow_html=True)

            # ⭐ puntos
            with col2:
                st.write(f"⭐ {row['Puntos']}")

            # ➕ sumar
            with col3:
                if st.button("➕", key=f"plus_{i}"):
                    st.session_state.data.at[i, "Puntos"] += 1
                    st.session_state.data.at[i, "Estado"] = 1
                    st.rerun()

            # ➖ restar
            with col4:
                if st.button("➖", key=f"minus_{i}"):
                    st.session_state.data.at[i, "Puntos"] = max(
                        0, st.session_state.data.at[i, "Puntos"] - 1
                    )
                    st.rerun()

    return st.session_state.data
