import { Bar } from "@ant-design/plots";
import { useEffect, useState } from "react";
import { ApiConnector } from "../utils/ApiConnector";
import { BACKEND_ENDPOINTS } from "../utils/endpoints";

const Graph = ({ importanceData }: any) => {
  if (!importanceData) return <></>;

  const data: any[] = [];

  importanceData.forEach((v: IImportanceData) => {
    data.push({
      key: v.column,
      value: v.importance,
    });
  });

  const config = {
    data,
    xField: "value",
    yField: "key",
    seriesField: "key",
    legend: {
      position: "top-left",
    },
  };
  return (
    <Bar
      {...(config as any)}
      style={{
        background: "white",
        padding: "16px",
        borderRadius: "0.375rem",
        maxWidth: "25wh",
      }}
    />
  );
};

interface IImportanceData {
  column: string;
  importance: number;
}

function VariableImportanceGraph({ pair }: any) {
  const [importanceData, setImportanceData] = useState<Array<IImportanceData>>(
    []
  );
  const [lowestImportanceData, setLowestImportanceData] =
    useState<IImportanceData>({
      column: "",
      importance: 0,
    });

  useEffect(() => {
    ApiConnector.get(BACKEND_ENDPOINTS.VARIABLE_IMPORTANCE(pair)).then(
      (data: any) => {
        setImportanceData(data.result);

        let lowest = data.result[0];
        data.result.forEach((v: any) => {
          if (v.importance < lowest.importance) {
            lowest = v;
          }
        });

        setLowestImportanceData(lowest);
      }
    );
  }, [pair]);

  return (
    <div>
      <h2>Variable Importance (%)</h2>
      <p>
        This graph shows the importance of each candle's data. In other words,
        this graph shows which variable impact the trend of the {pair}{" "}
        cryptocurrency pair in percentage.
      </p>
      <div>
        <Graph importanceData={importanceData} />
        <h4>Notes:</h4>
        <ul>
          <li>
            These values has been <u>normalized</u>.
          </li>
          <li>
            "{lowestImportanceData.column}" is the point of <u>reference</u>.
          </li>
        </ul>
      </div>
    </div>
  );
}

export default VariableImportanceGraph;
