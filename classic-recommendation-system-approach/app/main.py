from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

# ==========================================================
# Cargar modelo y datos
# ==========================================================
data = joblib.load("models/recommender_full.pkl")
pred_df = data["pred_df"]

# Cargar tabla de referencia (para traer categoría o nombre)
table_01 = pd.read_csv("data/raw/dataset_sample_1.csv")  # <-- ajusta la ruta según tu estructura

# ==========================================================
# Inicializar API
# ==========================================================
app = FastAPI(title="Recommender API", version="1.0")

# ==========================================================
# Modelo de entrada
# ==========================================================
class UserRequest(BaseModel):
    user_id: str
    top_k: int = 5

# ==========================================================
# Endpoint de recomendación
# ==========================================================
@app.post("/recommend")
def recommend(request: UserRequest):
    user_id = request.user_id
    top_k = request.top_k

    if user_id not in pred_df.index:
        return {"error": f"Usuario {user_id} no encontrado en el modelo."}

    # Obtener las predicciones del usuario
    user_scores = pred_df.loc[user_id].sort_values(ascending=False).head(top_k)

    # Filtrar la tabla original con esos códigos
    productos_info = (
        table_01[table_01["COD_PRODUCTO"].isin(user_scores.index)]
        [["COD_PRODUCTO", "CATEGORIA"]]
        .drop_duplicates(subset=["COD_PRODUCTO"])
    )

    # Combinar con los puntajes del modelo
    productos_info = productos_info.merge(
        user_scores.rename("score"),
        left_on="COD_PRODUCTO",
        right_index=True,
        how="left"
    ).sort_values("score", ascending=False)

    # Convertir a formato JSON
    productos_recomendados = productos_info.to_dict(orient="records")

    return {
        "user_id": user_id,
        "top_k": top_k,
        "productos_recomendados": productos_recomendados
    }
