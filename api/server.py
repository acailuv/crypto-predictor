import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn import preprocessing

import ccxt_indodax_engine as cie
import mysql_client as mc
import svc
import utils as u

load_dotenv()
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=[
                   "*"], allow_credentials=True, allow_methods="*", allow_headers="*")
mysql = mc.MySQLClient()

model = svc.SupportVectorClassifier(
    data_sample_count=50000, kernel_type="rbf", gamma=1000, C=1000, pair="BTCIDR")


class PredictionRequest(BaseModel):
    timestamp: int
    open_price: int
    high_price: int
    low_price: int
    close_price: int
    volume: float


@app.get("/health")
async def healthcheck():
    return {
        "is_healthy": True,
    }


@app.get("/predictions/{pair}/accuracy")
async def get_accuracy(pair: str):
    current_accuracy = mysql.read_common_data(
        f"{u.ACCURACY_PERCENTAGE}_{pair}", cast_to=float)

    return {
        "accuracy": current_accuracy["value"]
    }


@app.get("/predictions/{pair}/trend")
def get_predictions(pair: str):
    ccxt_engine = cie.CCXTIndodaxEngine()
    latest_data = ccxt_engine.get_latest_data()[:1]

    scaler = u.load_pickle(f"{u.SCALRERS_FOLDER}/{pair.upper()}.scaler")
    prediction_input = scaler.transform(latest_data)

    predictions = model.predict(prediction_input).tolist()

    return {
        "result": {
            "prediction": predictions[0],
            "prediction_remarks": u.humanize_prediction(predictions[0])
        },
    }


@app.get("/predictions/sample", status_code=501)
def post_predictions():
    return "Not Implemented"
