from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI(title="ChurnGuard API")

print("Current directory:", os.getcwd())
print("Files:", os.listdir("."))

# Load model and scaler
try:
    model = joblib.load("model/xgboost_model.pkl")
    scaler = joblib.load("model/scaler.pkl")
    print("✅ Model and Scaler loaded successfully!")
except Exception as e:
    print("❌ Load Error:", str(e))
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
    try:
        # Convert to DataFrame with correct column order
        input_data = pd.DataFrame([data.dict()])
        
        print("Input data columns:", input_data.columns.tolist())
        
        # Scale
        input_scaled = scaler.transform(input_data)
        
        # Predict
        prediction = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0][1]
        
        return {
            "prediction": "Churn" if prediction == 1 else "No Churn",
            "churn_probability": round(float(probability) * 100, 2)
        }
    except Exception as e:
        print("❌ Prediction Error:", str(e))
        return {"error": str(e)}

@app.get("/")
def home():
    return {"message": "ChurnGuard API is running!"}