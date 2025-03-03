import { useQuery } from "@tanstack/react-query";
import { getMe } from "../../services/apiAuth";

export const useUser = () => {
  const {
    data: user,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["user"],
    queryFn: getMe,
    retry: false,
  });

  return { user, isLoading, error };
};
