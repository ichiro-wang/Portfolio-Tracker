import { FieldErrors, useForm } from "react-hook-form";
import { useLogin } from "./useLogin";
import { LoginArgs } from "../../services/apiAuth";
import Button from "../../components/Button";
import Form from "../../components/Form";
import FormRow from "../../components/FormRow";
import FormInput from "../../components/FormInput";
import ButtonLink from "../../components/ButtonLink";
import ButtonGroup from "../../components/ButtonGroup";
import Spinner from "../../components/Spinner";
import Box from "../../components/Box";

const LoginForm = () => {
  const { login, isLoading } = useLogin();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors: formErrors },
  } = useForm<LoginArgs>();

  const onSubmit = ({ email, password }: LoginArgs) => {
    login({ email, password }, { onSettled: () => reset() });
  };

  const onError = (errors: FieldErrors<LoginArgs>) => {
    Object.values(errors).map((error) => {
      console.error(error?.message || "Error in log in");
    });
  };

  return (
    <Box className="w-fit">
      <Form
        onSubmit={handleSubmit(onSubmit, onError)}
        title="Log in to Portfolio Tracker"
      >
        <FormRow error={formErrors?.email?.message}>
          <FormInput
            type="text"
            id="email"
            label="Email"
            disabled={isLoading}
            {...register("email", { required: "Email is required" })}
          />
        </FormRow>

        <FormRow error={formErrors?.password?.message}>
          <FormInput
            type="password"
            id="password"
            label="Pasword"
            disabled={isLoading}
            {...register("password", { required: "Password is required" })}
          />
        </FormRow>

        <ButtonGroup>
          <Button type="submit" disabled={isLoading}>
            {isLoading ? <Spinner /> : "Login"}
          </Button>
          <ButtonLink to="/signup">Create an account</ButtonLink>
        </ButtonGroup>
      </Form>
    </Box>
  );
};

export default LoginForm;
