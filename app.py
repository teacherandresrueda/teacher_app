import streamlit as st
from modules.load_data import load_data
from modules.filters import apply_filters
from modules.metrics import show_metrics
from modules.dashboard import show_dashboard
from modules.alerts import show_alerts
from modules.dojo_view import show_dojo

# =========================
# CONFIGURACIÓN GENERAL
# =========================
st.set_page_config(
    page_title="Teacher Control Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# HEADER
# =========================
st.title("📊 Teacher Control System")
st.caption("Dashboard inteligente tipo ClassDojo")

# =========================
# CARGA DE DATOS (SEGURA)
# =========================
try:
    df = load_data()
except Exception as e:
    st.error("❌ Error cargando datos")
    st.exception(e)
    st.stop()

# =========================
# VALIDACIÓN DE DATOS
# =========================
if df is None or df.empty:
    st.warning("⚠️ No hay datos disponibles. Verifica el archivo CSV.")
    st.stop()

# =========================
# FILTROS
# =========================
df = apply_filters(df)

# =========================
# KPIs
# =========================
show_metrics(df)

st.divider()

# =========================
# DASHBOARD
# =========================
show_dashboard(df)

st.divider()

# =========================
# ALERTAS
# =========================
show_alerts(df)

st.divider()

# =========================
# VISTA VISUAL TIPO DOJO
# =========================
show_dojo(df)

# =========================
# FOOTER
# =========================
st.divider()
st.caption("🚀 Teacher App Pro | Sistema de análisis educativo")
