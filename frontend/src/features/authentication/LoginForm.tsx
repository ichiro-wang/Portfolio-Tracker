import { FieldErrors, useForm } from "react-hook-form";
import { useLogin } from "./useLogin";
import { SignupLoginArgs } from "../../services/apiAuth";
import Button from "../../components/Button";
import AuthForm from "./AuthForm";
import AuthFormRow from "./AuthFormRow";
import AuthFormInput from "./AuthFormInput";
import ButtonLink from "../../components/ButtonLink";
import AuthFormButtonBox from "./AuthFormButtonBox";
import Spinner from "../../components/Spinner";

const LoginForm = () => {
  const { login, isLoading } = useLogin();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors: formErrors },
  } = useForm<SignupLoginArgs>();

  const onSubmit = ({ email, password }: SignupLoginArgs) => {
    login({ email, password }, { onSettled: () => reset() });
  };

  const onError = (errors: FieldErrors<SignupLoginArgs>) => {
    Object.values(errors).map((error) => {
      console.error(error?.message || "Error in log in");
    });
  };

  return (
    <AuthForm
      onSubmit={handleSubmit(onSubmit, onError)}
      title="Log in to Portfolio Tracker"
    >
      <AuthFormRow error={formErrors?.email?.message}>
        <AuthFormInput
          type="text"
          id="email"
          label="Email"
          disabled={isLoading}
          {...register("email", { required: "Email is required" })}
        />
      </AuthFormRow>

      <AuthFormRow error={formErrors?.password?.message}>
        <AuthFormInput
          type="password"
          id="password"
          label="Pasword"
          disabled={isLoading}
          {...register("password", { required: "Password is required" })}
        />
      </AuthFormRow>

      <AuthFormButtonBox>
        <Button type="submit" disabled={isLoading}>
          {isLoading ? <Spinner /> : "Login"}
        </Button>
        <ButtonLink to="/signup">Create an account</ButtonLink>
      </AuthFormButtonBox>
    </AuthForm>
  );
};

export default LoginForm;
