from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.sklearn
import os

from src.data.preprocess import clean_text

app = FastAPI(title="API Inteligente de Enrutamiento de Tickets", version="1.0.0")

# --- Esquemas de Datos (Input/Output) ---
class TicketRequest(BaseModel):
    ticket: str

class TicketResponse(BaseModel):
    departamento: str
    confianza: float

# --- Variables Globales y Carga de Modelo ---
MODEL_PATH = os.getenv("MODEL_PATH", "model") # En AKS esto apuntaría al modelo montado
model = None

@app.on_event("startup")
def load_model():
    global model
    try:
        # En Azure ML / AKS, el modelo puede venir pre-descargado en el contenedor
        # o cargado directamente del registro de modelos vía la URI de MLflow.
        # model = mlflow.sklearn.load_model("models:/TicketClassifierModel/Production")
        model = mlflow.sklearn.load_model(MODEL_PATH)
        print("Modelo cargado exitosamente en memoria.")
    except Exception as e:
        print(f"Error crítico al cargar el modelo: {e}")

@app.post("/predict", response_model=TicketResponse)
def predict_ticket(request: TicketRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="El modelo no está disponible.")
    
    # 1. Preprocesar el input (Crucial en producción)
    cleaned_text = clean_text(request.ticket)
    
    # 2. Inferencia
    prediction = model.predict([cleaned_text])[0]
    
    # 3. Calcular Nivel de Confianza (Probabilidad)
    probabilities = model.predict_proba([cleaned_text])[0]
    confidence = max(probabilities)

    return TicketResponse(
        departamento=str(prediction),
        confianza=float(confidence)
    )

@app.get("/health")
def health_check():
    return {"status": "Servicio de Inferencia Activo", "model_loaded": model is not None}
