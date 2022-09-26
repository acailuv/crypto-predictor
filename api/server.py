import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn import preprocessing
from dotenv import load_dotenv

import svc
import utils as u
import ccxt_indodax_engine as cie
import mysql_client as mc

load_dotenv()
app = FastAPI()
mysql = mc.MySQLClient()

model = svc.SupportVectorClassifier(
    data_sample_count=50000, kernel_type="rbf", gamma=1000, C=1000, pair="BTCIDR")


@app.get("/health")
async def healthcheck():
    return {
        "is_healthy": True,
    }


@app.get("/predictions/{last_n_minutes}")
async def get_predictions(last_n_minutes: int):
    ccxt_engine = cie.CCXTIndodaxEngine()
    latest_data = ccxt_engine.get_latest_data()[:last_n_minutes]

    scaler = preprocessing.StandardScaler().fit(latest_data)
    prediction_input = scaler.transform(latest_data)

    predictions = model.predict(prediction_input)

    return {
        "result": latest_data,
        "predictions": predictions.tolist()
    }
