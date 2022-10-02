import React, { useEffect, useState } from "react";
import { ApiConnector } from "../utils/ApiConnector";
import { BACKEND_ENDPOINTS } from "../utils/endpoints";

function Accuracy() {
  const [accuracy, setAccuracy] = useState<number>(0);

  useEffect(() => {
    ApiConnector.get(BACKEND_ENDPOINTS.ACCURACY).then((data: any) => {
      setAccuracy(data.accuracy);
    });
  }, []);

  return (
    <h3 style={{ textAlign: "center" }}>
      Accuracy: {Math.fround(accuracy * 100)}%
    </h3>
  );
}

export default Accuracy;
