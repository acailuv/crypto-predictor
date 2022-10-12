import React from "react";
import {
  Container,
  Nav,
  Navbar,
  Row,
  Col,
  ThemeProvider,
} from "react-bootstrap";
import logo from "./assets/logo.svg";
import Trend from "./components/Trend";
import Table from "./components/PriceTable";
import "animate.css";
import { BrowserRouter, Route, Routes } from "react-router-dom";

function App() {
  return (
    <ThemeProvider
      breakpoints={["xxxl", "xxl", "xl", "lg", "md", "sm", "xs", "xxs"]}
    >
      <Navbar bg="dark" variant="dark">
        <Container>
          <Navbar.Brand href="/">
            <img
              src={logo}
              className="animate__animated animate__pulse animate__infinite animate__slow d-inline-block align-middle"
              alt="logo"
              width={40}
              height={40}
              style={{ marginRight: "4px" }}
            />
            Trendgetter
          </Navbar.Brand>
          <Nav className="me-auto">
            <Nav.Link href="/btc-idr">BTC/IDR</Nav.Link>
            <Nav.Link href="/eth-idr">ETH/IDR</Nav.Link>
            <Nav.Link href="/usdt-idr">USDT/IDR</Nav.Link>
          </Nav>
        </Container>
      </Navbar>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/btc-idr" element={<BTCIDR />} />
          <Route path="/eth-idr" element={<ETHIDR />} />
          <Route path="/usdt-idr" element={<USDTIDR />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

// You can think of these components as "pages"
// in your app.

function Home() {
  return (
    <div>
      <div
        className="App"
        style={{
          background: "#181E29",
          minHeight: "100vh",
          color: "white",
          padding: "1%",
        }}
      >
        <header className="App-header">
          <Container>
            <h1 style={{ textAlign: "center" }}>Welcome to Trendgetter!</h1>
            <hr />
            <Row>
              <Col xs="auto" style={{ textAlign: "center" }}>
                <img
                  src={logo}
                  className="animate__animated animate__bounceInLeft"
                  alt="logo"
                  width={300}
                  height={300}
                />
              </Col>
              <Col
                style={{
                  display: "flex",
                  flexDirection: "column",
                  justifyContent: "center",
                }}
              >
                <Row className="animate__animated animate__fadeIn">
                  <h4 style={{ paddingLeft: "0" }}>What is Trendgetter?</h4>
                </Row>
                <Row className="animate__animated animate__fadeIn animate__delay-1s">
                  Trendgetter is a state of the art cryptocurrency trend
                  forecaster that can help you identify the current trend of the
                  cryptocurrency market. Our AI uses advanced algorithm that
                  detect patterns using cryptocurrency data from 2011 to 2021.
                  With these identified patterns, our AI could make an educated
                  guess about future trend in various cryptocurrency pairs.
                </Row>
              </Col>
            </Row>
          </Container>
        </header>
      </div>
    </div>
  );
}

function BTCIDR() {
  return (
    <div
      className="App"
      style={{
        background: "#181E29",
        minHeight: "100vh",
        color: "white",
        padding: "1%",
      }}
    >
      <header className="App-header">
        <Container>
          <h1 style={{ textAlign: "center" }}>BTC/IDR Trend Prediction</h1>
          <Row></Row>
          <Trend />
        </Container>
        <Table cryptoCurrency="BTC" />
      </header>
    </div>
  );
}

function ETHIDR() {
  return (
    <div
      className="App"
      style={{
        background: "#181E29",
        minHeight: "100vh",
        color: "white",
        padding: "1%",
      }}
    >
      <header className="App-header">
        <Container>
          <h1 style={{ textAlign: "center" }}>ETH/IDR Trend Prediction</h1>
          <Row></Row>
          <Trend />
        </Container>
        <Table cryptoCurrency="ETH" />
      </header>
    </div>
  );
}

function USDTIDR() {
  return (
    <div
      className="App"
      style={{
        background: "#181E29",
        minHeight: "100vh",
        color: "white",
        padding: "1%",
      }}
    >
      <header className="App-header">
        <Container>
          <h1 style={{ textAlign: "center" }}>USDT/IDR Trend Prediction</h1>
          <Row></Row>
          <Trend />
        </Container>
        <Table cryptoCurrency="USDT" />
      </header>
    </div>
  );
}

export default App;
