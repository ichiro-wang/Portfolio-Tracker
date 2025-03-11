import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";

export const useGetStock = () => {
  const { id: fetchedId } = useParams();
  const id = fetchedId ?? "";

  const {
    data: stock,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["stock", id],
    queryFn: () => console.log(""),
    retry: false,
  });

  return { stock, isLoading, error };
};
