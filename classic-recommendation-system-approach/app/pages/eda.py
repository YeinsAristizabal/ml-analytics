import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =============================
# CONFIGURACIÓN DE PÁGINA
# =============================
st.set_page_config(page_title="EDA - Sistema de Recomendación", layout="centered")

st.title("📊 Análisis Exploratorio de Datos (EDA)")

st.markdown("""
Exploración inicial de los datos transaccionales para identificar patrones de consumo,
categorías principales, comportamiento por ciudad y evolución temporal de las ventas.
---
""")

# =============================
# CARGA DE DATOS
# =============================
@st.cache_data
def load_data():
    table_01 = pd.read_csv(".//data//raw//dataset_sample_1.csv")
    table_02 = pd.read_csv(".//data//raw//dataset_sample_2.csv")
    return table_01, table_02

table_01, table_02 = load_data()

# =============================
# LIMPIEZA BÁSICA
# =============================
if "FECHA_SOLUCION" in table_01.columns:
    table_01["FECHA_SOLUCION"] = pd.to_datetime(table_01["FECHA_SOLUCION"], errors="coerce")

# =============================
# SECCIÓN 1: CATEGORÍAS
# =============================
st.subheader("🔹 Distribución de Categorías")


top_cats = table_01["CATEGORIA"].value_counts().head(10)
fig1, ax1 = plt.subplots(figsize=(5, 5))
ax1.pie(top_cats.values, labels=top_cats.index, autopct="%1.1f%%", startangle=90)
ax1.set_title("Principales Categorías por Transacción")
st.pyplot(fig1)


top_units = table_01.groupby("CATEGORIA")["UNIDADES_BRUTAS"].sum().sort_values(ascending=False).head(10)
fig2, ax2 = plt.subplots(figsize=(5, 5))
ax2.pie(top_units.values, labels=top_units.index, autopct="%1.1f%%", startangle=90)
ax2.set_title("Distribución de Unidades Vendidas por Categoría")
st.pyplot(fig2)

# =============================
# SECCIÓN 2: TABLAS RESUMEN
# =============================
st.subheader("🔹 Tablas Resumen")

col3, col4 = st.columns(2)
with col3:
    st.markdown("**Top 10 Categorías por Frecuencia**")
    st.dataframe(top_cats.reset_index().rename(columns={"index": "CATEGORIA", "CATEGORIAS": "FRECUENCIA"}))

with col4:
    st.markdown("**Top 10 Categorías por Unidades Vendidas**")
    st.dataframe(top_units.reset_index().rename(columns={"index": "CATEGORIA", "UNIDADES_BRUTAS": "TOTAL"}))

col5, col6 = st.columns(2)
with col5:
    st.markdown("**Top 10 Ciudades con Más Transacciones**")
    top_cities = table_02["CIUDAD"].value_counts().head(10)
    st.dataframe(top_cities.reset_index().rename(columns={"index": "CIUDAD", "CIUDAD": "TRANSACCIONES"}))

with col6:
    st.markdown("**Venta Promedio por Categoría (Top 10)**")
    venta_promedio = table_01.groupby("CATEGORIA")["VENTA_BRUTA_CON_IVA"].mean().sort_values(ascending=False).head(10)
    st.dataframe(venta_promedio.reset_index().rename(columns={"VENTA_BRUTA_CON_IVA": "VENTA_PROMEDIO"}))

# =============================
# SECCIÓN 3: ANÁLISIS TEMPORAL
# =============================
st.subheader("🔹 Evolución Temporal de las Ventas")

if "FECHA_SOLUCION" in table_01.columns:
    df_time = table_01.dropna(subset=["FECHA_SOLUCION"])
    df_indexed = df_time.set_index("FECHA_SOLUCION")
    df_monthly = df_indexed["VENTA_BRUTA_CON_IVA"].resample("ME").sum()
    df_monthly.index = df_monthly.index.strftime("%Y-%m")

    fig3, ax3 = plt.subplots(figsize=(12, 6))
    ax3.plot(df_monthly.index, df_monthly.values, marker="o", linestyle="-")
    ax3.set_title("Venta Bruta Total con IVA por Mes")
    ax3.set_xlabel("Mes")
    ax3.set_ylabel("Venta Total con IVA")
    ax3.grid(True, linestyle="--", alpha=0.6)
    plt.xticks(rotation=45)
    st.pyplot(fig3)
else:
    st.warning("No se encontró la columna 'FECHA_SOLUCION' para generar el gráfico temporal.")

# =============================
# FINAL
# =============================
st.markdown("---")
st.markdown("**Nota:** Este análisis es exploratorio y busca identificar patrones de comportamiento general antes del modelado de recomendación.")
