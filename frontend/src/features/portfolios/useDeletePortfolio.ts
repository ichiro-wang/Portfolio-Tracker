import { useMutation, useQueryClient } from "@tanstack/react-query";
import { deletePortfolio as deletePortfolioApi } from "../../services/apiPortfolios";
import { useParams } from "react-router-dom";
import toast from "react-hot-toast";

export const useDeletePortfolio = () => {
  const queryClient = useQueryClient();
  const { id: fetchedId } = useParams();
  const id = fetchedId ?? "";

  const {
    mutate: deletePortfolio,
    isPending: isLoading,
    error,
  } = useMutation({
    mutationFn: (id: string) => deletePortfolioApi({ id }),
    onSuccess: () => {
      toast.success("Portfolio deleted");
      queryClient.removeQueries({ queryKey: ["portfolio", id] });
    },
    onError: () => {
      toast.error("Error deleting portfolio");
    },
  });

  return { deletePortfolio, isLoading, error };
};
