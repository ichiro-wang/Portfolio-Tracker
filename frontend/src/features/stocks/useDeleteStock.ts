import { useMutation, useQueryClient } from "@tanstack/react-query";
import { deleteStock as deleteStockApi } from "../../services/apiStocks";
import toast from "react-hot-toast";

export const useDeleteStock = () => {
  const queryClient = useQueryClient();

  const {
    mutate: deleteStock,
    isPending: isLoading,
    error,
  } = useMutation({
    mutationFn: deleteStockApi,
    onSuccess: (data: { deletedId: number; portfolioId: number }) => {
      queryClient.removeQueries({
        queryKey: ["stock", String(data.deletedId)],
      });
      queryClient.refetchQueries({
        queryKey: ["portfolio", String(data.portfolioId)],
      });
      toast.success("Stock deleted");
    },
    onError: () => {
      toast.error("Error deleting stock");
    },
  });

  return { deleteStock, isLoading, error };
};
