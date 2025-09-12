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
