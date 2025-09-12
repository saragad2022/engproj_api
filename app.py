from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import model_api

app = FastAPI(title="Question Difficulty API", version="1.0.0")

class QuestionRequest(BaseModel):
    question: str
    options: list[str]

@app.on_event("startup")
def startup():
    # Allow overriding paths with environment variables
    model_path = os.environ.get("MODEL_PATH", "models/model.pkl")
    vectorizer_path = os.environ.get("VECTORIZER_PATH", "models/vectorizer.pkl")
    try:
        model_api.load_model(model_path, vectorizer_path)
        print("Model and vectorizer loaded from:", model_path, vectorizer_path)
    except Exception as e:
        # Print error but allow server to start (so team can inspect logs)
        print("Error loading model/vectorizer at startup:", e)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(req: QuestionRequest):
    if model_api.MODEL is None or model_api.VECTORIZER is None:
        raise HTTPException(status_code=503, detail="Model or vectorizer not loaded. See logs.")
    try:
        difficulty = model_api.predict(model_api.MODEL, model_api.VECTORIZER, req.question, req.options)
        return {"difficulty_level": int(difficulty)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))