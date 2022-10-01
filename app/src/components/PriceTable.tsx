import React, { useEffect, useState } from "react";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { ApiConnector } from "../utils/ApiConnector";
import { BACKEND_ENDPOINTS } from "../utils/endpoints";

interface IPriceData {
  timestamp: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

function PriceTable() {
  const [priceData, setPriceData] = useState<IPriceData[]>([]);

  useEffect(() => {
    ApiConnector.get(BACKEND_ENDPOINTS.PREDICTIONS("BTCIDR")).then(
      (data: IPriceData[]) => {
        setPriceData(data);
      }
    );
  }, []);

  return (
    <Container>
      <Row>
        {/* <Col xs={{ order: "last" }}>First, but last</Col>
        <Col xs>Second, but unordered</Col>
        <Col xs={{ order: "first" }}>Third, but first</Col> */}
        {priceData.map((v) => (
          <p>{JSON.stringify(v)}</p>
        ))}
      </Row>
    </Container>
  );
}

export default PriceTable;
