import { Card, ListGroup } from "react-bootstrap";
import { useCryptoLogo } from "../utils/formatter";
import { BsArrowLeftRight, BsFillCaretRightFill } from "react-icons/bs";
import Accuracy from "./Accuracy";
import Trend from "./Trend";

function CryptoProfile({ pair, from, to }: any) {
  return (
    <Card style={{ width: "18rem", color: "black", textAlign: "center" }}>
      <Card.Img variant="top" src={useCryptoLogo(pair)} />
      <Card.Body>
        <Card.Title>
          The {from}/{to} Pair
        </Card.Title>
        <Card.Text>
          Check out the {pair} cryptocurrency pair details and predictions.
        </Card.Text>
      </Card.Body>
      <ListGroup className="list-group-flush">
        <ListGroup.Item>
          <b>Exchanges</b> {from} <BsArrowLeftRight /> {to}
        </ListGroup.Item>
        <ListGroup.Item>
          <b>Model Accuracy</b> is at{" "}
          <u>
            <Accuracy pair={pair} />
          </u>
        </ListGroup.Item>
        <ListGroup.Item>
          <b>Future Trend</b> <BsFillCaretRightFill /> <Trend pair={pair} />
        </ListGroup.Item>
      </ListGroup>
      <Card.Body>
        <Card.Link href={`https://indodax.com/market/${pair}`} target="_blank">
          Live {pair} Charts
        </Card.Link>
      </Card.Body>
    </Card>
  );
}

export default CryptoProfile;
