import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =============================
# CONFIGURACIÓN DE PÁGINA
# =============================
st.set_page_config(page_title="Resultados - Segmentación y Recomendación", layout="centered")

st.title("📈 Resultados del Análisis de Clientes y Recomendaciones")

st.markdown("""
En esta sección se presentan los resultados del análisis de segmentación **RFM**
y las reglas de afinidad obtenidas con el modelo de **Market Basket Analysis (MBA)**.

Los resultados permiten identificar clientes valiosos, sus patrones de compra y las
relaciones entre productos que pueden ser usadas para personalizar recomendaciones.
---
""")

# =============================
# CARGA DE DATOS
# =============================
@st.cache_data
def load_data():
    table_01 = pd.read_csv("./data/raw/dataset_sample_1.csv")
    mba = pd.read_csv("./data/processed/mba.csv")
    mba['antecedents'] = mba['antecedents'].str.replace("frozenset\\(|\\)|\\{|\\}|'", "", regex=True)
    mba['consequents'] = mba['consequents'].str.replace("frozenset\\(|\\)|\\{|\\}|'", "", regex=True)
    return table_01, mba

table_01, mba = load_data()

# =============================
# RFM SEGMENTATION
# =============================

st.subheader("🎯 Análisis RFM (Recency, Frequency, Monetary)")

snapshot_date = pd.to_datetime(table_01["FECHA_SOLUCION"]).max() + pd.Timedelta(days=1)

rfm = table_01.groupby('UUID_CLIENTE_CONSUMIDOR').agg({
    'FECHA_SOLUCION': lambda x: (snapshot_date - pd.to_datetime(x).max()).days,
    'PEDIDO': 'nunique',
    'VENTA_BRUTA_CON_IVA': 'sum'
}).reset_index().rename(columns={
    'FECHA_SOLUCION': 'recency_days',
    'PEDIDO': 'frequency',
    'VENTA_BRUTA_CON_IVA': 'monetary'
})

# Scoring
rfm['r_score'] = pd.qcut(rfm['recency_days'], 5, labels=[5,4,3,2,1]).astype(int)
rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5]).astype(int)
rfm['m_score'] = pd.qcut(rfm['monetary'], 5, labels=[1,2,3,4,5]).astype(int)

rfm['RFM_score'] = rfm['r_score'].astype(str) + rfm['f_score'].astype(str) + rfm['m_score'].astype(str)

# Segmentos
def segment(row):
    if row['RFM_score'].startswith('5'):
        return 'Cliente Oro'
    if row['r_score'] >= 4 and row['f_score'] >= 4:
        return 'Cliente Plata'
    if row['r_score'] <= 2 and row['f_score'] >= 4:
        return 'Cliente Bronce'
    return 'Otros'

rfm['segment'] = rfm.apply(segment, axis=1)

# =============================
# VISUALIZACIONES RFM
# =============================
st.markdown("**Distribución de Clientes por Segmento**")
seg_counts = rfm['segment'].value_counts()
fig1, ax1 = plt.subplots(figsize=(5, 5))
ax1.pie(seg_counts.values, labels=seg_counts.index, autopct="%1.1f%%", startangle=90)
ax1.set_title("Distribución de Segmentos RFM")
st.pyplot(fig1)

st.markdown("**Promedio de Métricas RFM por Segmento**")
avg_rfm = rfm.groupby("segment")[["recency_days", "frequency", "monetary"]].mean()
st.dataframe(avg_rfm.style.format({
    "recency_days": "{:.0f}",
    "frequency": "{:.1f}",
    "monetary": "${:,.0f}"
}))

# =============================
# MARKET BASKET ANALYSIS (MBA)
# =============================
st.subheader("🛒 Reglas de Afinidad - Market Basket Analysis")

st.markdown("""
Estas reglas representan combinaciones de productos que suelen comprarse juntas,
basadas en el análisis de **co-ocurrencias** de ítems en pedidos.
""")

st.markdown("**📋 Top 10 Reglas con Mayor Confianza**")
top_conf = mba.sort_values("confidence", ascending=False).head(10)
st.dataframe(top_conf)


# =============================
# FINAL
# =============================
st.markdown("---")
st.markdown("""
**Interpretación:**
- **Clientes Oro:** frecuentes, recientes y con alto gasto.
- **Clientes Plata:** consistentes, pero con menor gasto o antigüedad.
- **Clientes Bronce:** compran con frecuencia, pero no de forma reciente.

**MBA:** puede servir como insumo para recomendaciones y estrategias de *cross-selling*.
""")