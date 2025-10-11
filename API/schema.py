from pydantic import create_model
import joblib

features = joblib.load("models/features.pkl")