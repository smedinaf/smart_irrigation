import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


# ==========================================================
# ENCABEZADO
# ==========================================================

st.markdown(
    '<div class="main-title">📡 Tiempo real</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Supervisión de las lecturas enviadas por el sistema'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================================
# DATOS
# ==========================================================

humedad = st.session_state.humedad
umbral = st.session_state.umbral
valvula = st.session_state.valvula


# ==========================================================
# MÉTRICAS
# ==========================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Humedad actual",
        f"{humedad}%"
    )


with col2:

    st.metric(
        "Umbral",
        f"{umbral}%"
    )


with col3:

    st.metric(
        "Válvula",
        valvula
    )


# ==========================================================
# ESTADO DEL SISTEMA
# ==========================================================

if humedad < umbral:

    st.warning(
        "⚠️ SUELO SECO — "
        "El sistema de riego está activado."
    )

else:

    st.success(
        "✓ HUMEDAD SUFICIENTE — "
        "El sistema de riego está detenido."
    )


# ==========================================================
# LECTURAS RECIENTES
# ==========================================================

st.subheader("Lecturas recientes")


ahora = datetime.now()


horas = [
    ahora - timedelta(seconds=i)
    for i in range(5)
][::-1]


valores = [
    humedad + 4,
    humedad + 3,
    humedad + 2,
    humedad + 1,
    humedad
]


tabla = pd.DataFrame(
    {
        "Hora": [
            hora.strftime("%H:%M:%S")
            for hora in horas
        ],

        "Humedad (%)": valores,

        "Estado": [
            "ABIERTO"
            if valor < umbral
            else "CERRADO"

            for valor in valores
        ]
    }
)


st.dataframe(
    tabla,
    use_container_width=True,
    hide_index=True
)


# ==========================================================
# ACTUALIZAR
# ==========================================================

st.write("")


if st.button(
    "↻ Actualizar lectura",
    use_container_width=True
):

    st.rerun()


st.caption(
    "La actualización automática se conectará "
    "posteriormente con los datos reales del Arduino."
)
