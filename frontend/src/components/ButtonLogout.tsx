import Button from "./Button";
import { useLogout } from "../features/authentication/useLogout";
import Spinner from "./Spinner";

const ButtonLogout = () => {
  const { logout, isLoading } = useLogout();

  return (
    <Button disabled={isLoading} onClick={logout}>
      {isLoading ? <Spinner /> : "Log out"}
    </Button>
  );
};

export default ButtonLogout;
