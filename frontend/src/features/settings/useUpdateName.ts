import { useMutation, useQueryClient } from "@tanstack/react-query";
import { updateName as updateNameApi } from "../../services/apiSettings";
import toast from "react-hot-toast";

export const useUpdateName = () => {
  const queryClient = useQueryClient();

  const {
    mutate: updateName,
    isPending: isLoading,
    error,
  } = useMutation({
    mutationFn: updateNameApi,
    onSuccess: () => {
      toast.success("Name updated");
      queryClient.invalidateQueries({ queryKey: ["user"] });
    },
    onError: () => {
      toast.error("Something went wrong");
    },
  });

  return { updateName, isLoading, error };
};
