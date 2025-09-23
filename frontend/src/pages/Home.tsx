import { Navigate } from "react-router-dom";
import { formatCurrency } from "../utils/formatCurrency";
import { useUser } from "../features/authentication/useUser";
import RoundedImage from "../components/RoundedImage";
import Box from "../components/Box";

const Home = () => {
  const { user } = useUser();

  if (!user) {
    return <Navigate to="/login" />;
  }

  return (
    <div className="flex w-[30rem] flex-col gap-3">
      <Box className="items-center justify-between">
        <div>
          <RoundedImage src="/default.webp" alt="Profile Pic" />
          <h1 className="text-center">{user.name}</h1>
        </div>
        <div>
          <h1 className="text-end">Totals</h1>
          <p className="text-end">
            Book Value: {formatCurrency(user.bookValue)}
          </p>
          <p className="text-end">
            Market Value: {formatCurrency(user.marketValue)}
          </p>
        </div>
      </Box>
      <Box>
        <ul className="font-semibold">
          <li className="">The free stock api I am using has a limit.</li>
          <li>
            Market prices may not be available or may not be reflective of the
            most current values.
          </li>
        </ul>
      </Box>
    </div>
  );
};

export default Home;
