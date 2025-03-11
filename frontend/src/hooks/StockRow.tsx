import { HiEllipsisVertical } from "react-icons/hi2";
import Table from "../components/Table";
import { formatCurrency } from "../utils/formatCurrency";
import Modal from "../components/Modal";

interface Props {
  stock: StockType;
}

const StockRow = ({ stock }: Props) => {
  const openPL = stock.marketValue - stock.bookValue;
  const textColor = openPL >= 0 ? "text-green-600" : "text-red-600";

  return (
    <Table.Row>
      <p className="">{stock.ticker}</p>
      <p className="text-end">{formatCurrency(stock.averagePrice)}</p>
      <p className="text-end">{formatCurrency(stock.marketPrice)}</p>
      <p className="text-end">{formatCurrency(stock.bookValue)}</p>
      <p className="text-end">{formatCurrency(stock.marketValue)}</p>
      <p className={`text-end ${textColor}`}>{formatCurrency(openPL)}</p>
      <Modal>
        <p className="flex items-center justify-center rounded-full hover:cursor-pointer">
          <HiEllipsisVertical size={16} />
        </p>
      </Modal>
    </Table.Row>
  );
};

export default StockRow;
