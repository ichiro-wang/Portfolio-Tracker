import { useQuery } from "@tanstack/react-query";
import { getPortfolio as getPortfolioApi } from "../../services/apiPortfolios";
import { useParams } from "react-router-dom";

export const useGetPortfolio = () => {
  const { id: fetchedId } = useParams();
  const id = fetchedId ?? "";

  const {
    data: portfolio,
    isLoading,
    error,
  } = useQuery<PortfolioType>({
    queryFn: () => getPortfolioApi({ id }),
    queryKey: ["portfolio", id],
    retry: false,
  });

  return { portfolio, isLoading, error };
};
