import streamlit as st
import requests

st.title("🧪 Simulación de Detección")

API_URL = "http://127.0.0.1:8000/predict"

st.write("Introduce valores manualmente para simular el comportamiento de un usuario:")

with st.form("input_form"):
    count_day = st.number_input("Número de transacciones", min_value=0, value=10)
    sum_day = st.number_input("Suma total", min_value=0.0, value=5000.0)
    mean_day = st.number_input("Promedio", min_value=0.0, value=500.0)
    std_day = st.number_input("Desviación estándar", min_value=0.0, value=100.0)
    max_day = st.number_input("Máximo", min_value=0.0, value=1000.0)
    submitted = st.form_submit_button("Analizar")

if submitted:
    data = {
        "count_day": count_day,
        "sum_day": sum_day,
        "mean_day": mean_day,
        "std_day": std_day,
        "max_day": max_day
    }

    with st.spinner("Consultando modelo..."):
        response = requests.post(API_URL, json=data)

    if response.status_code == 200:
        result = response.json()
        label = result["label"]
        score = result["score"]

        st.success(f"Label: {label} — Score: {score:.6f}")
        if label == -1:
            st.error("⚠️ Actividad potencialmente FRAUDULENTA o sospechosa.")
        else:
            st.info("✅ Actividad normal.")
    else:
        st.error(f"Error: {response.text}")