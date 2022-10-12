import React, { useEffect, useState } from "react";
import { BACKEND_ENDPOINTS } from "../utils/endpoints";
import { ApiConnector } from "../utils/ApiConnector";
import { formatIDR } from "../utils/formatter";
import { Table } from "react-bootstrap";

export enum PredictionRemarks {
  Uptrend = "UPTREND",
  Sideways = "SIDEWAYS",
  Downtrend = "DOWNTREND",
}

interface IPriceData {
  timestamp: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  prediction: number;
  prediction_remarks: PredictionRemarks;
  is_correct_predictions: boolean;
}

function PriceTable({ cryptoCurrency }: any) {
  const [priceData, setPriceData] = useState<IPriceData[]>([]);

  useEffect(() => {
    ApiConnector.get(BACKEND_ENDPOINTS.PREDICTIONS("BTCIDR")).then(
      (data: any) => {
        setPriceData(data.result);
      }
    );
  }, []);

  return (
    <Table responsive>
      <thead>
        <tr style={{ background: "white" }}>
          <th>Timestamp</th>
          <th>Open</th>
          <th>High</th>
          <th>Low</th>
          <th>Close</th>
          <th>Volume</th>
          <th>Trend Prediction</th>
          <th>Actual</th>
        </tr>
      </thead>
      <tbody>
        {priceData.map((v) => (
          <tr style={{ textAlign: "center", margin: "8px" }}>
            <td>{new Date(v.timestamp).toString()}</td>
            <td>{formatIDR(v.open)}</td>
            <td>{formatIDR(v.high)}</td>
            <td>{formatIDR(v.low)}</td>
            <td>{formatIDR(v.close)}</td>
            <td>
              {v.volume} {cryptoCurrency}
            </td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
}

export default PriceTable;
