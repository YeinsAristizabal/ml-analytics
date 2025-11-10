import streamlit as st

# =============================
# Configuración general
# =============================
st.set_page_config(page_title="Sistema de Recomendación", layout="centered")

# =============================
# Título principal
# =============================
st.title("🛒 Sistema de Recomendación de Productos")

st.markdown("""
### 🎯 Descripción del Proyecto

Este proyecto implementa un **Sistema de Recomendación** basado en datos históricos de compra de clientes en una plataforma de comercio electrónico.

El objetivo es **personalizar la experiencia de compra**, mejorar la retención de usuarios y aumentar las conversiones, mostrando productos relevantes a cada cliente según su comportamiento de compra.

---

### Enfoques del modelo

El sistema combina diferentes técnicas de recomendación:

- **Filtrado Colaborativo (NMF)** → Detecta patrones comunes entre usuarios que compran productos similares.  
- **RFM Analysis (Recency, Frequency, Monetary)** → Identifica clientes más valiosos y recientes.  
- **Market Basket Analysis (MBA)** → Descubre combinaciones frecuentes de productos (“quien compra X también compra Y”). 
---

### 🧭 Navegación
- **📊 EDA:** Exploración de datos y patrones de compra.
- **📈 Results:** Resultados de las diferentes estrategias de recomendación.
- **🧪 Simulation:** Prueba manual del sistema de recomendación con un usuario.

---

Desarrollado como **MVP demostrativo** de recomendación inteligente.
- **Autor:** Yeins Yefferson Aristizabal López 
- **Data Scientist / AI Engineer**
""")
