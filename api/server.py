import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn import preprocessing

import svc
import utils as u

app = FastAPI()

# df = pd.read_csv(f"{u.RESOURCE_FOLDER}/BTCIDR_2011-2021.csv")
model = svc.SupportVectorClassifier(
    data_sample_count=50000, kernel_type="rbf", gamma=1000, C=1000, pair="BTCIDR")


class PredictReq(BaseModel):
    timestamp: float
    openPrice: float
    highPrice: float
    lowPrice: float
    closePrice: float
    volume: float


class TestReq(BaseModel):
    a: int
    b: float


class TestRes(BaseModel):
    result: str


@app.get("/health")
async def healthcheck():
    return {
        "is_healthy": True,
    }


@app.post("/predict")
async def predict(req: PredictReq):
    req = [[req.timestamp, req.openPrice, req.highPrice,
            req.lowPrice, req.closePrice, req.volume]]

    normalized_req = preprocessing.normalize(req)

    predictions = model.predict(normalized_req)

    return {
        "prediction": int(predictions[0]),
        "humanized_prediction": u.humanize_prediction(predictions[0])
    }
