import streamlit as st
import pandas as pd
from servicios import SERVICIOS

# =====================
# CONFIG
# =====================
st.set_page_config(
    page_title="RF Servicios",
    layout="wide",
    initial_sidebar_state="expanded"
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
# PREPARAR OPCIONES
# =====================
labels = [
    f"{s['id']} — {s['nombre']}"
    for s in SERVICIOS
]

# =====================
# SIDEBAR
# =====================
with st.sidebar:
    st.header("🛠️ Selección de servicio")

    idx = st.selectbox(
        "Buscar servicio",
        options=range(len(labels)),
        format_func=lambda i: labels[i]
    )

    servicio_sel = SERVICIOS[idx]

    cantidad = st.number_input(
        "Cantidad",
        min_value=1,
        step=1,
        value=1
    )

    tiempo_total = servicio_sel["tiempo_min"] * cantidad

    st.divider()
    st.markdown("### ⏱ Resumen")
    st.write(f"**Tiempo unitario:** {formatear_tiempo(servicio_sel['tiempo_min'])}")
    st.write(f"**Tiempo total:** {formatear_tiempo(tiempo_total)}")

    if st.button("➕ Agregar al RF", use_container_width=True):
        st.session_state.carrito.append({
            "Servicio": servicio_sel["nombre"],
            "Cantidad": cantidad,
            "Tiempo unitario (min)": servicio_sel["tiempo_min"],
            "Tiempo total (min)": tiempo_total
        })
        st.success("Servicio agregado al RF")

# =====================
# TABS
# =====================
tab1, tab2 = st.tabs(["🧾 Servicio", "📦 RF"])

# =====================
# TAB SERVICIO
# =====================
with tab1:
    st.subheader(servicio_sel["nombre"])

    col1, col2 = st.columns([2, 1])

    with col1:
        with st.expander("📄 Descripción del servicio", expanded=True):
            st.text(servicio_sel["descripcion"])

    with col2:
        st.metric("⏱ Tiempo base", formatear_tiempo(servicio_sel["tiempo_min"]))
        st.metric("📦 Cantidad", cantidad)
        st.metric("⌛ Total", formatear_tiempo(tiempo_total))

# =====================
# TAB RF
# =====================
with tab2:
    st.subheader("📦 Request For (RF)")

    if st.session_state.carrito:
        df = pd.DataFrame(st.session_state.carrito)

        df["Tiempo unitario"] = df["Tiempo unitario (min)"].apply(formatear_tiempo)
        df["Tiempo total"] = df["Tiempo total (min)"].apply(formatear_tiempo)

        st.dataframe(
            df[["Servicio", "Cantidad", "Tiempo unitario", "Tiempo total"]],
            use_container_width=True,
            hide_index=True
        )

        total_rf = df["Tiempo total (min)"].sum()
        st.divider()
        st.metric("⏱ Tiempo total RF", formatear_tiempo(total_rf))

        st.divider()
        st.markdown("### 🗑️ Eliminar servicio del RF")

        # Selector de eliminación
        idx_delete = st.selectbox(
            "Selecciona el servicio a eliminar",
            options=range(len(st.session_state.carrito)),
            format_func=lambda i: st.session_state.carrito[i]["Servicio"]
        )

        col_del_1, col_del_2 = st.columns([1, 3])

        with col_del_1:
            if st.button("🗑️ Eliminar"):
                st.session_state.carrito.pop(idx_delete)
                st.success("Servicio eliminado del RF")
                st.rerun()

    else:
        st.info("Aún no hay servicios en el RF")

