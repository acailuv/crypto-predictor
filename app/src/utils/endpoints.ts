export const BASE_URL = process.env.REACT_APP_BASE_URL;

export const BACKEND_ENDPOINTS = {
  TRENDS: (pair: string) => {
    return `${BASE_URL}/predictions/${pair}/trend`;
  },
  ACCURACY: (pair: string) => {
    return `${BASE_URL}/predictions/${pair}/accuracy`;
  },
  VARIABLE_IMPORTANCE: (pair: string) => {
    return `${BASE_URL}/predictions/${pair}/variable-importance`;
  },
};
