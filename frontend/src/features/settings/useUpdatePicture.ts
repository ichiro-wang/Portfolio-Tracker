import { useMutation, useQueryClient } from "@tanstack/react-query";
import { updatePicture as updatePictureApi } from "../../services/apiSettings";
import toast from "react-hot-toast";

export const useUpdatePicture = () => {
  const queryClient = useQueryClient();

  const {
    mutate: updatePicture,
    isPending: isLoading,
    error,
  } = useMutation({
    mutationFn: updatePictureApi,
    onSuccess: (updatedUser: UserType) => {
      toast.success("Picture updated");
      queryClient.setQueryData(["user"], (user: UserType) => {
        return { ...user, profilePic: updatedUser.profilePic };
      });
    },
    onError: () => {
      toast.error("Error updating picture");
    },
  });

  return { updatePicture, isLoading, error };
};
