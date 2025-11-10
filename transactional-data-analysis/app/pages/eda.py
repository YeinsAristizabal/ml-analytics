# app/pages/1_EDA_Básico.py
import streamlit as st
import polars as pl
import matplotlib.pyplot as plt

st.set_page_config(page_title="eda_basico", layout="centered")
st.title("📊 Exploración Rápida de Transacciones")

# === CONFIGURACIÓN ===

st.markdown(
    f"""
EDA rápido con:
- KPIs globales
- Porcentaje crédito / débito
- Top comercios por monto total
- Top usuarios por número de transacciones
- Evolución mensual de montos
"""
)
st.write("---")
# === CARGA DE DATOS ===

df_polars = pl.read_parquet(r"data//raw//sample_data_0006_part_00.parquet", n_rows=10000)

# === KPIs ===
total_tx = df_polars.height
total_amount = df_polars["transaction_amount"].sum()
avg_amount = df_polars["transaction_amount"].mean()

c1, c2, c3 = st.columns(3)
c1.metric("Transacciones", f"{total_tx:,}")
c2.metric("Monto total ($)", f"{total_amount:,.2f}")
c3.metric("Monto promedio ($)", f"{avg_amount:,.2f}")

st.divider()

# === PIE CHART: Crédito / Débito ===
if "transaction_type" in df_polars.columns:
    type_counts = (
        df_polars["transaction_type"]
        .to_pandas()
        .str.lower()
        .value_counts()
        .to_dict()
    )
    fig1, ax1 = plt.subplots()
    ax1.pie(
        type_counts.values(),
        labels=type_counts.keys(),
        autopct="%1.1f%%",
        startangle=90,
    )
    ax1.set_title("Distribución Crédito / Débito")
    st.pyplot(fig1)
else:
    st.info("No se encontró la columna 'transaction_type'.")

st.divider()
# === TOP 5 COMERCIOS POR MONTO ===
if "merchant_id" in df_polars.columns:
    top_merchants = (
        df_polars.group_by("merchant_id")
        .agg(pl.sum("transaction_amount").alias("total_amount"))
        .sort("total_amount", descending=True)
        .head(15)
    )
    st.subheader("🏪 Top 5 Comercios por Monto Total")
    st.write("Obs: Para esta muestra, solo se tiene un comercio")
    st.dataframe(top_merchants)
else:
    st.info("No se encontró la columna 'merchant_id'.")

st.write("---")
# === TOP 5 USUARIOS POR TRANSACCIONES ===
if "user_id" in df_polars.columns:
    top_users = (
        df_polars.group_by("user_id")
        .agg(pl.count().alias("tx_count"))
        .sort("tx_count", descending=True)
        .head(5)
    )
    st.subheader("👥 Top 5 Usuarios por Número de Transacciones")
    st.dataframe(top_users)
else:
    st.info("No se encontró la columna 'user_id'.")

st.divider()

# === EVOLUCIÓN MENSUAL ===
if "transaction_date" in df_polars.columns:
    df_monthly = (
        df_polars.with_columns([
            pl.col("transaction_date").dt.year().alias("year"),
            pl.col("transaction_date").dt.month().alias("month")
        ])
        .group_by(["year", "month"])
        .agg(pl.sum("transaction_amount").alias("total_monthly_amount"))
        .sort(["year", "month"])
        .with_columns(
            (pl.col("year").cast(pl.Utf8) + "-" +
             pl.col("month").cast(pl.Utf8).str.pad_start(2, "0")).alias("year_month")
        )
    )

    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(
        df_monthly["year_month"],
        df_monthly["total_monthly_amount"],
        marker="o", linestyle="-", color="skyblue"
    )
    ax2.set_title("Evolución Mensual del Monto Total")
    ax2.set_xlabel("Mes (YYYY-MM)")
    ax2.set_ylabel("Monto Total")
    plt.xticks(rotation=45, ha="right")
    plt.grid(alpha=0.4, linestyle="--")
    st.pyplot(fig2)
else:
    st.info("No se encontró la columna 'transaction_date' para análisis temporal.")

st.divider()
