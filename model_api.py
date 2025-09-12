import os
import joblib
import re
import string
from fastapi import FastAPI
from pydantic import BaseModel

MODEL = None
VECTORIZER = None

# -----------------------
# تحميل الموديل
# -----------------------
def load_model(model_path: str, vectorizer_path: str):
    global MODEL, VECTORIZER
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    if not os.path.exists(vectorizer_path):
        raise FileNotFoundError(f"Vectorizer file not found: {vectorizer_path}")
    MODEL = joblib.load(model_path)
    VECTORIZER = joblib.load(vectorizer_path)
    return MODEL, VECTORIZER

# -----------------------
# تنظيف النصوص
# -----------------------
def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ''
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess(question: str, options: list):
    opts = [str(o) for o in options]
    combined = question + ' ' + ' '.join(opts)
    return clean_text(combined)

# -----------------------
# التنبؤ
# -----------------------
def predict(model, vectorizer, question: str, options: list):
    if model is None or vectorizer is None:
        raise RuntimeError("Model or vectorizer not loaded. Call load_model() first.")
    text = preprocess(question, options)
    X = vectorizer.transform([text])
    y_pred = model.predict(X)
    return int(y_pred[0])

# -----------------------
# API
# -----------------------
app = FastAPI(title="Difficulty Prediction API")

class QuestionInput(BaseModel):
    question: str
    options: list

@app.on_event("startup")
def startup_event():
    global MODEL, VECTORIZER
    MODEL, VECTORIZER = load_model("models/model.pkl", "models/vectorizer.pkl")

@app.post("/predict")
def get_prediction(data: QuestionInput):
    level = predict(MODEL, VECTORIZER, data.question, data.options)
    return {"difficulty_level": level}
