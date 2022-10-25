import React from "react";
import {
  Container,
  Nav,
  Navbar,
  Row,
  Col,
  ThemeProvider,
} from "react-bootstrap";
import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import BTCLogo from "./assets/BTC.svg";
import ETHLogo from "./assets/ETH.svg";
import USDTLogo from "./assets/USDT.svg";
import Accuracy from "./components/Accuracy";
import "animate.css";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Trend from "./components/Trend";

function App() {
  return (
    <ThemeProvider
      breakpoints={["xxxl", "xxl", "xl", "lg", "md", "sm", "xs", "xxs"]}
    >
      <Navbar bg="dark" variant="dark">
        <Container>
          <Navbar.Brand href="/">
            <img
              src={BTCLogo}
              className="animate__animated animate__pulse animate__infinite animate__slow d-inline-block align-middle"
              alt="logo"
              width={40}
              height={40}
              style={{ marginRight: "4px" }}
            />
            Trendgetter |{" "}
            <span style={{ fontWeight: "lighter" }}>
              A Forecasting Tool for Every Cryptocurrency Trendsetters.
            </span>
          </Navbar.Brand>
          <Nav className="justify-content-end">
            <Nav.Link href="/btc-idr">Forecast BTC/IDR</Nav.Link>
            <Nav.Link href="/eth-idr">Forecast ETH/IDR</Nav.Link>
            <Nav.Link href="/usdt-idr">Forecast USDT/IDR</Nav.Link>
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
      <Navbar bg="dark" variant="dark">
        <Container>
          <Navbar.Brand href="/">
            <img
              src={BTCLogo}
              className="animate__animated animate__pulse animate__infinite animate__slow d-inline-block align-middle"
              alt="logo"
              width={40}
              height={40}
              style={{ marginRight: "4px" }}
            />
            Trendgetter |{" "}
            <span style={{ fontWeight: "lighter" }}>
              A Forecasting Tool for Every Cryptocurrency Trendsetters.
            </span>
          </Navbar.Brand>
          <Nav className="justify-content-end">
            <Nav.Link href="/btc-idr">Forecast BTC/IDR</Nav.Link>
            <Nav.Link href="/eth-idr">Forecast ETH/IDR</Nav.Link>
            <Nav.Link href="/usdt-idr">Forecast USDT/IDR</Nav.Link>
          </Nav>
        </Container>
      </Navbar>
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
                  src={BTCLogo}
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
            <hr />
            <Row>
              <h4 style={{ textAlign: "center" }}>
                How Advanced is Trendgetter?
              </h4>
              <Row stlye={{ marginBottom: "64px" }}>
                <p
                  style={{
                    textAlign: "center",
                  }}
                >
                  Our cutting edge cryptocurrency trend forecasting AI has
                  achieved more than 90%<sup>*</sup> accuracy across three
                  cryptocurrency pairs.
                </p>
              </Row>
              <Row>
                <Col style={{ display: "flex", justifyContent: "center" }}>
                  <Card
                    style={{ width: "18rem", color: "black" }}
                    className="animate__animated animate__bounceInUp animate__delay-2s"
                  >
                    <Card.Header as="h5">In BTC/IDR Pair</Card.Header>
                    <Card.Img variant="top" src={BTCLogo} />
                    <Card.Body>
                      <Card.Title style={{ fontSize: "48px" }}>
                        95.730%
                      </Card.Title>
                      <Card.Text>
                        Accuracy in BTC/IDR Cryptocurrency Pair
                      </Card.Text>
                      <Button variant="primary" href="/btc-idr">
                        View BTC/IDR Trend Forecast
                      </Button>
                    </Card.Body>
                  </Card>
                </Col>
                <Col style={{ display: "flex", justifyContent: "center" }}>
                  <Card
                    style={{ width: "18rem", color: "black" }}
                    className="animate__animated animate__bounceInUp animate__delay-2s"
                  >
                    <Card.Header as="h5">In ETH/IDR Pair</Card.Header>
                    <Card.Img variant="top" src={ETHLogo} />
                    <Card.Body>
                      <Card.Title style={{ fontSize: "48px" }}>
                        99.790%
                      </Card.Title>
                      <Card.Text>
                        Accuracy in ETH/IDR Cryptocurrency Pair
                      </Card.Text>
                      <Button variant="primary" href="/eth-idr">
                        View ETH/IDR Trend Forecast
                      </Button>
                    </Card.Body>
                  </Card>
                </Col>
                <Col style={{ display: "flex", justifyContent: "center" }}>
                  <Card
                    style={{ width: "18rem", color: "black" }}
                    className="animate__animated animate__bounceInUp animate__delay-2s"
                  >
                    <Card.Header as="h5">In USDT/IDR Pair</Card.Header>
                    <Card.Img variant="top" src={USDTLogo} />
                    <Card.Body>
                      <Card.Title style={{ fontSize: "48px" }}>
                        99.790%
                      </Card.Title>
                      <Card.Text>
                        Accuracy in USDT/IDR Cryptocurrency Pair
                      </Card.Text>
                      <Button variant="primary" href="/usdt-idr">
                        View USDT/IDR Trend Forecast
                      </Button>
                    </Card.Body>
                  </Card>
                </Col>
              </Row>
              <Row stlye={{ marginBottom: "64px" }}>
                <p
                  style={{
                    textAlign: "center",
                  }}
                >
                  <sub>*Using training data from 2011 to 2021</sub>
                </p>
              </Row>
            </Row>
            <hr />
            <Row style={{ textAlign: "center" }}>
              <h4>Try Our Cryptocurrency Trend Forecaster Now!</h4>
              <p>
                So, what are you waiting for? Try our cutting edge artificial
                intelligence powered cryptocurrency pair trend forecaster now
                for <b>FREE</b>!
              </p>
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
          <Accuracy pair="BTCIDR" />
          <Trend pair="BTCIDR" />
        </Container>
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
          <Accuracy pair="ETHIDR" />
          <Trend pair="ETHIDR" />
        </Container>
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
          <Accuracy pair="USDTIDR" />
          <Trend pair="USDTIDR" />
        </Container>
      </header>
    </div>
  );
}

export default App;
