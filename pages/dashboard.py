import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Smart Irrigation",
    page_icon="🌱",
    layout="wide"
)

# ============================================================
# ESTILOS
# ============================================================

st.markdown("""
<style>

    /* Fondo general */
    .stApp {
        background-color: #f7faf9;
    }

    /* Título */
    .main-title {
        font-size: 42px;
        font-weight: 700;
        color: #182b3a;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 18px;
        color: #6b7c88;
        margin-top: -8px;
        margin-bottom: 30px;
    }

    /* Tarjetas */
    .card {
        background-color: white;
        border: 1px solid #dfe7e4;
        border-radius: 18px;
        padding: 25px;
        height: 190px;
        box-shadow: 0px 3px 12px rgba(0,0,0,0.04);
    }

    .card-title {
        font-size: 17px;
        color: #657782;
        font-weight: 600;
        margin-bottom: 15px;
    }

    .card-value {
        font-size: 40px;
        font-weight: 700;
        color: #182b3a;
    }

    .card-description {
        font-size: 14px;
        color: #83919a;
        margin-top: 8px;
    }

    /* Estado */
    .status-active {
        background-color: #dceefe;
        border-radius: 14px;
        padding: 20px 25px;
        color: #1164a3;
        font-size: 18px;
        margin-top: 25px;
        margin-bottom: 30px;
    }

    .status-normal {
        background-color: #e1f5e9;
        border-radius: 14px;
        padding: 20px 25px;
        color: #18834b;
        font-size: 18px;
        margin-top: 25px;
        margin-bottom: 30px;
    }

    /* Modo simulación */
    .simulation {
        background-color: #fff5d9;
        border: 1px solid #f1d58b;
        border-radius: 12px;
        padding: 12px 18px;
        color: #80621b;
        margin-bottom: 25px;
        font-size: 14px;
    }

    /* Estado del sistema */
    .system-box {
        background-color: white;
        border: 1px solid #dfe7e4;
        border-radius: 16px;
        padding: 20px;
        margin-top: 10px;
    }

    .system-title {
        font-size: 20px;
        font-weight: 700;
        color: #182b3a;
        margin-bottom: 15px;
    }

    .system-item {
        font-size: 16px;
        color: #344955;
        margin: 12px 0;
    }

    /* Animación gota */
    .drop {
        display: inline-block;
        animation: dropAnimation 1s infinite;
    }

    @keyframes dropAnimation {
        0% {
            transform: translateY(-6px);
            opacity: 0.4;
        }

        50% {
            transform: translateY(5px);
            opacity: 1;
        }

        100% {
            transform: translateY(-6px);
            opacity: 0.4;
        }
    }

    /* Planta */
    .plant {
        font-size: 42px;
        animation: plantAnimation 2s infinite ease-in-out;
    }

    @keyframes plantAnimation {
        0% {
            transform: rotate(-2deg);
        }

        50% {
            transform: rotate(2deg);
        }

        100% {
            transform: rotate(-2deg);
        }
    }

</style>
""", unsafe_allow_html=True)

# ============================================================
# ESTADO DE LA SIMULACIÓN
# ============================================================

if "humedad" not in st.session_state:
    st.session_state.humedad = 35.0

if "umbral" not in st.session_state:
    st.session_state.umbral = 40

if "historial" not in st.session_state:
    st.session_state.historial = []

if "ultima_actualizacion" not in st.session_state:
    st.session_state.ultima_actualizacion = time.time()

# ============================================================
# SIMULACIÓN DE HUMEDAD
# ============================================================

ahora = time.time()

# Actualizamos aproximadamente cada segundo
if ahora - st.session_state.ultima_actualizacion >= 1:

    humedad = st.session_state.humedad
    umbral = st.session_state.umbral

    # --------------------------------------------------------
    # Si está seco → regamos → humedad aumenta
    # --------------------------------------------------------

    if humedad < umbral:

        humedad += np.random.uniform(0.4, 1.3)

    # --------------------------------------------------------
    # Si ya hay suficiente humedad → deja de regar
    # y lentamente vuelve a bajar
    # --------------------------------------------------------

    else:

        humedad -= np.random.uniform(0.1, 0.5)

    humedad = max(0, min(100, humedad))

    st.session_state.humedad = humedad

    # Guardar historial
    st.session_state.historial.append({
        "Hora": datetime.now().strftime("%H:%M:%S"),
        "Humedad": round(humedad, 1)
    })

    # Mantener solamente las últimas 30 lecturas
    if len(st.session_state.historial) > 30:
        st.session_state.historial.pop(0)

    st.session_state.ultima_actualizacion = ahora

