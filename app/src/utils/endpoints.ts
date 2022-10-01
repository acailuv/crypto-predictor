export const BASE_URL = process.env.REACT_APP_BASE_URL;

export const BACKEND_ENDPOINTS = {
  PREDICTIONS: (pair: string) => {
    return `${BASE_URL}/predictions/${pair}/6`;
  },
  ACCURACY: `${BASE_URL}/predictions/accuracy`,
};
