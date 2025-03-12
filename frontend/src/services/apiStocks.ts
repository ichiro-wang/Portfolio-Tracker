import axios from "axios";

interface GetStockArgs {
  id: number;
}

export const getStock = async ({ id }: GetStockArgs) => {
  const res = await axios.get(`/api/stocks/${id}`);

  if (res.data.error) {
    throw new Error(res.data.error);
  }

  return res.data;
};
