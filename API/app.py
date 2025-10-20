import joblib
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel
from schema import CustomerData

app = FastAPI(title="Customer Segmentation API")

# Load model
model = joblib.load("models/customer_segmentation.pkl")

features = joblib.load("models/features.pkl")

@app.get("/")
def home():
    return {"message": "Customer Segmentation API is running"}

@app.get("/features")
def get_features():
    return features

@app.post("/predict")
def predict(data: CustomerData): # type: ignore

    # Convert request to dataframe
    df = pd.DataFrame(
        [data.model_dump()]
    )