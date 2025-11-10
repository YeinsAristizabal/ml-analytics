# Aplicación de IA en Documentos y FAQs (MVP)

## Estructura
- `docs/` → 5 PDFs (política, procedimiento, reporte, términos, FAQs).
- `data/` → `faqs_train.csv` y `faqs_test.csv`.
- `app_fastapi/` → `main.py` y `requirements.txt` (API mínima).
- `notebook.ipynb` → notebook de trabajo.

## Instalación rápida
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r app_fastapi/requirements.txt
uvicorn app_fastapi.main:app --reload   # API en http://127.0.0.1:8000
streamlit run app.py
```

## Tareas (resumen)
1. Procesar PDFs y extraer tópicos → exportar CSV/JSON.
2. Construir chatbot (clasificador o RAG) y evaluar con `faqs_test.csv`.
3. Generar dashboard con KPIs.
4. Documento breve con decisiones, métricas y uso de IA (prompts + validación).
