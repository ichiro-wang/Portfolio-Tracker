import { useUpdateName } from "./useUpdateName";
import { FieldErrors, useForm } from "react-hook-form";
import { UpdateNameArgs } from "../../services/apiSettings";
import Form from "../../components/Form";
import FormRow from "../../components/FormRow";
import FormInput from "../../components/FormInput";
import { useUser } from "../authentication/useUser";
import Button from "../../components/Button";
import Spinner from "../../components/Spinner";

const UpdateNameForm = () => {
  const { user } = useUser();
  const { updateName, isLoading } = useUpdateName();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<UpdateNameArgs>();

  const onSubmit = ({ name }: UpdateNameArgs) => {
    if (user?.name === name) return;
    updateName({ name });
  };

  const onError = (errors: FieldErrors<UpdateNameArgs>) => {
    Object.values(errors).map((error) => {
      console.error(error?.message || "Error in updating name");
    });
  };

  return (
    <Form title="Update Name" onSubmit={handleSubmit(onSubmit, onError)}>
      <FormRow error={errors?.name?.message}>
        <FormInput
          disabled={isLoading}
          id="name"
          label="Name"
          type="text"
          defaultValue={user?.name}
          {...register("name", { required: "Name cannot be blank" })}
        />
      </FormRow>
      <Button className="mt-3" disabled={isLoading} type="submit">
        {isLoading ? <Spinner /> : "Confirm"}
      </Button>
    </Form>
  );
};

export default UpdateNameForm;
