from pydantic import create_model
import joblib

features = joblib.load("models/features.pkl")

# this can be useful if we are dealing with using saved features rather that creating them manually 
# CustomerData = create_model(
#     "CustomerData",
#     **{feature: (float, ...) for feature in features}
# )

from pydantic import BaseModel, Field


class CustomerData(BaseModel):

    Education: float = Field(..., example=7)
    Income: float = Field(..., example=65000)

    Kidhome: float = Field(..., example=0)
    Teenhome: float = Field(..., example=1)

    Recency: float = Field(..., example=20)

    Wines: float = Field(..., example=450)
    Fruits: float = Field(..., example=30)
    Meat: float = Field(..., example=250)
    Fish: float = Field(..., example=60)
    Sweets: float = Field(..., example=35)
    Gold: float = Field(..., example=80)

    NumDealsPurchases: float = Field(..., example=3)
    NumWebPurchases: float = Field(..., example=8)
    NumCatalogPurchases: float = Field(..., example=4)
    NumStorePurchases: float = Field(..., example=10)
    NumWebVisitsMonth: float = Field(..., example=5)

    Customer_For: float = Field(..., example=3000)

    Age: float = Field(..., example=45)

    Spent: float = Field(..., example=900)