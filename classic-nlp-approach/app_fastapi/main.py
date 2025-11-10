from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI(title="Chatbot MVP", version="0.1.0")

class Query(BaseModel):
    question: str

# FAQS = {
#     "certificado": "Ingresa al Portal > Mi Perfil > Certificados y presiona Descargar.",
#     "tramite": "Ingresa al Portal > Mis trámites > Estado para ver el detalle.",
#     "contraseña": "Usa la opción '¿Olvidaste la contraseña?' en la pantalla de ingreso.",
#     "whatsapp": "Sí, WhatsApp está habilitado y concentra el 42% de las atenciones.",
#     "soporte": "Puedes escribir a soporte@empresa.com para asistencia."
# }

# Cargar modelo y vectorizador entrenado
clf = joblib.load("modelos/faq_model.pkl") 
vectorizer = joblib.load("modelos/vectorizer.pkl")

@app.get("/health")
def health():
    return {"status": "ok"}

# @app.post("/chat")
# def chat(q: Query):
#     ql = q.question.lower()
#     for k, v in FAQS.items():
#         if k in ql:
#             return {"answer": v, "matched": k}
#     return {"answer": "No tengo esa respuesta aún. ¿Puedes reformular?", "matched": None}

@app.post("/chat")
def chat(q: Query):
    # Transformar la pregunta con el vectorizador
    X_q = vectorizer.transform([q.question])
    # Predecir la respuesta
    pred = clf.predict(X_q)[0]
    return {"answer": pred}
