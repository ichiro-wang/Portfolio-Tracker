import { useQuery } from "@tanstack/react-query";
import { getStock as getStockApi } from "../../services/apiStocks";

export const useGetStock = (id: number) => {
  const {
    data: stock,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["stock", String(id)],
    queryFn: () => getStockApi({ id }),
    retry: false,
  });

  return { stock, isLoading, error };
};
