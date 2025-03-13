import { useMutation, useQueryClient } from "@tanstack/react-query";
import { deletePortfolio as deletePortfolioApi } from "../../services/apiPortfolios";
import toast from "react-hot-toast";
import { useNavigate } from "react-router-dom";

export const useDeletePortfolio = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const {
    mutate: deletePortfolio,
    isPending: isLoading,
    error,
  } = useMutation({
    mutationFn: (id: string) => deletePortfolioApi({ id }),
    onSuccess: (data: { deletedId: number }) => {
      console.log(data.deletedId);
      toast.success("Portfolio deleted");
      queryClient.removeQueries({
        queryKey: ["portfolio", String(data.deletedId)],
      });
      queryClient.setQueryData(
        ["portfolios"],
        (oldPortfolios: PortfolioType[] = []) => {
          return oldPortfolios.filter(
            (portfolio) => portfolio.id !== data.deletedId,
          );
        },
      );
      navigate("/portfolios", { replace: true });
    },
    onError: () => {
      toast.error("Error deleting portfolio");
    },
  });

  return { deletePortfolio, isLoading, error };
};
