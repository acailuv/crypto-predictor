import React, { useEffect, useState } from "react";
import { ApiConnector } from "../utils/ApiConnector";
import { BACKEND_ENDPOINTS } from "../utils/endpoints";
import { BiLineChart, BiLineChartDown } from "react-icons/bi";
import { TbChartArrows } from "react-icons/tb";
import { titleCase } from "../utils/formatter";

function predictionsIconFor(prediction?: number) {
  if (prediction === undefined) return <></>;

  switch (prediction) {
    case 0:
      return (
        <BiLineChartDown style={{ color: "red", background: "#343a40" }} />
      );
    case 1:
      return <TbChartArrows />;
    case 2:
      return (
        <BiLineChart style={{ color: "lightgreen", background: "#343a40" }} />
      );
    default:
      return <></>;
  }
}

function Trend({ pair }: any) {
  const [trend, setTrend] = useState<{
    prediction?: number;
    prediction_remarks?: string;
  }>({});

  useEffect(() => {
    ApiConnector.get(BACKEND_ENDPOINTS.TRENDS(pair)).then((data: any) => {
      setTrend(data.result);
    });
  }, [pair]);

  return (
    <span style={{ textAlign: "center" }}>
      {/* The {pair} Cryptocurrency Pair is currently on a/an {trend}. */}
      {predictionsIconFor(trend.prediction)}{" "}
      {trend.prediction_remarks ? titleCase(trend.prediction_remarks!) : ""}
    </span>
  );
}

export default Trend;
