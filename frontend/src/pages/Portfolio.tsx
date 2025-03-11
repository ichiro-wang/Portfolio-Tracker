import Loader from "../components/Loader";
import { useGetPortfolio } from "../features/portfolios/useGetPortfolio";
import Box from "../components/Box";
import PortfolioActions from "../features/portfolios/PortfolioActions";
import { Navigate } from "react-router-dom";
import PortfolioTable from "../features/portfolios/PortfolioTable";

const Portfolio = () => {
  const { data, isLoading } = useGetPortfolio();

  if (isLoading) {
    return <Loader />;
  }

  if (!data) {
    return <Navigate to="/error" replace={true} />;
  }

  return (
    <div className="flex w-[40rem] flex-col gap-3">
      <Box className="justify-between">
        <PortfolioActions portfolio={data.portfolio} />
      </Box>
      <Box>
        <PortfolioTable />
      </Box>
    </div>
  );
};

export default Portfolio;
