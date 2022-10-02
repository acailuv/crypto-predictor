export const ApiConnector = {
  get: (url: string) => {
    return fetch(url, {
      method: "GET",
    }).then((res) => res.json());
  },
};
