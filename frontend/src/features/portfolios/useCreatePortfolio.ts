import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createPortfolio as createPortfolioApi } from "../../services/apiPortfolios";
import toast from "react-hot-toast";

export const useCreatePortfolio = () => {
  const queryClient = useQueryClient();

  const {
    mutate: createPortfolio,
    isPending: isLoading,
    error,
  } = useMutation({
    mutationFn: createPortfolioApi,
    onSuccess: (portfolio: PortfolioType) => {
      toast.success("Portfolio created");
      queryClient.setQueryData(["portfolio", portfolio.id], portfolio);
    },
    onError: () => {
      toast.error("Error creating portfolio");
    },
  });

  return { createPortfolio, isLoading, error };
};
