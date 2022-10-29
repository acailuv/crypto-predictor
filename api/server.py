import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, status, HTTPException
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

model = {
    "BTCIDR": svc.SupportVectorClassifier(data_sample_count=50000, kernel_type="rbf", gamma=1000, C=1000, pair="BTCIDR"),
    "ETHIDR": svc.SupportVectorClassifier(data_sample_count=50000, kernel_type="rbf", gamma=100, C=100, pair="ETHIDR"),
    "USDTIDR": svc.SupportVectorClassifier(data_sample_count=50000, kernel_type="rbf", gamma=100, C=100, pair="USDTIDR"),
}


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

    try:
        selected_model = model[u.alphanumeric_only(pair).upper()]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Pair {pair} is not supported',
        )

    predictions = selected_model.predict(prediction_input).tolist()

    return {
        "result": {
            "prediction": predictions[0],
            "prediction_remarks": u.humanize_prediction(predictions[0])
        },
    }


@app.get("/predictions/{pair}/variable-importance")
def post_predictions(pair: str):
    try:
        selected_model = model[u.alphanumeric_only(pair).upper()]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Pair {pair} is not supported',
        )

    importance = selected_model.classifier._get_coef()[0]
    columns = ["Timestamp", "Open", "High", "Low", "Close", "Volume"]
    # importance, columns = zip(*sorted(zip(importance, columns)))

    res = []
    minImp, maxImp = min(importance), max(importance)

    for i in range(len(importance)):
        importance[i] -= minImp
        importance[i] /= (maxImp - minImp)
        importance[i] *= 100

    for i in range(len(importance)):
        res.append({
            "column": columns[i],
            "importance": importance[i]
        })

    return {
        "result": res
    }
