import streamlit as st
import pandas as pd
from servicios import SERVICIOS

# =====================
# CONFIG
# =====================
st.set_page_config(
    page_title="RF Servicios",
    layout="wide"
)

st.title("📋 RF – Gestión de Servicios")

# =====================
# FUNCIONES
# =====================
def formatear_tiempo(minutos: int) -> str:
    if minutos < 60:
        return f"{minutos} min"

    horas = minutos // 60
    resto = minutos % 60

    if resto == 0:
        return "1 hora" if horas == 1 else f"{horas} horas"

    return f"{horas} h {resto} min"

# =====================
# SESSION STATE
# =====================
if "carrito" not in st.session_state:
    st.session_state.carrito = []

# =====================
# BUSCADOR SERVICIOS
# =====================
labels = {
    i: f"{s['id']} — {s['nombre']}"
    for i, s in enumerate(SERVICIOS)
}

# =====================
# LAYOUT PRINCIPAL
# =====================
col_left, col_right = st.columns([3, 2])

# =====================
# COLUMNA IZQUIERDA
# =====================
with col_left:
    st.subheader("🔍 Selección de servicio")

    idx = st.selectbox(
        "Busca y selecciona un servicio",
        options=list(labels.keys()),
        format_func=lambda i: labels[i]
    )

    servicio = SERVICIOS[idx]

    cantidad = st.number_input(
        "Cantidad",
        min_value=1,
        step=1,
        value=1
    )

    tiempo_total = servicio["tiempo_min"] * cantidad

    st.divider()

    st.subheader(servicio["nombre"])

    st.markdown("**Descripción**")
    st.info(servicio["descripcion"])

    c1, c2, c3 = st.columns(3)
    c1.metric("⏱ Unitario", formatear_tiempo(servicio["tiempo_min"]))
    c2.metric("📦 Cantidad", cantidad)
    c3.metric("⌛ Total", formatear_tiempo(tiempo_total))

    if st.button("➕ Agregar al RF", use_container_width=True):
        st.session_state.carrito.append({
            "Servicio": servicio["nombre"],
            "Cantidad": cantidad,
            "Tiempo unitario (min)": servicio["tiempo_min"],
            "Tiempo total (min)": tiempo_total
        })
        st.success("Servicio agregado al RF")

# =====================
# COLUMNA DERECHA – RF
# =====================
with col_right:
    st.subheader("📦 RF Actual")

    if st.session_state.carrito:
        df = pd.DataFrame(st.session_state.carrito)

        df["Tiempo unitario"] = df["Tiempo unitario (min)"].apply(formatear_tiempo)
        df["Tiempo total"] = df["Tiempo total (min)"].apply(formatear_tiempo)

        st.dataframe(
            df[["Servicio", "Cantidad", "Tiempo unitario", "Tiempo total"]],
            hide_index=True,
            use_container_width=True,
            height=350
        )

        total_rf = df["Tiempo total (min)"].sum()
        st.metric("⏱ Total RF", formatear_tiempo(total_rf))

        st.divider()

        idx_delete = st.selectbox(
            "Eliminar servicio",
            options=range(len(st.session_state.carrito)),
            format_func=lambda i: st.session_state.carrito[i]["Servicio"]
        )

        if st.button("🗑️ Eliminar seleccionado", use_container_width=True):
            st.session_state.carrito.pop(idx_delete)
            st.rerun()

    else:
        st.info("Aún no has agregado servicios al RF")
