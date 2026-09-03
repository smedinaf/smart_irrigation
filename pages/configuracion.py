import streamlit as st


# ==========================================================
# ENCABEZADO
# ==========================================================

st.markdown(
    '<div class="main-title">⚙️ Configuración</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Configuración del umbral de humedad'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================================
# EXPLICACIÓN
# ==========================================================

st.subheader("Umbral de humedad")

st.write(
    "El sistema activa el riego cuando "
    "la humedad está por debajo de este valor."
)


# ==========================================================
# BOTONES − Y +
# ==========================================================

col1, col2, col3 = st.columns([1, 2, 1])


# ----------------------------------------------------------
# DISMINUIR
# ----------------------------------------------------------

with col1:

    if st.button(
        "−",
        use_container_width=True
    ):

        st.session_state.umbral = max(
            5,
            st.session_state.umbral - 5
        )

        st.rerun()


# ----------------------------------------------------------
# VALOR
# ----------------------------------------------------------

with col2:

    st.markdown(
        f"""
        <div style="
            text-align:center;
            font-size:3rem;
            font-weight:700;
            padding:0.5rem;
        ">

            {st.session_state.umbral}%

        </div>
        """,
        unsafe_allow_html=True
    )


# ----------------------------------------------------------
# AUMENTAR
# ----------------------------------------------------------

with col3:

    if st.button(
        "+",
        use_container_width=True
    ):

        st.session_state.umbral = min(
            95,
            st.session_state.umbral + 5
        )

        st.rerun()


# ==========================================================
# SLIDER
# ==========================================================

nuevo_umbral = st.slider(
    "Seleccionar umbral",
    min_value=5,
    max_value=95,
    value=st.session_state.umbral,
    step=5
)


if nuevo_umbral != st.session_state.umbral:

    st.session_state.umbral = nuevo_umbral


# ==========================================================
# ESTADO DEL SISTEMA
# ==========================================================

st.divider()

st.subheader("Estado del sistema")


col1, col2 = st.columns(2)


with col1:

    st.write("⚙️ Modo")
    st.success("AUTOMÁTICO")

    st.write("🌱 Sensor")
    st.success("FUNCIONANDO")


with col2:

    st.write("🔌 Comunicación")
    st.success("ACTIVA")

    st.write("💧 Válvula")
    st.info(st.session_state.valvula)


# ==========================================================
# NOTA
# ==========================================================

st.info(
    "En la versión final, este valor se sincronizará "
    "con el umbral configurado directamente en el Arduino."
)
