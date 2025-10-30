<div align="center">

# Customer Segmentation API

**Turn raw marketing data into actionable customer segments - served over a modern REST API.**

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![pandas](https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/)

An end-to-end machine-learning project that groups customers from a marketing campaign into
**four data-driven segments** and serves the trained model through a lightweight FastAPI service.

</div>

---

## Overview

Understanding *who* your customers are is the first step toward marketing that actually converts.
This project takes a real marketing-campaign dataset, engineers meaningful customer features,
reduces them with **PCA**, clusters the customers with **Agglomerative Clustering** (validated with
the elbow method on K-Means), and packages everything behind a REST API.

Give the API a customer profile and it instantly replies with:

- the **cluster** the customer belongs to,
- a human-readable **segment name**, and
- a ready-to-use marketing **recommendation**.

### Features

- End-to-end notebook: cleaning -> feature engineering -> encoding -> scaling -> PCA -> clustering
- Trained artifacts saved with `joblib` and reloaded by the API
- FastAPI service with automatic interactive docs at `/docs`
- Strict request validation through a Pydantic schema generated from the saved feature order
- Every cluster mapped to a marketing playbook (loyalty, discounts, recommendations, retention)

## Project Structure

````text
customer-segmentation/
|
+-- marketing_campaign.csv      # Raw campaign dataset (2,240 customers)
+-- segment.ipynb               # Full ML workflow: EDA, preprocessing, PCA, clustering
|
+-- API/
    +-- app.py                  # FastAPI application (/, /features, /predict)
    +-- schema.py               # Pydantic request schema (24 engineered features)
    +-- requirements.txt        # Python dependencies
    +-- models/
        +-- customer_segmentation.pkl     # Trained clustering model
        +-- customer_response_model.pkl   # Trained response model
        +-- features.pkl                  # Canonical feature order
````

## Dataset

`marketing_campaign.csv` contains **2,240 customers** described by 29 attributes:

| Group | Columns |
|---|---|
| People | `ID`, `Year_Birth`, `Education`, `Marital_Status`, `Income`, `Kidhome`, `Teenhome`, `Dt_Customer`, `Recency` |
| Products | `MntWines`, `MntFruits`, `MntMeatProducts`, `MntFishProducts`, `MntSweetProducts`, `MntGoldProds` |
| Purchases | `NumWebPurchases`, `NumCatalogPurchases`, `NumStorePurchases`, `NumDealsPurchases`, `NumWebVisitsMonth` |
| Campaigns | `AcceptedCmp1`-`AcceptedCmp5`, `Complain`, `Response` |

From these raw columns the notebook engineers richer features such as `Age`, `Spent`,
`Children`, `Family_Size`, `Is_Parent`, `Customer_For` and `Total_Promos`.

## Machine-Learning Pipeline

1. **Cleaning** - drop missing incomes, parse `Dt_Customer`, cap outlier ages and incomes
2. **Feature engineering** - `Customer_For`, `Spent`, `Children`, `Family_Size`, `Is_Parent`, `Total_Promos`
3. **Encoding** - `LabelEncoder` for the remaining categorical columns
4. **Scaling** - `StandardScaler` so no feature dominates the distance metrics
5. **Dimensionality reduction** - `PCA(n_components=3)` for clustering and visualisation
6. **Clustering** - elbow method with `KElbowVisualizer` -> **4 clusters** via `AgglomerativeClustering`
7. **Export** - model and feature order persisted with `joblib` into `API/models/`

## The Four Customer Segments

| Cluster | Segment | Profile | Marketing action |
|:---:|---|---|---|
| 0 | **Premium Customers** | High spenders with a strong income | Offer loyalty rewards |
| 1 | **Budget Customers** | Cost-conscious, deal-driven shoppers | Send discounts |
| 2 | **Regular Customers** | Steady, average purchasers | Recommend products |
| 3 | **Inactive Customers** | Lapsed or low-engagement buyers | Run a retention campaign |

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check / welcome message |
| `GET` | `/features` | Returns the canonical feature order used by the model |
| `POST` | `/predict` | Classifies a customer into one of the four segments |

FastAPI also serves **interactive documentation** at `/docs` (Swagger UI) and `/redoc`.

## Example Request

````bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Education": 7, "Income": 65000,
    "Kidhome": 0, "Teenhome": 1, "Recency": 20,
    "Wines": 450, "Fruits": 30, "Meat": 250,
    "Fish": 60, "Sweets": 35, "Gold": 80,
    "NumDealsPurchases": 3, "NumWebPurchases": 8,
    "NumCatalogPurchases": 4, "NumStorePurchases": 10,
    "NumWebVisitsMonth": 5, "Customer_For": 3000,
    "Age": 45, "Spent": 900, "Living_With": 1,
    "Children": 1, "Family_Size": 3, "Is_Parent": 1,
    "Total_Promos": 2
  }'
````

**Response**

````json
{
  "cluster": 0,
  "segment": "Premium Customers",
  "recommendation": "Offer loyalty rewards"
}
````
