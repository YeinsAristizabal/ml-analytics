# Imagen base
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /code

# Instalar dependencias
COPY app_fastapi/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY app_fastapi/ .

# Exponer puerto
EXPOSE 8000

# Comando para correr FastAPI con uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]