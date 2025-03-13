import Table from "../../components/Table";
import { formatCurrency } from "../../utils/formatCurrency";
import Modal from "../../components/Modal";
import Menus from "../../components/Menus";
import {
  HiArrowsPointingIn,
  HiArrowsPointingOut,
  HiTrash,
} from "react-icons/hi2";
import ConfirmDelete from "../../components/ConfirmDelete";
import {
  createContext,
  Dispatch,
  ReactNode,
  SetStateAction,
  useContext,
  useState,
} from "react";
import { useDeleteStock } from "./useDeleteStock";
import TransactionTable from "../transactions/TransactionTable";

interface StockRowContextProps {
  stock: StockType;
  showTransactions: boolean;
  setShowTransactions: Dispatch<SetStateAction<boolean>>;
}

const StockRowContext = createContext<StockRowContextProps | undefined>(
  undefined,
);

interface StockRowProps {
  stock: StockType;
  children: ReactNode;
}

const StockRow = ({ stock, children }: StockRowProps) => {
  const [showTransactions, setShowTransactions] = useState<boolean>(false);

  return (
    <StockRowContext.Provider
      value={{ stock, showTransactions, setShowTransactions }}
    >
      <div
        className={`${showTransactions ? "mb-2 rounded-md border border-zinc-700 p-1" : ""}`}
      >
        {children}
      </div>
    </StockRowContext.Provider>
  );
};

const StockDetails = () => {
  const context = useContext(StockRowContext);
  if (!context) {
    throw new Error("StockDetails used outside StockRow component");
  }
  const { stock, showTransactions, setShowTransactions } = context;
  const { deleteStock, isLoading } = useDeleteStock();

  const openPL = stock.marketValue - stock.bookValue;
  let textColor;
  if (openPL > 0) textColor = "text-green-600";
  else if (openPL < 0) textColor = "text-red-600";
  else textColor = "text-black";

  return (
    <Table.Row>
      <p className="">{stock.ticker}</p>
      <p className="text-end">{stock.openQuantity}</p>
      <p className="text-end">{formatCurrency(stock.averagePrice)}</p>
      <p className="text-end">{formatCurrency(stock.marketPrice)}</p>
      <p className="text-end">{formatCurrency(stock.bookValue)}</p>
      <p className="text-end">{formatCurrency(stock.marketValue)}</p>
      <p className={`text-end ${textColor}`}>{formatCurrency(openPL)}</p>
      <Modal>
        <Menus.Menu>
          <Menus.Toggle id={stock.id} />
          <Menus.List id={stock.id}>
            <Menus.Button
              icon={
                showTransactions ? (
                  <HiArrowsPointingIn />
                ) : (
                  <HiArrowsPointingOut />
                )
              }
              onClick={() => setShowTransactions((show) => !show)}
            >
              Details
            </Menus.Button>
            <Modal.Open openName="delete">
              <Menus.Button icon={<HiTrash />}>Delete</Menus.Button>
            </Modal.Open>
          </Menus.List>
        </Menus.Menu>
        <Modal.Window name="delete">
          <ConfirmDelete
            resourceName="stock"
            onClick={() => deleteStock({ id: stock.id })}
            disabled={isLoading}
          />
        </Modal.Window>
      </Modal>
    </Table.Row>
  );
};

const TransactionDetailsWrapper = () => {
  const context = useContext(StockRowContext);
  if (!context) {
    throw new Error("TransactionDetails used outside StockRow component");
  }
  const { stock, showTransactions } = context;

  if (!showTransactions) return null;

  return <TransactionTable stockId={stock.id} />;
};
StockRow.StockDetails = StockDetails;
StockRow.TransactionDetails = TransactionDetailsWrapper;

export default StockRow;
