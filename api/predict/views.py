from fastapi import APIRouter, Depends, HTTPException
from api.predict.service import Predict
from api.predict.schemas import PredictionParams, PredictionOutput

predict_router = APIRouter()
tag = ["Predict"]

@predict_router.post('/predict', response_model=PredictionOutput, tags=tag)
def predict_route(data: PredictionParams):
    try:
        predict_service = Predict(params=data)
        pred = predict_service.predict()

        if not pred:
            raise HTTPException(status_code=400, detail="Prediction failed or empty result")

        return PredictionOutput(
            message=pred.get('data', ""),
            result=pred.get("result")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")