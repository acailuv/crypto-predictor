import React, { useEffect, useState } from "react";
import { ApiConnector } from "../utils/ApiConnector";
import { BACKEND_ENDPOINTS } from "../utils/endpoints";

function Trend({ pair }: any) {
  const [trend, setTrend] = useState<string>("Loading...");

  useEffect(() => {
    ApiConnector.get(BACKEND_ENDPOINTS.TRENDS(pair)).then((data: any) => {
      setTrend(data.result.prediction_remarks);
    });
  }, [pair]);

  return (
    <h3 style={{ textAlign: "center" }}>
      The {pair} Cryptocurrency Pair is currently on a/an {trend}.
    </h3>
  );
}

export default Trend;
