import Button from "./Button";
import { useLogout } from "../features/authentication/useLogout";

const ButtonLogout = () => {
  const { logout, isLoading } = useLogout();

  return (
    <Button disabled={isLoading} onClick={logout}>
      Log out
    </Button>
  );
};

export default ButtonLogout;
