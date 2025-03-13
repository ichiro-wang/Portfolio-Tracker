import Box from "../components/Box";
import Loader from "../components/Loader";
import PortfolioActions from "../features/portfolios/PortfolioActions";
import PortfolioTable from "../features/portfolios/PortfolioTable";
import { useGetPortfolio } from "../features/portfolios/useGetPortfolio";

const Portfolio = () => {
  const { isLoading } = useGetPortfolio();

  if (isLoading) {
    return <Loader />;
  }

  return (
    <div className="flex w-[40rem] flex-col gap-3">
      <Box className="justify-between">
        <PortfolioActions />
      </Box>
      <Box>
        <PortfolioTable />
      </Box>
    </div>
  );
};

export default Portfolio;
