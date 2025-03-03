import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { logout as logoutApi } from "../../services/apiAuth";
import toast from "react-hot-toast";
import { useCallback } from "react";

export const useLogout = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const {
    mutate,
    isPending: isLoading,
    data: message,
    error,
  } = useMutation({
    mutationFn: () => logoutApi(),
    onSuccess: () => {
      queryClient.removeQueries();
      navigate("/login");
    },
    onError: () => {
      toast.error("Error with logout");
    },
  });

  const logout = useCallback(() => mutate(), [mutate]);

  return { logout, isLoading, message, error };
};
