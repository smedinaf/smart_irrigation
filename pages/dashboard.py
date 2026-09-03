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
# ESTILO VISUAL
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #f7faf9;
}

h1 {
    color: #182b3a;
}

h2, h3 {
    color: #182b3a;
}

.block-container {
    padding-top: 3rem;
    padding-bottom: 3rem;
}

[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #dfe7e4;
    padding: 20px;
    border-radius: 16px;
}

[data-testid="stMetricValue"] {
    color: #182b3a;
}

.simulacion {
    background-color: #fff5d9;
    border: 1px solid #f1d58b;
    padding: 14px 18px;
    border-radius: 12px;
    margin-bottom: 25px;
}

.riego {
    background-color: #dceefe;
    border: 1px solid #b9d8f5;
    padding: 18px;
    border-radius: 14px;
    color: #1164a3;
    font-size: 18px;
    margin: 20px 0;
}

.normal {
    background-color: #e1f5e9;
    border: 1px solid #bde4cb;
    padding: 18px;
    border-radius: 14px;
    color: #18834b;
    font-size: 18px;
    margin: 20px 0;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# VARIABLES INICIALES
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
# SIMULACIÓN DEL SENSOR
# ============================================================

ahora = time.time()

if ahora - st.session_state.ultima_actualizacion >= 1:

    humedad = st.session_state.humedad
    umbral = st.session_state.umbral

    # --------------------------------------------------------
    # SUELO SECO → SE ACTIVA EL RIEGO
    # --------------------------------------------------------

    if humedad < umbral:

        humedad += np.random.uniform(0.5, 1.5)

    # --------------------------------------------------------
    # SUELO HÚMEDO → EL RIEGO SE DETIENE
    # --------------------------------------------------------

    else:

        humedad -= np.random.uniform(0.1, 0.5)

    humedad = max(0, min(100, humedad))

    st.session_state.humedad = humedad

    # Guardar lectura
    st.session_state.historial.append({
        "Hora": datetime.now().strftime("%H:%M:%S"),
        "Humedad": round(humedad, 1)
    })

    # Mantener las últimas 30 lecturas
    if len(st.session_state.historial) > 30:
        st.session_state.historial.pop(0)

    st.session_state.ultima_actualizacion = ahora

# ============================================================
# DATOS ACTUALES
# ============================================================

humedad = st.session_state.humedad
umbral = st.session_state.umbral

valvula_abierta = humedad < umbral

# ============================================================
# ENCABEZADO
# ============================================================

st.title("🌱 Smart Irrigation")

st.write(
    "Monitoreo remoto del sistema de riego"
)

st.divider()

# ============================================================
# MODO SIMULACIÓN
# ============================================================

st.info(
    "🧪 MODO SIMULACIÓN — Los datos mostrados actualmente "
    "son generados automáticamente para representar el "
    "comportamiento esperado del sistema físico."
)

# ============================================================
# TARJETAS PRINCIPALES
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        label="💧 Humedad actual",
        value=f"{humedad:.0f}%",
        delta=f"{humedad - umbral:.0f}% respecto al umbral"
    )

with col2:

    st.metric(
        label="🎯 Umbral configurado",
        value=f"{umbral}%"
    )

with col3:

    if valvula_abierta:

        st.metric(
            label="🚿 Estado de válvula",
            value="ABIERTA",
            delta="Riego activo"
        )

    else:

        st.metric(
            label="🚿 Estado de válvula",
            value="CERRADA",
            delta="Riego detenido"
        )

# ============================================================
# ESTADO DEL RIEGO
# ============================================================

if valvula_abierta:

    st.markdown(
        '<div class="riego">'
        '💧 <b>RIEGO ACTIVO</b><br>'
        'La humedad está por debajo del umbral. '
        'La válvula está abierta.'
        '</div>',
        unsafe_allow_html=True
    )

else:

    st.markdown(
        '<div class="normal">'
        '🌱 <b>HUMEDAD ADECUADA</b><br>'
        'El nivel de humedad es suficiente. '
        'La válvula permanece cerrada.'
        '</div>',
        unsafe_allow_html=True
    )

# ============================================================
# BARRA DE HUMEDAD
# ============================================================

st.subheader("💧 Nivel de humedad")

st.progress(
    int(humedad)
)

st.caption(
    f"Humedad actual: {humedad:.1f}%"
)

# ============================================================
# HISTORIAL
# ============================================================

st.subheader("📈 Historial de humedad")

if len(st.session_state.historial) > 1:

    df = pd.DataFrame(
        st.session_state.historial
    )

    df = df.set_index("Hora")

    st.line_chart(
        df["Humedad"],
        height=300
    )

else:

    st.info(
        "Recopilando datos para generar el historial..."
    )

# ============================================================
# ESTADO DEL SISTEMA
# ============================================================

st.subheader("🔌 Estado del sistema")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.success("🟢 Arduino\n\nSIMULADO")

with col2:

    st.success("🟢 Sensor\n\nFUNCIONANDO")

with col3:

    if valvula_abierta:
        st.info("💧 Válvula\n\nABIERTA")
    else:
        st.success("🔒 Válvula\n\nCERRADA")

with col4:

    st.success("🟢 Comunicación\n\nSIMULADA")

# ============================================================
# ESTADO DEL CULTIVO
# ============================================================

st.subheader("🌱 Estado del cultivo")

if humedad < 25:

    st.warning(
        "🌵 El suelo está muy seco. "
        "El sistema mantiene el riego activado."
    )

elif humedad < umbral:

    st.info(
        "💧 El suelo está seco. "
        "El sistema está realizando el riego automáticamente."
    )

elif humedad < 70:

    st.success(
        "🌱 El cultivo presenta un nivel de humedad adecuado."
    )

else:

    st.info(
        "💦 El suelo presenta un nivel alto de humedad."
    )

# ============================================================
# INFORMACIÓN DE SIMULACIÓN
# ============================================================

st.divider()

st.caption(
    "Smart Irrigation • Prototipo de monitoreo remoto • "
    "Modo demostración"
)

# ============================================================
# ACTUALIZACIÓN AUTOMÁTICA
# ============================================================

time.sleep(1)

st.rerun()
