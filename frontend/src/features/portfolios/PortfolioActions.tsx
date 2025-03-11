import { HiOutlinePlusCircle, HiTrash } from "react-icons/hi2";
import { formatCurrency } from "../../utils/formatCurrency";
import Modal from "../../components/Modal";
import Button from "../../components/Button";

interface Props {
  portfolio: PortfolioType;
}

const PortfolioActions = ({ portfolio }: Props) => {
  return (
    <>
      <div className="flex flex-col justify-center">
        <span className="font-bold">{portfolio.name}</span>
        <div className="grid grid-cols-2">
          <span>Book Value:&nbsp;</span>
          <span>{formatCurrency(portfolio.bookValue)}</span>
          <span>Market Value:&nbsp;</span>
          <span>{formatCurrency(portfolio.marketValue)}</span>
        </div>
      </div>
      <div className="flex gap-1">
        <Modal>
          <Modal.Open openName="add">
            <Button className="min-w-0 rounded-full border border-black bg-white px-2 text-black hover:bg-black hover:text-white">
              <HiOutlinePlusCircle size={24} />
            </Button>
          </Modal.Open>
          <Modal.Window name="add">
            <h1>hello</h1>
          </Modal.Window>
          <Modal.Open openName="delete">
            <Button className="min-w-0 rounded-full border border-red-500 bg-red-500 px-2 text-white hover:bg-white hover:text-red-500">
              <HiTrash size={24} />
            </Button>
          </Modal.Open>
          <Modal.Window name="delete">
            <h1>delete</h1>
          </Modal.Window>
        </Modal>
      </div>
    </>
  );
};

export default PortfolioActions;
