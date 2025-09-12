# Question Difficulty API - Quick Start (no Docker)

This repository contains a small FastAPI service that predicts the difficulty level (1-11)
of a multiple-choice question (MCQ). The model is a scikit-learn model and the text
vectorizer (e.g., TfidfVectorizer) is saved with joblib.

## Files included
- `app.py` - FastAPI application.
- `model_api.py` - model loading, preprocessing and predict wrapper.
- `requirements.txt` - Python dependencies.
- `test_client.py` - simple script to call the `/predict` endpoint.
- `models/` - place `model.pkl` and `vectorizer.pkl` here (NOT included).
- `example_request.json` - example payload.

## Step A — (On Google Colab) save and download model files
In your Colab notebook `engproj.ipynb`, run these (if you already saved, skip):
```python
import joblib
# assuming your model variable is named `model` and vectorizer named `vectorizer`
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

# then to download (Colab)
from google.colab import files
files.download("model.pkl")
files.download("vectorizer.pkl")
```
Download those files and put them into the `models/` folder of this project.

## Step B — (Local) prepare the environment
```bash
python -m venv venv
# activate the venv
# Linux / macOS:
source venv/bin/activate
# Windows (PowerShell):
venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

## Step C — Put your model files
Copy the downloaded `model.pkl` and `vectorizer.pkl` into the `models/` folder.

## Step D — Run the API
```bash
uvicorn app:app --reload --port 8000
```
Open `http://127.0.0.1:8000/docs` to test the API using the Swagger UI.

## Example curl
```bash
curl -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" \
  -d '{"question":"What is the capital of France?","options":["Paris","London","Berlin","Rome"]}'
```

## Troubleshooting
- **NameError: vectorizer is not defined**: ensure `vectorizer.pkl` was saved from Colab and placed into `models/`.
- **FileNotFoundError**: check the `models/` path and filenames.
- **Version mismatch**: If scikit-learn versions differ (train vs. runtime) you may get errors loading the model - try to use the same scikit-learn version.
- **If predictions look wrong**: ensure preprocessing (clean_text) matches what was used during training. If you used custom preprocessing before vectorizing in the notebook, copy that code into `model_api.py -> clean_text`.