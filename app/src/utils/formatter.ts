import BTCLogo from "../assets/BTC.svg";
import ETHLogo from "../assets/ETH.svg";
import USDTLogo from "../assets/USDT.svg";

export function formatIDR(n: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "IDR",
  }).format(n);
}

export function titleCase(str: string): string {
  return str.replace(/\w\S*/g, function (txt) {
    return txt.charAt(0).toUpperCase() + txt.substring(1).toLowerCase();
  });
}

export function useCryptoLogo(pair: string) {
  switch (pair) {
    case "BTCIDR":
      return BTCLogo;
    case "ETHIDR":
      return ETHLogo;
    case "USDTIDR":
      return USDTLogo;
    default:
      return BTCLogo;
  }
}
