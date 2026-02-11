import streamlit as st
import pandas as pd
from servicios import SERVICIOS

# =====================
# CONFIG
# =====================
st.set_page_config(
    page_title="Calculadora LPU",
    layout="wide"
)

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

if "modo_factura" not in st.session_state:
    st.session_state.modo_factura = False

if "rf" not in st.session_state:
    st.session_state.rf = ""

if "titulo" not in st.session_state:
    st.session_state.titulo = ""

# =====================
# MODO FACTURA (PANTALLA LIMPIA)
# =====================
if st.session_state.modo_factura:

    df = pd.DataFrame(st.session_state.carrito)
    total_min = df["Tiempo total (min)"].sum()

    df["Tiempo unitario"] = df["Tiempo unitario (min)"].apply(formatear_tiempo)
    df["Tiempo total"] = df["Tiempo total (min)"].apply(formatear_tiempo)

    with st.container(border=True):
        st.markdown(f"### {st.session_state.titulo or 'Sin título'}")
        st.markdown(f"### {st.session_state.rf or '—'}")

        st.divider()

        st.dataframe(
            df[["Servicio", "Cantidad", "Tiempo unitario", "Tiempo total"]],
            hide_index=True,
            use_container_width=True
        )

        st.divider()
        st.metric("⏱ Total", formatear_tiempo(total_min))

    if st.button("⬅ Volver", use_container_width=True):
        st.session_state.modo_factura = False
        st.rerun()

    st.stop()

# =====================
# VISTA NORMAL
# =====================
st.title("🧮 Calculadora LPU")

labels = {
    i: f"{s['id']} — {s['nombre']}"
    for i, s in enumerate(SERVICIOS)
}

col_left, col_right = st.columns([3, 2])

# =====================
# COLUMNA IZQUIERDA (ESTÁTICA)
# =====================
with col_left:
    st.subheader("🔍 Selección de servicio")

    idx = st.selectbox(
        "Buscar servicio",
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

    with st.container(border=True):
        st.markdown(f"### {servicio['nombre']}")

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
            st.success("Servicio agregado")

    with st.expander("📄 Descripción del servicio"):
        st.write(servicio["descripcion"])

# =====================
# COLUMNA DERECHA (RF ACTUAL)
# =====================
with col_right:
    st.subheader("📦 RF Actual")

    if st.session_state.carrito:
        df = pd.DataFrame(st.session_state.carrito)
        df["Tiempo total"] = df["Tiempo total (min)"].apply(formatear_tiempo)

        st.dataframe(
    df[["Servicio", "Cantidad", "Tiempo total"]],
    hide_index=True,
    use_container_width=True
)


        total = sum(item["Tiempo total (min)"] for item in st.session_state.carrito)
        st.metric("⏱ Total RF", formatear_tiempo(total))

        st.divider()
        

        # RF + TITULO SOLO CUANDO HAY SERVICIOS
        st.session_state.rf = st.text_input("RF", st.session_state.rf)
        st.session_state.titulo = st.text_input("Título", st.session_state.titulo)
        

        if st.button("📸 Tomar captura", use_container_width=True):
            st.session_state.modo_factura = True
            st.rerun()

             # ---- ELIMINAR SERVICIO ----
        idx_delete = st.selectbox(
            "Eliminar servicio",
            options=range(len(st.session_state.carrito)),
            format_func=lambda i: st.session_state.carrito[i]["Servicio"]
        )

        if st.button("🗑️ Eliminar seleccionado", use_container_width=True):
            st.session_state.carrito.pop(idx_delete)
            st.rerun()

        st.divider()

    else:
        st.info("Sin servicios agregados")

        
