# src/api/simple_app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
import numpy as np

MODEL_PATH = os.getenv("MODEL_PATH", "models/isolation_forest.joblib")
SCALER_PATH = os.getenv("SCALER_PATH", "models/scaler.joblib")

app = FastAPI(title="Fraccionamiento Scoring")

# Cargar modelo al iniciar la app
if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"Model file not found: {MODEL_PATH}")
model = joblib.load(MODEL_PATH)

scaler = None
if os.path.exists(SCALER_PATH):
    scaler = joblib.load(SCALER_PATH)


class SingleFeatures(BaseModel):
    count_day: float
    sum_day: float
    mean_day: float
    std_day: float
    max_day: float


@app.post("/predict")
def predict(payload: SingleFeatures):
    try:
        # construir numpy array (1, n_features)
        X = np.array([[payload.count_day,
                       payload.sum_day,
                       payload.mean_day,
                       payload.std_day,
                       payload.max_day]], dtype=float)
        # aplicar scaler si existe
        if scaler is not None:
            X = scaler.transform(X)

        # predecir
        label = int(model.predict(X)[0])                 # -1 anomaly, 1 normal
        score = float(model.decision_function(X)[0])     # mayor = más normal; menor = más anómalo

        return {"label": label, "score": score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
