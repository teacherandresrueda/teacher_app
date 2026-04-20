import streamlit as st
import pandas as pd
import os

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Academic Intelligence System", layout="wide")

st.title("⚡ Academic Intelligence System")

# =========================
# DATA FILE
# =========================
DATA_FILE = "data/students.csv"

# =========================
# LOAD BASE DATA
# =========================
if "df" not in st.session_state:
    if os.path.exists(DATA_FILE):
        st.session_state.df = pd.read_csv(DATA_FILE)
    else:
        st.session_state.df = pd.DataFrame(columns=["Nombre", "Puntos"])

df = st.session_state.df

# =========================
# FUNCTION: DETECT NAME COLUMN
# =========================
def find_name_column(columns):
    possible = ["Nombre", "Name", "Student", "Alumno"]
    for col in columns:
        if col.strip() in possible:
            return col
    return None

# =========================
# MULTI FILE UPLOADER
# =========================
uploaded_files = st.file_uploader(
    "Upload ClassDojo reports (multiple allowed)",
    type=["csv"],
    accept_multiple_files=True
)

if uploaded_files:
    dfs = []

    for file in uploaded_files:
        temp_df = pd.read_csv(file)

        # Detect name column
        name_col = find_name_column(temp_df.columns)

        if name_col is None:
            st.error(f"No name column found in {file.name}")
            st.write("Columns detected:", list(temp_df.columns))
            continue

        temp_df = temp_df.rename(columns={name_col: "Nombre"})
        temp_df["group"] = file.name

        dfs.append(temp_df)

    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)

        # Create Puntos if not exists
        if "Puntos" not in combined_df.columns:

            pos_cols = [c for c in combined_df.columns if "positivo" in c.lower()]
            neg_cols = [c for c in combined_df.columns if "negativo" in c.lower() or "necesita" in c.lower()]

            combined_df["Puntos"] = 0

            if pos_cols:
                combined_df["Puntos"] += combined_df[pos_cols].sum(axis=1)

            if neg_cols:
                combined_df["Puntos"] -= combined_df[neg_cols].sum(axis=1)

        combined_df = combined_df[["Nombre", "Puntos"]]
        combined_df = combined_df.groupby("Nombre", as_index=False).sum()

        st.session_state.df = combined_df

        os.makedirs("data", exist_ok=True)
        st.session_state.df.to_csv(DATA_FILE, index=False)

        df = st.session_state.df

        st.success("Files loaded successfully ⚡")

# =========================
# MENU
# =========================
menu = st.sidebar.radio("Menu", [
    "Dashboard",
    "Student Intelligence",
    "Alerts Center",
    "Reports"
])

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":

    st.header("Overview")

    col1, col2 = st.columns(2)

    if not df.empty:
        col1.metric("Students", df["Nombre"].nunique())
        col2.metric("Total Points", int(df["Puntos"].sum()))
    else:
        col1.metric("Students", 0)
        col2.metric("Total Points", 0)

    st.dataframe(df)

# =========================
# STUDENT INTELLIGENCE
# =========================
elif menu == "Student Intelligence":

    st.header("Student Intelligence")

    if df.empty:
        st.warning("No students loaded")
    else:
        students = df["Nombre"].unique()

        col1, col2 = st.columns(2)

        student = col1.selectbox("Select student", students)

        puntos = col2.number_input("Points (+ / -)", step=1, value=0)

        if st.button("Apply Points ⚡"):

            idx = df[df["Nombre"] == student].index

            if len(idx) > 0:
                st.session_state.df.loc[idx, "Puntos"] += puntos
            else:
                new_row = pd.DataFrame([[student, puntos]], columns=["Nombre", "Puntos"])
                st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)

            os.makedirs("data", exist_ok=True)
            st.session_state.df.to_csv(DATA_FILE, index=False)

            st.success(f"{puntos} points applied to {student}")

# =========================
# ALERTS CENTER
# =========================
elif menu == "Alerts Center":

    st.header("🚨 Alerts Center")

    if df.empty:
        st.warning("No data")
    else:
        for i, row in df.iterrows():
            if row["Puntos"] < 0:
                st.error(f"{row['Nombre']} → Needs attention")

# =========================
# REPORTS
# =========================
elif menu == "Reports":

    st.header("📊 Reports")

    if df.empty:
        st.warning("No data")
    else:
        st.dataframe(df)

        st.download_button(
            "Download CSV",
            df.to_csv(index=False),
            "report.csv",
            "text/csv"
        )
