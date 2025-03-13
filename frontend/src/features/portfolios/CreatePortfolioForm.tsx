import Form from "../../components/Form";
import { FieldErrors, useForm } from "react-hook-form";
import { CreatePortfolioArgs } from "../../services/apiPortfolios";
import { useCreatePortfolio } from "./useCreatePortfolio";
import FormRow from "../../components/FormRow";
import FormInput from "../../components/FormInput";
import Button from "../../components/Button";
import Spinner from "../../components/Spinner";
import ButtonGroup from "../../components/ButtonGroup";

interface Props {
  onCloseModal?: () => void;
} 

const CreatePortfolioForm = ({ onCloseModal }: Props) => {
  const { createPortfolio, isLoading } = useCreatePortfolio();

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<CreatePortfolioArgs>();

  const onSubmit = ({ name }: CreatePortfolioArgs) => {
    createPortfolio(
      { name },
      {
        onSettled: () => {
          reset();
          onCloseModal?.();
        },
      },
    );
  };

  const onError = (errors: FieldErrors<CreatePortfolioArgs>) => {
    Object.values(errors).map((error) => {
      console.error(error.message);
    });
  };

  return (
    <Form onSubmit={handleSubmit(onSubmit, onError)} title="Create Portfolio">
      <FormRow error={errors?.name?.message}>
        <FormInput
          disabled={isLoading}
          id="name"
          label="Name"
          type="text"
          {...register("name", { required: "Name is required" })}
        />
      </FormRow>
      <ButtonGroup>
        <Button
          disabled={isLoading}
          onClick={() => {
            reset();
            onCloseModal?.();
          }}
        >
          Cancel
        </Button>
        <Button disabled={isLoading} type="submit">
          {isLoading ? <Spinner /> : "Create"}
        </Button>
      </ButtonGroup>
    </Form>
  );
};

export default CreatePortfolioForm;
