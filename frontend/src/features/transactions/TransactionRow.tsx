import { HiTrash } from "react-icons/hi2";
import Modal from "../../components/Modal";
import Table from "../../components/Table";
import { capitalizeFirstLetter } from "../../utils/capitalizeFirstLetter";
import { formatCurrency } from "../../utils/formatCurrency";
import { formatDate } from "../../utils/formatDate";
import ConfirmDelete from "../../components/ConfirmDelete";
import { useDeleteTransaction } from "./useDeleteTransaction";
import { useParams } from "react-router-dom";

interface Props {
  transaction: TransactionType;
}

const TransactionRow = ({ transaction }: Props) => {
  const { deleteTransaction, isLoading } = useDeleteTransaction();

  const { id: fetchedId } = useParams();
  const portfolioId = fetchedId === undefined ? -1 : Number(fetchedId);

  return (
    <Table.Row className="text-xs">
      <p>{formatDate(new Date(transaction.date))}</p>
      <p className="text-end">{transaction.quantity}</p>
      <p className="text-end">{formatCurrency(transaction.price)}</p>
      <p className="text-end">{capitalizeFirstLetter(transaction.type)}</p>
      <div className="flex justify-end">
        <Modal>
          <Modal.Open openName="delete">
            <div className="flex w-fit items-center justify-end rounded-full p-[0.1rem] hover:cursor-pointer hover:bg-zinc-300">
              <HiTrash />
            </div>
          </Modal.Open>
          <Modal.Window name="delete">
            <ConfirmDelete
              onClick={() =>
                deleteTransaction({ id: transaction.id, portfolioId })
              }
              disabled={isLoading}
              resourceName="transaction"
            />
          </Modal.Window>
        </Modal>
      </div>
    </Table.Row>
  );
};

export default TransactionRow;
