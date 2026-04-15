import pandas as pd
import os

def load_data():
    base_path = os.path.dirname(__file__)  # modules/
    root_path = os.path.abspath(os.path.join(base_path, ".."))  # teacher_app/
    
    file_path = os.path.join(root_path, "data", "Log_Unificado.csv")

    # 🔥 Debug visual (te ayuda en cloud)
    print("PATH:", file_path)

    # 🚨 Validaciones PRO
    if not os.path.exists(file_path):
        return pd.DataFrame({
            "Alumno": ["SIN ARCHIVO"],
            "Grupo": ["NA"],
            "Equipo": [0],
            "Puntos": [0],
            "Nivel": ["🔴"],
            "Estado": [0]
        })

    if os.path.isdir(file_path):
        return pd.DataFrame({
            "Alumno": ["ERROR: ES CARPETA"],
            "Grupo": ["NA"],
            "Equipo": [0],
            "Puntos": [0],
            "Nivel": ["🔴"],
            "Estado": [0]
        })

    # 🔥 Cargar archivo
    df = pd.read_csv(file_path)

    # 🔥 Limpieza total
    df.columns = df.columns.str.strip()

    required_cols = ["Alumno", "Grupo", "Equipo", "Puntos", "Nivel", "Estado"]

    for col in required_cols:
        if col not in df.columns:
            df[col] = 0

    df["Estado"] = pd.to_numeric(df["Estado"], errors="coerce").fillna(0).astype(int)
    df["Puntos"] = pd.to_numeric(df["Puntos"], errors="coerce").fillna(0)

    df["Alumno"] = df["Alumno"].astype(str)
    df["Grupo"] = df["Grupo"].astype(str)

    return df
