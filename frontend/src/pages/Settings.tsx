import UpdateNameForm from "../features/settings/UpdateNameForm";
import UpdatePictureForm from "../features/settings/UpdatePictureForm";
import { useUser } from "../features/authentication/useUser";
import Box from "../components/Box";
import RoundedImage from "../components/RoundedImage";
import Spinner from "../components/Spinner";
import { useUpdateName } from "../features/settings/useUpdateName";
import { useUpdatePicture } from "../features/settings/useUpdatePicture";

const Settings = () => {
  const { user } = useUser();
  const { isLoading: isLoadingName } = useUpdateName();
  const { isLoading: isLoadingPicture } = useUpdatePicture();

  const isLoading = isLoadingName || isLoadingPicture;

  return (
    <div className="flex flex-col gap-3 w-[30rem]">
      <Box className="items-center justify-between">
        {isLoading ? (
          <Spinner />
        ) : (
          <>
            <RoundedImage src={user?.profilePic} alt="Profile Pic" />
            <span>{user?.name}</span>
          </>
        )}
      </Box>
      <Box>
        <UpdateNameForm />
      </Box>
      <Box>
        <UpdatePictureForm />
      </Box>
    </div>
  );
};

export default Settings;
