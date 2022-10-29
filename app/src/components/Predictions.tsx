import { Container, Row, Col } from "react-bootstrap";
import CryptoProfile from "./CryptoProfile";
import VariableImportanceGraph from "./VariableImportanceGraph";

function Predictions({ pair, from, to }: any) {
  return (
    <Container>
      <h1 style={{ textAlign: "center" }}>
        {from}/{to} Trend Predictions
      </h1>
      <hr />
      <Row>
        <Col xs="auto">
          <CryptoProfile pair={pair} from={from} to={to} />
        </Col>
        <Col>
          <VariableImportanceGraph pair={pair} />
        </Col>
      </Row>
    </Container>
  );
}

export default Predictions;
