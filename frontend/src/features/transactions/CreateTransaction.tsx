import { useForm } from "react-hook-form";
import { useParams } from "react-router-dom";

interface Props {
  onCloseModal?: () => void;
}

const CreateTransaction = ({ onCloseModal }: Props) => {
  const { id: fetchedId } = useParams();
  const id = fetchedId ?? "";

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<TransactionType>();

  const onSubmit = ({ date, quantity, price, type }: TransactionType) => {};
};

export default CreateTransaction;
