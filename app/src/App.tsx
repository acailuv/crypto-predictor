import React from "react";
import { Col, Container, Row } from "react-bootstrap";
import logo from "./assets/logo.svg";
import Accuracy from "./components/Accuracy";
import Table from "./components/PriceTable";
import "animate.css";

function App() {
  return (
    <div
      className="App"
      style={{ background: "#181E29", minHeight: "100vh", color: "white" }}
    >
      <header className="App-header">
        <Container>
          <h1 style={{ textAlign: "center" }}>Predict!</h1>
          <Row>
            <img
              src={logo}
              className="animate__animated animate__swing animate__infinite animate__slow"
              alt="logo"
              width={400}
              height={400}
            />
          </Row>
          <Accuracy />
        </Container>
        <Table cryptoCurrency="BTC" />
      </header>
    </div>
  );
}

export default App;
