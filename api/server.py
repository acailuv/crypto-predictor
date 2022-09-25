from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import utils as u

import svc

app = FastAPI()

# df = pd.read_csv(f"{u.RESOURCE_FOLDER}/BTCIDR_2011-2021.csv")
# model = svc.SupportVectorClassifier(df, 50000, "rbf")


class PredictReq(BaseModel):
    openPrice: float
    highPrice: float
    lowPrice: float
    closePrice: float
    volume: float


@app.get("/health")
async def healthcheck():
    return {
        "isHealthy": True,
    }


@app.post("/predict")
async def predict(req: PredictReq):
    return req
