import { FieldErrors, useForm } from "react-hook-form";
import { useParams } from "react-router-dom";
import { useCreateTransaction } from "./useCreateTransaction";
import Form from "../../components/Form";
import FormRow from "../../components/FormRow";
import FormInput from "../../components/FormInput";
import ButtonGroup from "../../components/ButtonGroup";
import Button from "../../components/Button";
import FormOptions from "../../components/FormOptions";
import { TransactionOptions } from "../../types";
import Spinner from "../../components/Spinner";

interface Props {
  onCloseModal?: () => void;
}

const CreateTransactionForm = ({ onCloseModal }: Props) => {
  const { createTransaction, isLoading } = useCreateTransaction();

  const { id: fetchedId } = useParams();
  const portfolioId = fetchedId === undefined ? -1 : Number(fetchedId);

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<TransactionType & { portfolioId: number; ticker: string }>();

  const onSubmit = ({
    portfolioId,
    ticker,
    date,
    quantity,
    price,
    type,
  }: TransactionType & { portfolioId: number; ticker: string }) => {
    createTransaction(
      { portfolioId, ticker, date, quantity, price, type },
      { onSettled: () => onCloseModal?.() },
    );
  };

  const onError = (errors: FieldErrors) => {
    Object.values(errors).map((error) => {
      return console.error(error?.message || "Error in creating transaction");
    });
  };

  return (
    <Form
      onSubmit={handleSubmit(onSubmit, onError)}
      title="Record a Transaction"
    >
      <div className="grid w-[30rem] grid-cols-[1fr_1fr_0.5fr] gap-2">
        <input type="hidden" value={portfolioId} {...register("portfolioId")} />
        <FormRow error={errors?.date?.message}>
          <FormInput
            disabled={isLoading}
            id="date"
            label="Date"
            defaultValue={
              new Date(
                new Date().getTime() - new Date().getTimezoneOffset() * 60000,
              )
                .toISOString()
                .split("T")[0]
            }
            type="date"
            {...register("date", {
              required: "Please specify a date",
              validate: (date) => {
                const selectedDate = new Date(date);
                const today = new Date();

                // normalize both dates to only consider yyyy-mm-dd
                const selectedDateStr = selectedDate
                  .toISOString()
                  .split("T")[0];
                const todayStr = new Date(
                  today.getTime() - today.getTimezoneOffset() * 60000,
                )
                  .toISOString()
                  .split("T")[0];

                return (
                  selectedDateStr <= todayStr || "Cannot pick a future date"
                );
              },
            })}
          />
        </FormRow>

        <FormRow error={errors?.ticker?.message}>
          <FormInput
            disabled={isLoading}
            id="ticker"
            label="Ticker"
            type="text"
            placeholder="TICKER"
            {...register("ticker", { required: "Specify a ticker symbol" })}
          />
        </FormRow>
        <FormRow error={errors?.type?.message}>
          <FormOptions
            disabled={isLoading}
            id="type"
            label="Type"
            options={TransactionOptions}
            {...register("type", { required: "Please select a type" })}
          />
        </FormRow>
        <FormRow error={errors?.quantity?.message}>
          <FormInput
            disabled={isLoading}
            id="quantity"
            label="Quantity"
            defaultValue={0.0}
            type="number"
            step="any"
            {...register("quantity", {
              required: "Specify the share quantity",
              validate: (value) =>
                value > 0 || "Share quantity must be greater than 0",
            })}
          />
        </FormRow>
        <FormRow error={errors?.price?.message}>
          <FormInput
            disabled={isLoading}
            id="price"
            label="Price"
            defaultValue={0.0}
            type="number"
            step="any"
            {...register("price", {
              required: "Specify the price",
              validate: (value) => value > 0 || "Price must be greater than 0",
            })}
          />
        </FormRow>
      </div>

      <ButtonGroup className="justify-end">
        <Button
          type="button"
          disabled={isLoading}
          onClick={() => {
            reset();
            onCloseModal?.();
          }}
        >
          Cancel
        </Button>
        <Button type="submit" disabled={isLoading}>
          {isLoading ? <Spinner /> : "Confirm"}
        </Button>
      </ButtonGroup>
    </Form>
  );
};

export default CreateTransactionForm;
