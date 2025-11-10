import streamlit as st

st.set_page_config(page_title="Detector de Fraccionamiento", layout="centered")

st.title("💳 Sistema de Detección de Fraccionamiento Transaccional")
st.markdown("""
### 🧩 Descripción del Proyecto

Detectar patrones anómalos en transacciones financieras.  
Utiliza un modelo **Isolation Forest** entrenado con datos históricos para identificar comportamientos que podrían sugerir **fraccionamiento transaccional** o intentos de evasión de controles financieros.

---

### 🎯 Objetivo
Detectar, visualizar y simular posibles **anomalías** en el comportamiento transaccional diario de usuarios o cuentas.

---

### ⚙️ Premisas del modelo
- Los datos de entrada se basan en **agregaciones diarias** por usuario:
  - `count_day`: número de transacciones.
  - `sum_day`: suma total de montos.
  - `mean_day`: valor promedio.
  - `std_day`: desviación estándar.
  - `max_day`: transacción máxima.
- El modelo fue entrenado sin etiquetas (`unsupervised`) usando **Isolation Forest**.
- Las predicciones devuelven:
  - `1`: comportamiento normal.
  - `-1`: comportamiento anómalo o sospechoso.

---

### 🧭 Navegación
- **📊 EDA Básico:** Exploración visual de las variables.
- **📈 Resultados del Modelo:** Métricas y análisis de predicciones.
- **🧪 Simulación:** Prueba manual de escenarios y predicción.

---
Desarrollado como **MVP demostrativo** en detección de anomalías.
""")
