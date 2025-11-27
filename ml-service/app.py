# ml-service/app.py
import os
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, RootModel
from dotenv import load_dotenv

from utils import load_pickle, ensure_df, preprocess_and_predict

load_dotenv()

# Paths to artifacts
MODEL_PATH = os.getenv("MODEL_PATH", "model_artifacts/best_model.pkl")
PREPROCESSOR_PATH = os.getenv("PREPROCESSOR_PATH", "model_artifacts/preprocessor.pkl")

app = FastAPI(title="ML Service - Antigravity Credit Risk", version="2.0")

# Global variables to store artifacts
model = None
scaler = None
model_columns = None

# Load artifacts on startup
try:
    print(f"Loading model from {MODEL_PATH}...")
    model = load_pickle(MODEL_PATH)
    
    print(f"Loading preprocessor from {PREPROCESSOR_PATH}...")
    # preprocessor.pkl contains (scaler, model_columns)
    scaler, model_columns = load_pickle(PREPROCESSOR_PATH)
    
    print("Artifacts loaded successfully.")
except Exception as e:
    print(f"Error loading artifacts: {e}")
    model = None
    scaler = None
    model_columns = None

# Pydantic model for a single prediction input
class SingleInput(RootModel):
    # allow arbitrary fields
    root: Dict[str, Any]

class BatchInput(BaseModel):
    data: List[Dict[str, Any]] = Field(..., description="List of records")

@app.get("/health")
def health():
    return {
        "status": "ok", 
        "model_loaded": model is not None and scaler is not None
    }

@app.post("/predict")
def predict(payload: BatchInput):
    if model is None or scaler is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    try:
        df = ensure_df(payload.data)
        result = preprocess_and_predict(model, scaler, model_columns, df)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/predict_single")
def predict_single(payload: SingleInput):
    if model is None or scaler is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    try:
        data = payload.root
        df = ensure_df([data])
        result = preprocess_and_predict(model, scaler, model_columns, df)
        
        # Extract single result
        pred = result["predictions"][0]
        prob = result["probabilities"][0] if result["probabilities"] else None
        
        return {"prediction": pred, "probability": prob}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
