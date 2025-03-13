import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createTransaction as createTransactionApi } from "../../services/apiTransactions";
import { useParams } from "react-router-dom";
import toast from "react-hot-toast";

export const useCreateTransaction = () => {
  const queryClient = useQueryClient();
  const { id: fetchedId } = useParams();
  const id = fetchedId ?? "";

  const {
    mutate: createTransaction,
    isPending: isLoading,
    error,
  } = useMutation({
    mutationFn: createTransactionApi,
    onSuccess: (data: { stockId: number }) => {
      queryClient.refetchQueries({ queryKey: ["portfolio", id] });
      queryClient.refetchQueries({ queryKey: ["stock", String(data.stockId)] });
      toast.success("Transaction Created");
    },
    onError: () => {
      toast.error("Error recording transaction");
    },
  });

  return { createTransaction, isLoading, error };
};
