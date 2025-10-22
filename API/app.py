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


    # Keep same feature order
    df = df[features]


    # Predict cluster
    cluster = model.predict(df)[0]


    cluster_information = {

        0:{
            "name":"Premium Customers",
            "action":"Offer loyalty rewards"
        },

        1:{
            "name":"Budget Customers",
            "action":"Send discounts"
        },

        2:{
            "name":"Regular Customers",
            "action":"Recommend products"
        },

        3:{
            "name":"Inactive Customers",
            "action":"Retention campaign"
        }
