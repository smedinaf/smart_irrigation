import streamlit as st


# ==========================================================
# CONFIGURACIÓN GENERAL
# ==========================================================

st.set_page_config(
    page_title="Smart Irrigation",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# ESTILOS GENERALES
# ==========================================================

st.markdown("""
<style>

    /* Fondo principal */
    .stApp {
        background-color: #f7f9f8;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e3e7e5;
    }

    /* Título */
    .main-title {
        font-size: 2.4rem;
        font-weight: 700;
        color: #1f2933;
        margin-bottom: 0;
    }

    /* Subtítulo */
    .subtitle {
        font-size: 1rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }

    /* Tarjetas */
    .card {
        background-color: white;
        border: 1px solid #e1e5e3;
        border-radius: 16px;
        padding: 1.5rem;
        min-height: 150px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    .card-title {
        color: #6b7280;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .card-value {
        color: #1f2933;
        font-size: 2.4rem;
        font-weight: 700;
        margin-top: 0.5rem;
    }

    /* Títulos de sección */
    .section-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #1f2933;
        margin-top: 1rem;
    }

    /* Estado online */
    .online {
        color: #16a34a;
        font-weight: 600;
    }

</style>
""", unsafe_allow_html=True)


# ==========================================================
# VARIABLES GLOBALES
# ==========================================================

if "humedad" not in st.session_state:
    st.session_state.humedad = 35

if "umbral" not in st.session_state:
    st.session_state.umbral = 40

if "valvula" not in st.session_state:
    st.session_state.valvula = "ABIERTO"


# ==========================================================
# PÁGINAS
# ==========================================================

dashboard = st.Page(
    "pages/dashboard.py",
    title="Dashboard",
    icon="🏠"
)

tiempo_real = st.Page(
    "pages/real_time.py",
    title="Tiempo real",
    icon="📡"
)

configuracion = st.Page(
    "pages/configuracion.py",
    title="Configuración",
    icon="⚙️"
)

historial = st.Page(
    "pages/historial.py",
    title="Historial",
    icon="📈"
)


# ==========================================================
# SISTEMA DE NAVEGACIÓN
# ==========================================================

pg = st.navigation([
    dashboard,
    tiempo_real,
    configuracion,
    historial
])


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown("## 🌱 Smart Irrigation")

    st.caption(
        "Sistema interactivo de control "
        "de humedad para cultivos"
    )

    st.divider()

    st.markdown("### Estado del sistema")

    st.markdown(
        '<p class="online">🟢 Arduino — CONECTADO</p>',
        unsafe_allow_html=True
    )

    st.write("🟢 Sensor — FUNCIONANDO")

    if st.session_state.valvula == "ABIERTO":

        st.write("💧 Válvula — ABIERTA")

    else:

        st.write("⚪ Válvula — CERRADA")

    st.write("🟢 Comunicación — ACTIVA")

    st.divider()

    st.caption("Smart Irrigation")
    st.caption("Prototipo académico")


# ==========================================================
# EJECUTAR PÁGINA
# ==========================================================

pg.run()
