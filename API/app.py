import joblib
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel
from schema import CustomerData

app = FastAPI(title="Customer Segmentation API")

# Load model
model = joblib.load("models/customer_segmentation.pkl")