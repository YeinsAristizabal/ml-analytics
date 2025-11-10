import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import os

# ==========================
# pipeline
# ==========================
DATA = Path('data')
DOCS = Path('docs')
from pypdf import PdfReader
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # normaliza espacios y saltos de linea    
    text = re.sub(r'[^a-záéíóúüñ0-9.,:;?! ]', '', text) # elimina caracteres especiales, conserva letras, números y puntuación básica
    return text.strip()

def read_pdf(path):
    text = []
    r = PdfReader(str(path))
    for p in r.pages:
       page_text = p.extract_text() or ""
       text.append(clean_text(page_text))
    return "\n".join(text)
corpus = {p.name: read_pdf(p) for p in DOCS.glob('*.pdf')}

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# concatenar todo el texto de los PDFs
docs = " ".join(list(corpus.values()))
# generar la nube
wc = WordCloud(width=1500, height=1000, background_color="white",
               collocations=False).generate(docs)
fig, ax = plt.subplots(figsize=(12, 6))
ax.imshow(wc, interpolation="bilinear")
ax.axis("off")

# Lectura .json con principales tópicos
import json
# Suponiendo que el JSON está en un archivo llamado 'topicos.json'
with open('output/resultados_topicos.json', 'r') as f:
    datos_json = json.load(f)
# primeres tres palabras de cada tópico: Si el .json fuera enorme, haría un for
topico_0 = datos_json[0]['keywords'][:3]
topico_1 = datos_json[1]['keywords'][:3]
topico_2 = datos_json[2]['keywords'][:3]

# ==========================
# Header
# ==========================
st.set_page_config(page_title="dashboard", layout="centered")
st.title("chatbot de FAQs")
st.markdown("Esta aplicación permite explorar datos, visualizar KPIs y responder a preguntas frecuentes")
st.markdown("---")
# ==========================
# Sección de EDA (3 gráficos)
# ==========================
st.subheader("Exploración de Datos (EDA)")
col1, col2, col3 = st.columns(3)
with col2:
    st.pyplot(fig)
st.markdown("---")
# ==========================
# Sección de KPIs (3 KPIs)
# ==========================
st.subheader("KPIs")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric(label="Documentos procesados", value=len(list(DOCS.glob('*.pdf'))))
kpi2.metric(label="Acuraccy modelo", value="67 %")
kpi3.metric(label="F1 Score modelo", value="80 %")
st.markdown("---")
# ==========================
# Sección de Tópicos (3 KPIs)
# ==========================
st.subheader("Principales palabras o contenido de cada tópico")
top1, top2, top3 = st.columns(3)
with top1:
    st.write("Tópico 1:", topico_0)
with top2:
    st.write("Tópico 2:", topico_1)
with top3:
    st.write("Tópico 3:", topico_2)
st.markdown("---")

# ==========================
# Sección de Tabla
# ==========================
st.subheader("Tabla de datos: Probabilidad de un documento pertenecer a un tópico")
# Ejemplo de tabla
# cargar .json como dataframe
data = pd.read_csv("output/resultados_topicos_por_documento.csv")
data = data.rename(columns={'Unnamed: 0': 'Documento'})
st.dataframe(data)
st.markdown("---")
# ==========================
# Sección Chatbot (text-area)
# ==========================
import requests
# URL del endpoint
url = os.getenv("FASTAPI_URL", "http://127.0.0.1:8000")
# url = "http://127.0.0.1:8000/chat"
st.subheader("Chatbot Básico")
# Pregunta a enviar
user_input = st.text_area("Escribe tu mensaje aquí:")
payload = {"question": user_input}
# Hacer POST
response = requests.post(url, json=payload)

if st.button("Enviar"):
    if user_input.strip() != "":
        # Respuesta 
        st.text(response.json()["answer"])
    else:
        st.warning("Por favor ingresa un mensaje.")
st.markdown("---")

# ==========================
# Footer
# ==========================
st.markdown("---")
st.markdown("© 2025 by Yeins Aristizabal")
st.markdown("**Disclaimer:** Esta app es solo para fines demostrativos")
st.markdown("---")