import axios from "axios";

interface CreateTransactionArgs {
  portfolioId: number;
  ticker: string;
  type: "buy" | "sell";
  quantity: number;
  price: number;
  fees?: number;
  date: Date;
}

export const createTransaction = async ({
  portfolioId,
  ticker,
  type,
  quantity,
  price,
  date,
}: CreateTransactionArgs) => {
  const res = await axios.post("/api/transactions/create", {
    portfolioId,
    ticker,
    type,
    quantity,
    price,
    date,
  });

  if (res.data.error) {
    throw new Error(res.data.error);
  }

  return res.data;
};
