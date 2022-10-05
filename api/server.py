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


@app.get("/predictions/accuracy")
async def get_accuracy():
    current_accuracy = mysql.read_common_data(
        u.ACCURACY_PERCENTAGE, cast_to=float)

    return {
        "accuracy": current_accuracy["value"]
    }


@app.get("/predictions/{pair}/{last_n_minutes}")
def get_predictions(pair: str, last_n_minutes: int):
    ccxt_engine = cie.CCXTIndodaxEngine()
    latest_data = ccxt_engine.get_latest_data()[:last_n_minutes]

    scaler = u.load_pickle(f"{u.SCALRERS_FOLDER}/{pair.upper()}.scaler")
    prediction_input = scaler.transform(latest_data)

    res = []

    correct_predictions_count = mysql.read_common_data(
        u.CORRECT_PREDICTIONS, cast_to=int)["value"]
    total_predictions = mysql.read_common_data(
        u.CANDLES_PREDICTED, cast_to=int)["value"]
    latest_timestamp = mysql.read_common_data(
        u.LATEST_TIMESTAMP, cast_to=int)["value"]

    predictions = model.predict(prediction_input).tolist()

    for i, _ in enumerate(latest_data):
        if i == 0 or i+1 == len(latest_data):
            continue

        open_price = latest_data[i][1]
        next_close_price = latest_data[i+1][4]

        current_result = {
            "timestamp": latest_data[i][0],
            "open": latest_data[i][1],
            "high": latest_data[i][2],
            "low": latest_data[i][3],
            "close": latest_data[i][4],
            "volume": latest_data[i][5],
            "prediction": -1,
            "prediction_remarks": "",
            "is_correct_prediction": False
        }

        current_result["prediction"] = predictions[i]
        current_result["prediction_remarks"] = u.humanize_prediction(
            predictions[i])

        if open_price < next_close_price or open_price == next_close_price:
            if predictions[i] == u.UPTREND:
                current_result["is_correct_prediction"] = True

        elif open_price == next_close_price:
            if predictions[i] == u.SIDEWAYS:
                current_result["is_correct_prediction"] = True

        else:
            if predictions[i] == u.DOWNTREND:
                current_result["is_correct_prediction"] = True

        if current_result["is_correct_prediction"] and latest_data[i][0] > latest_timestamp:
            correct_predictions_count += 1

        total_predictions += 1
        res.append(current_result)

    res = sorted(res, key=lambda x: x["timestamp"], reverse=True)

    if latest_timestamp < res[0]["timestamp"]:
        new_accuracy = correct_predictions_count/total_predictions

        mysql.write_common_data(u.ACCURACY_PERCENTAGE, new_accuracy)
        mysql.write_common_data(u.CANDLES_PREDICTED, total_predictions)
        mysql.write_common_data(u.CORRECT_PREDICTIONS,
                                correct_predictions_count)
        mysql.write_common_data(u.LATEST_TIMESTAMP, res[0]["timestamp"])

    return {
        "result": res,
    }


@app.post("/predictions")
def post_predictions(req: PredictionRequest):
    scaler = u.load_pickle(f"{u.SCALRERS_FOLDER}/BTCIDR.scaler")
    prediction_input = scaler.transform(
        [[req.timestamp, req.open_price, req.high_price, req.low_price, req.close_price, req.volume]])

    predictions = model.predict(prediction_input).tolist()

    res = {
        "timestamp": req.timestamp,
        "open": req.open_price,
        "high": req.high_price,
        "low": req.low_price,
        "close": req.close_price,
        "volume": req.volume,
        "prediction": predictions[0],
    }

    return {
        "result": res,
    }


@app.get("/predictions/sample", status_code=501)
def post_predictions():
    return "Not Implemented"
