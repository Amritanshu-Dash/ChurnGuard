from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(title="Churn Guard API")

#Load the pre-trained model
model = joblib.load("model/xgboost_model.pkl")

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

    input_data = pd.DataFrame([data.dict()])

    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)[0][1]

    return {
        "prediction": "Churn" if prediction[0] == 1 else "No Churn",
        "Churn Probability": round(probability * 100 , 2)
    }

@app.get("/")
def home():
    return {"message": "Welcome to the Churn Guard API! Use the /predict endpoint to predict customer churn."}