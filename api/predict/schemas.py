from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

class IrisClass(str, Enum):
    setosa = 'Setosa'
    virginica = 'Virginica'
    versicolor = 'VersiColor'

class PredictionParams(BaseModel):
    sepal_length : float 
    sepal_width : float
    petal_length : float
    petal_width : float

class PredictionRequest(BaseModel):
    data : List[PredictionParams]

class PredictionOutput(BaseModel):
    message : str
    result : List[IrisClass]   # ⬅️ hasil pakai enum, bukan angka mentah