import React, { useEffect, useState } from "react";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { BACKEND_ENDPOINTS } from "../utils/endpoints";
import { ApiConnector } from "../utils/ApiConnector";
import { formatIDR } from "../utils/formatter";

export enum PredictionRemarks {
  Uptrend = "UPTREND",
  Sideways = "SIDEWAYS",
  Downtrend = "Downtrend",
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
    <Container>
      <Row
        style={{
          background: "lightgrey",
          textAlign: "center",
          margin: "8px",
          color: "black",
        }}
      >
        <Col xs>
          <h5>Open</h5>
        </Col>
        <Col xs>
          <h5>High</h5>
        </Col>
        <Col xs>
          <h5>Low</h5>
        </Col>
        <Col xs>
          <h5>Close</h5>
        </Col>
        <Col xs>
          <h5>Volume</h5>
        </Col>
      </Row>
      {priceData.map((v) => (
        <Row style={{ textAlign: "center", margin: "8px" }}>
          <Col xs>{formatIDR(v.open)}</Col>
          <Col xs>{formatIDR(v.high)}</Col>
          <Col xs>{formatIDR(v.low)}</Col>
          <Col xs>{formatIDR(v.close)}</Col>
          <Col xs>
            {v.volume} {cryptoCurrency}
          </Col>
        </Row>
      ))}
    </Container>
  );
}

export default PriceTable;
