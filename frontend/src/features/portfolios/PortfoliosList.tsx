import Box from "../../components/Box";
import PortfolioRow from "./PortfolioRow";
import { useGetPortfolios } from "./useGetPortfolios";
import { useNavigate } from "react-router-dom";

const PortfoliosList = () => {
  const { portfolios } = useGetPortfolios();
  const navigate = useNavigate();

  return (
    <>
      {(portfolios === undefined || portfolios.length === 0) && (
        <Box className="items-center justify-center">
          <span className="">No portfolios {":("}</span>
        </Box>
      )}

      {portfolios?.map((portfolio) => {
        return (
          <Box
            onClick={() => navigate(`/portfolios/${portfolio.id}`)}
            className="justify-between hover:cursor-pointer"
            key={crypto.randomUUID()}
          >
            <PortfolioRow portfolio={portfolio} />
          </Box>
        );
      })}
    </>
  );
};

export default PortfoliosList;
