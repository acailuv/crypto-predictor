import React from "react";
import logo from "./assets/logo.svg";
import Table from "./components/PriceTable";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1></h1>
        <img
          src={logo}
          className="App-logo"
          alt="logo"
          width={400}
          height={400}
        />
        <Table />
      </header>
    </div>
  );
}

export default App;
