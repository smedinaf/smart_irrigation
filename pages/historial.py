import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


# ==========================================================
# ENCABEZADO
# ==========================================================

st.markdown(
    '<div class="main-title">📈 Historial</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Comportamiento histórico de la humedad del cultivo'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================================
# DATOS DE DEMOSTRACIÓN
# ==========================================================

ahora = datetime.now()


tiempos = [
    ahora - timedelta(minutes=10 * i)
    for i in range(13)
][::-1]


humedades = [
    78,
    74,
    70,
    67,
    64,
    61,
    57,
    53,
    49,
    44,
    39,
    36,
    st.session_state.humedad
]


datos = pd.DataFrame(
    {
        "Humedad (%)": humedades
    },
    index=tiempos
)


# ==========================================================
# GRÁFICA
# ==========================================================

st.subheader("Historial de humedad")


st.line_chart(
    datos,
    height=400
)


# ==========================================================
# ESTADÍSTICAS
# ==========================================================

st.subheader("Resumen")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Humedad promedio",
        f"{datos['Humedad (%)'].mean():.0f}%"
    )


with col2:

    st.metric(
        "Humedad mínima",
        f"{datos['Humedad (%)'].min():.0f}%"
    )


with col3:

    st.metric(
        "Humedad máxima",
        f"{datos['Humedad (%)'].max():.0f}%"
    )


# ==========================================================
# RESUMEN DEL DÍA
# ==========================================================

st.divider()

st.subheader("Resumen del día")


col1, col2 = st.columns(2)


with col1:

    st.write(
        "💧 Tiempo total de riego: **12 min**"
    )

    st.write(
        "🔄 Activaciones del riego: **4**"
    )


with col2:

    st.write(
        "🌱 Estado actual: **ACTIVO**"
    )

    st.write(
        "🎯 Umbral actual:",
        f"**{st.session_state.umbral}%**"
    )
