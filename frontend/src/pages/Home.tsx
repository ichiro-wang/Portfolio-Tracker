import { Navigate } from "react-router-dom";
import Button from "../components/Button";
import Loader from "../components/Loader";
import { useAuthContext } from "../contexts/AuthContext";
import { useLogout } from "../features/authentication/useLogout";
import { formatCurrency } from "../utils/formatCurrency";

const Home = () => {
  const { user, isLoading: isLoadingUser } = useAuthContext();
  const { logout, isLoading: isLoadingLogout } = useLogout();

  if (isLoadingUser) {
    return <Loader />;
  }

  if (!user) {
    return <Navigate to="/login" />;
  }

  return (
    <div>
      <h1>Welcome {user?.name}</h1>
      {user.bookValue && <p>Book Value: {formatCurrency(user.bookValue)}</p>}
      {user.marketValue && <p>Market Value: {formatCurrency(user.marketValue)}</p>}
      <img src={user?.profilePic} alt="Profile Picture" />
      <Button disabled={isLoadingLogout} onClick={logout}>
        Logout
      </Button>
    </div>
  );
};

export default Home;