# ============================================================
# VARIABLES
# ============================================================

humedad = st.session_state.humedad
umbral = st.session_state.umbral

valvula_abierta = humedad < umbral

# ============================================================
# TÍTULO
# ============================================================

st.markdown(
    '<div class="main-title">🌱 Smart Irrigation</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Monitoreo remoto del sistema de riego</div>',
    unsafe_allow_html=True
)

# ============================================================
# AVISO DE SIMULACIÓN
# ============================================================

st.markdown("""
<div class="simulation">
    🧪 <b>MODO SIMULACIÓN</b> — Los datos mostrados actualmente
    son generados automáticamente para representar el comportamiento
    esperado del sistema físico.
</div>
""", unsafe_allow_html=True)

# ============================================================
# TARJETAS PRINCIPALES
# ============================================================

col1, col2, col3 = st.columns(3)

# ------------------------------------------------------------
# HUMEDAD
# ------------------------------------------------------------

with col1:

    st.markdown(f"""
    <div class="card">

        <div class="card-title">
            💧 Humedad actual
        </div>

        <div class="card-value">
            {humedad:.0f}%
        </div>

        <div class="card-description">
            Lectura del sensor de humedad
        </div>

    </div>
    """, unsafe_allow_html=True)


# ------------------------------------------------------------
# UMBRAL
# ------------------------------------------------------------

with col2:

    st.markdown(f"""
    <div class="card">

        <div class="card-title">
            🎯 Umbral configurado
        </div>

        <div class="card-value">
            {umbral}%
        </div>

        <div class="card-description">
            Nivel mínimo de humedad
        </div>

    </div>
    """, unsafe_allow_html=True)


# ------------------------------------------------------------
# VÁLVULA
# ------------------------------------------------------------

with col3:

    if valvula_abierta:

        estado = "💧 ABIERTA"
        descripcion = "Riego actualmente activo"

    else:

        estado = "🔒 CERRADA"
        descripcion = "Riego detenido"

    st.markdown(f"""
    <div class="card">

        <div class="card-title">
            🚿 Estado de válvula
        </div>

        <div class="card-value">
            {estado}
        </div>

        <div class="card-description">
            {descripcion}
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# ESTADO DEL RIEGO
# ============================================================

if valvula_abierta:

    st.markdown("""
    <div class="status-active">

        <span class="drop">💧</span>

        <b> RIEGO ACTIVO</b>

        — La humedad está por debajo del umbral.

    </div>
    """, unsafe_allow_html=True)

else:

    st.markdown("""
    <div class="status-normal">

        🌱 <b>HUMEDAD ADECUADA</b>

        — El riego está detenido.

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# GRÁFICA
# ============================================================

st.subheader("📈 Historial de humedad")

if len(st.session_state.historial) > 0:

    df = pd.DataFrame(st.session_state.historial)

    df = df.set_index("Hora")

    st.line_chart(
        df["Humedad"],
        height=300
    )

else:

    st.info("Esperando datos de humedad...")


# ============================================================
# ESTADO DEL SISTEMA
# ============================================================

st.subheader("🔌 Estado del sistema")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Arduino",
        "SIMULADO"
    )

with col2:

    st.metric(
        "Sensor",
        "FUNCIONANDO"
    )

with col3:

    st.metric(
        "Válvula",
        "ABIERTA" if valvula_abierta else "CERRADA"
    )

with col4:

    st.metric(
        "Comunicación",
        "SIMULADA"
    )


# ============================================================
# INFORMACIÓN DEL CULTIVO
# ============================================================

st.subheader("🌱 Estado del cultivo")

col1, col2 = st.columns([1, 3])

with col1:

    st.markdown(
        '<div class="plant">🌱</div>',
        unsafe_allow_html=True
    )

with col2:

    if humedad < 25:

        mensaje = "El suelo está muy seco. El sistema necesita regar."

    elif humedad < umbral:

        mensaje = "El suelo está seco. El riego está activado."

    elif humedad < 70:

        mensaje = "La humedad se encuentra en un rango adecuado."

    else:

        mensaje = "El suelo presenta un nivel alto de humedad."

    st.write(mensaje)


# ============================================================
# ACTUALIZACIÓN AUTOMÁTICA
# ============================================================

time.sleep(1)

st.rerun()
