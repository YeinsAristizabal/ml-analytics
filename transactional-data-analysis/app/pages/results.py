# app/pages/2_Resultados_Modelo.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="Resultados Modelo", layout="centered")
st.title("📈 Resultados — Actividad sospechosa")

df = pd.read_csv(r"data//processed//isolation_forest_results.csv", nrows=10000)

st.dataframe(df.head(5))
# --- KPIs simples ---
total = len(df)
n_suspects = int((df["if_label"] == -1).sum()) if "if_label" in df.columns else 0
pct = 100 * n_suspects / max(1, total)

c1, c2, c3 = st.columns(3)
c1.metric("Registros cargados", f"{total:,}")
c2.metric("Sospechosos", f"{n_suspects:,}")
c3.metric("Score mínimo", f"{df['if_score'].min():.4f}" if "if_score" in df.columns else "N/A")

st.markdown("---")

# --- Top N sospechosos (por if_score ascendente) ---
top_n = st.number_input("Top N sospechosos a mostrar", min_value=3, max_value=200, value=6, step=1)
if "if_label" in df.columns and "if_score" in df.columns:
    ml_suspects = df[df["if_label"] == -1].sort_values("if_score", ascending=True)
    if ml_suspects.empty:
        st.info("No hay registros con if_label == -1 en el CSV.")
    else:
        display_cols = ["user_id", "date", "if_score"]
        for c in ["count_day", "sum_day", "mean_day", "std_day", "max_day"]:
            if c in ml_suspects.columns:
                display_cols.append(c)
        st.subheader(f"Top {top_n} sospechosos (label=-1, menor if_score = más anómalo)")
        st.dataframe(ml_suspects[display_cols].head(top_n).reset_index(drop=True))
        # permitir descargar top
        top_bytes = ml_suspects[display_cols].head(top_n).to_parquet(index=False)
        st.download_button("Descargar Top (parquet)", data=top_bytes, file_name="top_ml_suspects.parquet")
else:
    st.info("El CSV no contiene columnas 'if_label' y/o 'if_score' necesarias para listar sospechosos.")

st.markdown("---")

# --- Histograma simple de scores ---
if "if_score" in df.columns:
    st.subheader("Distribución de if_score")
    fig, ax = plt.subplots(figsize=(9,3))
    ax.hist(df["if_score"], bins=50)
    ax.set_xlabel("if_score (mayor → más normal, menor → más anómalo)")
    ax.set_ylabel("Frecuencia")
    st.pyplot(fig)

st.markdown("---")
# --- Scatter count vs sum coloreado por label (si existen) ---
if {"count_day", "sum_day", "if_label"}.issubset(set(df.columns)):
    st.subheader("Scatter: transacciones (count_day) vs suma (sum_day)")
    sample = df.sample(n=min(5000, len(df)), random_state=42)
    colors = sample["if_label"].map({1: "blue", -1: "red"})
    fig2, ax2 = plt.subplots(figsize=(9,4))
    ax2.scatter(sample["count_day"], sample["sum_day"], c=colors, alpha=0.6, s=12)
    ax2.set_xlabel("count_day")
    ax2.set_ylabel("sum_day")
    st.pyplot(fig2)
    st.write("Azul = 1: Actividad Normal")
    st.write("Rojo = -1: Actividad Sospechosa")
    st.success("Visualización completada.")
else: 
    st.info("Introduce la ruta del CSV y presiona 'Cargar CSV'.")
