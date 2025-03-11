import Box from "../components/Box";
import Button from "../components/Button";
import Loader from "../components/Loader";
import Modal from "../components/Modal";
import CreatePortfolioForm from "../features/portfolios/CreatePortfolioForm";
import PortfoliosList from "../features/portfolios/PortfoliosList";
import { useCreatePortfolio } from "../features/portfolios/useCreatePortfolio";
import { useGetPortfolios } from "../features/portfolios/useGetPortfolios";

const Portfolios = () => {
  const { isLoading: isLoadingGet } = useGetPortfolios();
  const { isLoading: isLoadingCreate } = useCreatePortfolio();

  if (isLoadingGet || isLoadingCreate) {
    return <Loader />;
  }

  return (
    <div className="flex w-[30rem] flex-col gap-3">
      <PortfoliosList />
      <Box className="items-center justify-end gap-3">
        <p>Add a portfolio</p>
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
