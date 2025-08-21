import os
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from typing import Union, List
import statistics
import math

load_dotenv(dotenv_path='.dev.env')
api_key = os.getenv("GITHUB_API")

app = FastAPI(title='Test Project 1')

@app.get("/")
def read_root():
    return {"message": "Hello World, welcome to Test Project 1!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# predict kalkulasi sederhana
@app.get("/predict/")
def predict(
    data_id: int,
    val: List[float] = Query(...)
):
    if not val:
        return {"error": "val must not be empty"}

    avg = statistics.mean(val)
    med = statistics.median(val)
    stdev = statistics.pstdev(val)

    result = "Positive" if avg > 0.5 else "Negative"

    return {
        "data_id": data_id,
        "values": val,
        "average": avg,
        "median": med,
        "stdev": stdev,
        "prediction": result
    }

# jarak Euclidean
@app.get("/distance/")
def calc_distance(x: float, y: float):
    dist = math.sqrt(x**2 + y**2)
    return {
        "point": (x, y),
        "euclidean_distance_from_origin": dist
    }

# regresi linear sederhana
@app.get("/linear_regression/")
def linear_regression(
    x: List[float] = Query(...),
    y: List[float] = Query(...),
    predict_x: Union[float, None] = None):
    if len(x) != len(y) or len(x) == 0:
        return {"error": "x and y must have same length and not be empty"}

    x_mean = statistics.mean(x)
    y_mean = statistics.mean(y)

    # hitung intersep & estimasi parameter (ols)
    numerator = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, y))
    denominator = sum((xi - x_mean) ** 2 for xi in x)
    m = numerator / denominator if denominator != 0 else 0
    b = y_mean - m * x_mean

    response = {
        "slope_m": m,
        "intercept_b": b,
        "equation": f"y = {m:.3f}x + {b:.3f}"
    }

    # prediksi nilai baru
    if predict_x is not None:
        predicted_y = m * predict_x + b
        response["prediction_for_x"] = predict_x
        response["predicted_y"] = predicted_y

    return response