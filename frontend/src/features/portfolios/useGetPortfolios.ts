import { useQuery } from "@tanstack/react-query";
import { getPortfolios as getPortfoliosApi } from "../../services/apiPortfolios";

export const useGetPortfolios = () => {
  const { data:portfolios, isLoading, error } = useQuery<PortfolioType[]>({
    queryFn: getPortfoliosApi,
    queryKey: ["portfolios"],
    retry: 1,
  });

  return { portfolios, isLoading, error };
};
