import Button from "../components/Button";
import { useLogout } from "../features/authentication/useLogout";

const Home = () => {
  const { logout, isLoading } = useLogout();
  return (
    <>
      <h1>home</h1>
      <Button disabled={isLoading} onClick={logout}>
        logout
      </Button>
    </>
  );
};

export default Home;
