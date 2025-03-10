import Box from "../components/Box";
import Button from "../components/Button";
import Loader from "../components/Loader";
import Modal from "../components/Modal";
import CreatePortfolioForm from "../features/portfolios/CreatePortfolioForm";
import PortfolioSimple from "../features/portfolios/PortfolioSimple";
import { useCreatePortfolio } from "../features/portfolios/useCreatePortfolio";
import { useGetPortfolios } from "../features/portfolios/useGetPortfolios";

const Portfolios = () => {
  const { portfolios, isLoading: isLoadingGet } = useGetPortfolios();
  const { isLoading: isLoadingCreate } = useCreatePortfolio();

  if (isLoadingGet || isLoadingCreate) {
    return <Loader />;
  }

  return (
    <div className="flex flex-col gap-3">
      {(portfolios === undefined || portfolios.length === 0) && (
        <Box className="items-center justify-center">
          <span className="">No portfolios {":("}</span>
        </Box>
      )}

      {portfolios?.map(() => {
        return (
          <Box>
            <PortfolioSimple />
          </Box>
        );
      })}

      <Box className="w-[20rem]">
        <Modal>
          <Modal.Open openName="create">
            <Button>Create</Button>
          </Modal.Open>
          <Modal.Window name="create">
            <CreatePortfolioForm />
          </Modal.Window>
        </Modal>
      </Box>
    </div>
  );
};

export default Portfolios;
