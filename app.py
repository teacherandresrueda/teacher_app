import streamlit as st

st.set_page_config(page_title="Control de Grupos", layout="wide")

# -------------------------------
# 📊 BASE DE DATOS (TUS GRUPOS)
# -------------------------------

grupos = {
    "1D": [
        "Adán Tlaqueparo","Alexis Ramírez","Amairani Bernal","Antonio Rayas",
        "Camila Pérez","Camila Villegas","Dominic Bardales","Evelyn Alejandra",
        "Fernanda Roblero","Gabriel Rodríguez","Gael Gil","Iván Jiménez",
        "Jacqueline Rujerio","Javier Mejía","Jocelyn Rodríguez","Joshua Giovanni",
        "José Calderón","Leilani Oropesa","Montserrat Martínez","Regina Sánchez",
        "Renata Rosales","Sebastián Proa","Sebastián Álvarez","Sharon Ledezma",
        "Sofía Ponciano","Ulises Romero","Uriel García","Uriel López",
        "Violeta Martínez","Yael Herdanes","Yael Sánchez","Yair García",
        "Yamilex Rangel","Yazmín Lomas","Ángel Tapia"
    ],
    "1E": [
        "Aarón Hernández","Abril González","Aylin Martínez","Brandon López",
        "Dafne Ruiz","Diego Torres","Emiliano Cruz","Fernanda Gómez",
        "Gael Hernández","Ivanna López","Javier Sánchez","Jimena Flores",
        "José Luis Pérez","Juan Pablo Ramírez","Karen Morales","Luis Ángel Díaz",
        "María Fernanda Ruiz","Mateo Hernández","Mía González","Natalia López",
        "Renata Gómez","Rodrigo Sánchez","Sofía Hernández","Valeria Cruz",
        "Ximena López","Yael Torres"
    ],
    "1F": [
        "Ashely Aidee","Axel Torres","Daniel Quintana","Eduardo Vilchis",
        "Emiliano Luna","Evoleth Analy","Fernanda Amaya","Gael Galicia",
        "Gretel Alejandra","Gustavo Angel","Harumi Calixto","Iker Irán",
        "Ingrid Ximena","Jesús Adrian","Joaly Mendez","Lizeth Mariana",
        "Luis David","Luis Gerardo","Mariana Faloful","Mariana García",
        "Mateo Villas","Matias Arias","Renata Rosales","Támara Corona",
        "Ulises Eliot","Valeria Alejandra","Valeria Michel","Vanessa Negrete",
        "Vania Denisse","Violeta Sánchez","Yatziri Galán","Zoe Rangel"
    ],
    "2D": [
        "Abril Zarazua","Diego Sánchez","Franco David","Ian Mateo",
        "Iker Alexander","José De Jesús","Juan Pablo","Julian Barrera",
        "Javier Alejandro","Javier Resendis","Karla Alejandra","Karla Danae",
        "Leilany Pomar","Leonardo Zarazua","Luis Andrik","Mariana Trejo",
        "Michelle Alejandra","Martinez Navarrete","Michelle Angeline",
        "Natalia Isabel","Raciel Bolaños","Renata Rangel","Ruben García",
        "Sebastián Aguilar","Skarletth Flores","Valente Rodriguez",
        "Valeria Zoe","Ximena Anaya","Zuleyca Genoveva"
    ],
    "2E": [
        "Ailine Avalos","Aldo Yael Montero","America Yazmin Luna",
        "Brandon Mateo Morales","Briseyda Reyes","Britany Aidee Gonzalez",
        "Carlos Daniel Garcia","Christopher Alonso Mendez",
        "Derek Yael Gonzalez","Diego Montenegro","Dilan Rodrigo Bernal",
        "Elizabeth Martinez","Erandi Nicole Santiago",
        "Iker Alexander Carmona","Iker Noel Sanchez",
        "Iñaki Javier Martinez","Jorge Dario Cruz",
        "Juan Gabriel Rubio","Juan Manuel Ramirez",
        "Karla Jacqueline Castellanos","Karla Paola Vega",
        "Kerem Samantha Alonso","Kevin Mael Rojas",
        "Leilany Guadalupe Alcantara","Luis Angel Rodriguez",
        "Madeline Amelia Olvera","Maximo Alfonso Mar"
    ]
}

# -------------------------------
# 🎛️ INTERFAZ
# -------------------------------

st.title("📚 Control de Alumnos")

# Selector de grupo
grupo_seleccionado = st.selectbox("Selecciona un grupo", list(grupos.keys()))

# Buscador
busqueda = st.text_input("🔍 Buscar alumno")

# Lista base
alumnos = grupos[grupo_seleccionado]

# Filtro por búsqueda
if busqueda:
    alumnos = [a for a in alumnos if busqueda.lower() in a.lower()]

st.subheader(f"Grupo {grupo_seleccionado} ({len(alumnos)} alumnos)")

# Mostrar alumnos
for i, alumno in enumerate(alumnos):
    col1, col2 = st.columns([1, 4])
    with col1:
        st.write(f"{i+1}")
    with col2:
        st.write(alumno)

# -------------------------------
# ⚡ EXTRA: CONTROL SIMPLE (ASISTENCIA)
# -------------------------------

st.markdown("---")
st.subheader("✔️ Registro rápido")

asistencia = {}

for alumno in grupos[grupo_seleccionado]:
    asistencia[alumno] = st.checkbox(alumno, key=f"{grupo_seleccionado}_{alumno}")

# Botón de resumen
if st.button("📊 Ver resumen"):
    presentes = [a for a, v in asistencia.items() if v]
    st.success(f"Asistieron: {len(presentes)} alumnos")
    st.write(presentes)
