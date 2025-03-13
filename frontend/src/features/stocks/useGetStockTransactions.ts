import { useQuery } from "@tanstack/react-query";
import { getStockTransactions as getStockTransactionsApi } from "../../services/apiStocks";

export const useGetStockTransactions = (id: number) => {
  const {
    data: transactions,
    isLoading,
    error,
  } = useQuery<TransactionType[]>({
    queryKey: ["stock", String(id)],
    queryFn: () => getStockTransactionsApi({ id }),
    retry: false,
  });

  return { transactions, isLoading, error };
};
