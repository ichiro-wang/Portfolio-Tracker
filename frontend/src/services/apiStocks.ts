import axios from "axios";

interface GetStockTransactionsArgs {
  id: number;
}

export const getStockTransactions = async ({
  id,
}: GetStockTransactionsArgs) => {
  const res = await axios.get(`/api/stocks/${id}`);

  if (res.data.error) {
    throw new Error(res.data.error);
  }

  return res.data;
};

interface DeleteStockArgs {
  id: number;
}

export const deleteStock = async ({ id }: DeleteStockArgs) => {
  const res = await axios.delete(`/api/stocks/delete/${id}`);

  if (res.data.error) {
    throw new Error(res.data.error);
  }

  return res.data;
};
