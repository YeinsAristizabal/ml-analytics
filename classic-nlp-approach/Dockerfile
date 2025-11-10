FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY app.py .
COPY data ./data
COPY docs ./docs
COPY output ./output

# Exponer puerto Streamlit
EXPOSE 8501

# Variable de entorno: backend URL (se sobreescribe en Cloud Run)
ENV FASTAPI_URL="http://127.0.0.1:8000"

# Comando de inicio
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
