import axios from "axios";

export const getPortfolios = async () => {
  const res = await axios.get("/api/portfolios/all");

  if (res.data.error) {
    throw new Error(res.data.error);
  }

  return res.data;
};

export interface CreatePortfolioArgs {
  name: string;
}

export const createPortfolio = async ({ name }: CreatePortfolioArgs) => {
  const res = await axios.post("/api/portfolios/create", { name });

  if (res.data.error) {
    throw new Error(res.data.error);
  }

  return res.data;
};

interface GetDeletePortfolioArgs {
  id: string;
}

export const getPortfolio = async ({ id }: GetDeletePortfolioArgs) => {
  const res = await axios.get(`/api/portfolios/${id}`);

  if (res.data.error) {
    throw new Error(res.data.error);
  }

  return res.data;
};

export const deletePortfolio = async ({ id }: GetDeletePortfolioArgs) => {
  const res = await axios.delete(`/api/portfolios/delete/${id}`);

  if (res.data.error) {
    throw new Error(res.data.error);
  }

  return res.data;
};
