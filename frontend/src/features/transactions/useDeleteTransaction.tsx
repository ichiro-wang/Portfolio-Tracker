import { useMutation, useQueryClient } from "@tanstack/react-query";
import { deleteTransaction as deleteTransactionApi } from "../../services/apiTransactions";
import { useParams } from "react-router-dom";
import toast from "react-hot-toast";

export const useDeleteTransaction = () => {
  const queryClient = useQueryClient();
  const { id: fetchedId } = useParams();
  const id = fetchedId ?? "";

  const {
    mutate: deleteTransaction,
    isPending: isLoading,
    error,
  } = useMutation({
    mutationFn: deleteTransactionApi,
    onSuccess: (data: { deletedId: number; stockId: number }) => {
      queryClient.refetchQueries({ queryKey: ["portfolio", id] });
      queryClient.refetchQueries({ queryKey: ["stock", String(data.stockId)] });
      toast.success("Transaction deleted");
    },
    onError: () => {
      toast.error("Error deleting transaction");
    },
  });

  return { deleteTransaction, isLoading, error };
};
