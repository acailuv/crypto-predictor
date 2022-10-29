import React, { useEffect, useState } from "react";
import { ApiConnector } from "../utils/ApiConnector";
import { BACKEND_ENDPOINTS } from "../utils/endpoints";

function Accuracy({ pair }: any) {
  const [accuracy, setAccuracy] = useState<number>(0);

  useEffect(() => {
    ApiConnector.get(BACKEND_ENDPOINTS.ACCURACY(pair)).then((data: any) => {
      setAccuracy(data.accuracy);
    });
  }, [pair]);

  return (
    <span style={{ textAlign: "center" }}>
      {Math.fround(accuracy * 100).toFixed(3)}%
    </span>
  );
}

export default Accuracy;
