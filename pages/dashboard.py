import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


# ==========================================================
# ENCABEZADO
# ==========================================================

st.markdown(
    '<div class="main-title">🌱 Smart Irrigation</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Monitoreo remoto del sistema de riego'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================================
# DATOS ACTUALES
# ==========================================================

humedad = st.session_state.humedad
umbral = st.session_state.umbral
valvula = st.session_state.valvula


# ==========================================================
# TARJETAS PRINCIPALES
# ==========================================================

col1, col2, col3 = st.columns(3)


# ----------------------------------------------------------
# HUMEDAD
# ----------------------------------------------------------

with col1:

    st.markdown(
        f"""
        <div class="card">

            <div class="card-title">
                Humedad actual
            </div>

            <div class="card-value">
                {humedad}%
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(humedad / 100)


# ----------------------------------------------------------
# UMBRAL
# ----------------------------------------------------------

with col2:

    st.markdown(
        f"""
        <div class="card">

            <div class="card-title">
                Umbral configurado
            </div>

            <div class="card-value">
                {umbral}%
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ----------------------------------------------------------
# VÁLVULA
# ----------------------------------------------------------

with col3:

    if valvula == "ABIERTO":

        icono = "💧"

    else:

        icono = "⚪"

    st.markdown(
        f"""
        <div class="card">

            <div class="card-title">
                Estado de válvula
            </div>

            <div class="card-value">
                {icono} {valvula}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# MENSAJE DE ESTADO
# ==========================================================

st.write("")


if humedad < umbral:

    st.info(
        "💧 RIEGO ACTIVO — "
        "La humedad está por debajo del umbral."
    )

else:

    st.success(
        "✓ RIEGO DETENIDO — "
        "La humedad se encuentra en un nivel suficiente."
    )


# ==========================================================
# HISTORIAL DE HUMEDAD
# ==========================================================

st.markdown(
    '<div class="section-title">'
    'Historial de humedad'
    '</div>',
    unsafe_allow_html=True
)


ahora = datetime.now()


tiempos = [
    ahora - timedelta(minutes=5 * i)
    for i in range(12)
][::-1]


valores = [
    62,
    65,
    68,
    71,
    67,
    63,
    59,
    55,
    51,
    47,
    42,
    humedad
]


datos = pd.DataFrame(
    {
        "Humedad (%)": valores
    },
    index=tiempos
)


st.line_chart(
    datos,
    height=320
)


# ==========================================================
# INFORMACIÓN INFERIOR
# ==========================================================

col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Última lectura",
        ahora.strftime("%H:%M:%S")
    )


with col2:

    st.metric(
        "Estado del sistema",
        "ACTIVO"
    )
