from fastapi import FastAPI
from api.predict.views import predict_router
from api.scheduler.views import scheduler_router

import os
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from typing import Union, List
import statistics
import math

app = FastAPI(title="TEST PROJECT 1")

# register routers
app.include_router(predict_router)
app.include_router(scheduler_router)

@app.get("/")
def read_root():
    return {"message": "Hello World, welcome to Test Project 1!"}

# predict logic sederhana
@app.get("/predict1/")
def predict1(
    data_id: int,
    val: List[float] = Query(...)
):
    if not val:
        return {"error": "val harus diisi!"}

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
        "jarak euclid (phytagoras)": dist
    }

# regresi linear sederhana
@app.get("/linear_regression/")
def linear_regression(
    x: List[float] = Query(...),
    y: List[float] = Query(...),
    predict_x: Union[float, None] = None):
    if len(x) != len(y) or len(x) == 0:
        return {"error": "x dan y harus punya panjang data yang sama!"}

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