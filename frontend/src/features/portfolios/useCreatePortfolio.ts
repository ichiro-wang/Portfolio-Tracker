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
    onSuccess: (newPortfolio: PortfolioType) => {
      toast.success("Portfolio created");
      queryClient.setQueryData(
        ["portfolios"],
        (oldPortfolios: PortfolioType[]) => {
          return oldPortfolios
            ? [...oldPortfolios, newPortfolio]
            : [newPortfolio];
        },
      );
      queryClient.setQueryData(["portfolio", newPortfolio.id], newPortfolio);
    },
    onError: () => {
      toast.error("Error creating portfolio");
    },
  });

  return { createPortfolio, isLoading, error };
};
