import streamlit as st
import requests
import pandas as pd

# ==========================================================
# Configuración inicial
# ==========================================================
st.set_page_config(page_title="Simulación de Recomendaciones", page_icon="🛍️", layout="centered")

st.title("🧠 Simulación del Sistema de Recomendación Filtrado Colaborativo (Users)")
st.markdown(
    """
    Este módulo permite **simular las recomendaciones personalizadas**
    de productos para un cliente determinado, usando el modelo de **Filtrado Colaborativo**.
    """
)

# ==========================================================
# URL del backend (ajusta si usas otro puerto o despliegue)
# ==========================================================
API_URL = "http://127.0.0.1:8080/recommend"

# ==========================================================
# Formulario de entrada
# ==========================================================
st.subheader("📋 Selecciona un usuario para generar recomendaciones")

with st.form("recommendation_form"):
    user_id = st.text_input("ID del Usuario (UUID_CLIENTE_CONSUMIDOR):", "")
    top_k = st.slider("Número de productos recomendados:", 1, 10, 5)
    submitted = st.form_submit_button("🔍 Obtener Recomendaciones")

# ==========================================================
# Envío de solicitud y visualización de resultados
# ==========================================================
if submitted:
    if not user_id:
        st.warning("Por favor, introduce un ID de usuario válido.")
    else:
        payload = {"user_id": user_id, "top_k": top_k}

        with st.spinner("Consultando modelo..."):
            try:
                response = requests.post(API_URL, json=payload)
            except requests.exceptions.ConnectionError:
                st.error("⚠️ No se pudo conectar con la API. Verifica que FastAPI esté ejecutándose.")
                st.stop()

        if response.status_code == 200:
            data = response.json()
            productos = pd.DataFrame(data["productos_recomendados"])
            st.success(f"✅ Recomendaciones generadas para el usuario `{user_id}`")
            st.dataframe(productos, use_container_width=True)
        else:
            st.error(f"Error: {response.status_code} — {response.text}")
