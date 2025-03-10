import { useMutation, useQueryClient } from "@tanstack/react-query";
import { signup as signupApi, SignupArgs } from "../../services/apiAuth";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";

export const useSignup = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const {
    mutate: signup,
    data: user,
    isPending: isLoading,
    error,
  } = useMutation({
    mutationFn: ({ name, email, password }: SignupArgs) =>
      signupApi({ name, email, password }),
    onSuccess: (user) => {
      queryClient.setQueryData(["user"], user);
      navigate("/home");
    },

    onError: () => {
      toast.error("Error with signup");
    },
  });

  return { signup, user, isLoading, error };
};
