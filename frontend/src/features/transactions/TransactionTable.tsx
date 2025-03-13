import FullDimensions from "../../components/FullDimensions";
import Loader from "../../components/Loader";
import Table from "../../components/Table";
import { useGetStockTransactions } from "../stocks/useGetStockTransactions";
import TransactionRow from "./TransactionRow";

interface Props {
  stockId: number;
}

const TransactionTable = ({ stockId }: Props) => {
  const { transactions, isLoading } = useGetStockTransactions(stockId);

  if (isLoading) {
    return (
      <FullDimensions>
        <Loader />
      </FullDimensions>
    );
  }

  if (!transactions) {
    return <p>No transactions</p>;
  }

  return (
    <div className="mb-1 px-2 py-1">
      <Table columns="1fr 1fr 1fr 1fr 0.2fr">
        <Table.Header className="text-sm">
          <p>Date</p>
          <p className="text-end">Quantity</p>
          <p className="text-end">Price</p>
          <p className="text-end">Type</p>
          <p>{/* empty for delete button */}</p>
        </Table.Header>
        <Table.Body
          data={transactions}
          render={(transaction) => (
            <TransactionRow key={transaction.id} transaction={transaction} />
          )}
          noDataMessage="no data"
        ></Table.Body>
      </Table>
    </div>
  );
};

export default TransactionTable;
