from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI(title="ChurnGuard API")

# Debug: Print current directory and files
print("Current working directory:", os.getcwd())
print("Files in /app:", os.listdir("."))

# Load model and scaler with error handling
try:
    model = joblib.load("model/xgboost_model.pkl")
    scaler = joblib.load("model/scaler.pkl")
    print("✅ Model and Scaler loaded successfully!")
except Exception as e:
    print("❌ Error loading model/scaler:", str(e))
    model = None
    scaler = None

class CustomerData(BaseModel):
    CreditScore: int
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float
    Gender_Male: int
    Geography_Germany: int
    Geography_Spain: int

@app.post("/predict")
def predict_churn(data: CustomerData):
    if model is None or scaler is None:
        return {"error": "Model or scaler not loaded"}

    input_data = pd.DataFrame([data.dict()])
    input_scaled = scaler.transform(input_data)
    
    prediction = model.predict(input_scaled)
    probability = model.predict_proba(input_scaled)[0][1]
    
    return {
        "prediction": "Churn" if prediction[0] == 1 else "No Churn",
        "churn_probability": round(float(probability) * 100, 2)
    }

@app.get("/")
def home():
    return {"message": "ChurnGuard API is running! Go to /docs"}