import { Navigate } from "react-router-dom";
import Loader from "../components/Loader";
import { useAuthContext } from "../contexts/AuthContext";
import { formatCurrency } from "../utils/formatCurrency";

const Home = () => {
  const { user, isLoading } = useAuthContext();

  if (isLoading) {
    return <Loader />;
  }

  if (!user) {
    return <Navigate to="/login" />;
  }

  return (
    <div>
      <h1>Welcome {user?.name}</h1>
      {user.bookValue != null && (
        <p>Book Value: {formatCurrency(user.bookValue)}</p>
      )}
      {user.marketValue != null && (
        <p>Market Value: {formatCurrency(user.marketValue)}</p>
      )}
      <img src={user?.profilePic} alt="Profile Picture" />
    </div>
  );
};

export default Home;
