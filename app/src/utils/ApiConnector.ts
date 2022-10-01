export const ApiConnector = {
  get: (url: string) => {
    return fetch(url, {
      method: "GET",
      mode: "no-cors",
    }).then((res) => res.json());
  },
};
