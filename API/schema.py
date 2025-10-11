from pydantic import create_model
import joblib

features = joblib.load("models/features.pkl")

# this can be useful if we are dealing with using saved features rather that creating them manually 
# CustomerData = create_model(
#     "CustomerData",
#     **{feature: (float, ...) for feature in features}
# )