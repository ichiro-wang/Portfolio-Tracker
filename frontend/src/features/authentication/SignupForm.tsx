import { FieldErrors, useForm } from "react-hook-form";
import AuthForm from "./AuthForm";
import { SignupLoginArgs } from "../../services/apiAuth";
import { useSignup } from "./useSignup";
import AuthFormRow from "./AuthFormRow";
import AuthFormInput from "./AuthFormInput";
import Button from "../../components/Button";
import ButtonLink from "../../components/ButtonLink";
import AuthFormButtonBox from "./AuthFormButtonBox";
import Spinner from "../../components/Spinner";

interface SignupWithConfirm extends SignupLoginArgs {
  confirmPassword: string;
}

const SignupForm = () => {
  const { signup, isLoading } = useSignup();

  const {
    register,
    handleSubmit,
    reset,
    getValues,
    formState: { errors: formErrors },
  } = useForm<SignupWithConfirm>();

  const onSubmit = ({ name, email, password }: SignupLoginArgs) => {
    signup({ name, email, password }, { onSettled: () => reset() });
  };

  const onError = (errors: FieldErrors<SignupLoginArgs>) => {
    Object.values(errors).map((error) => {
      console.error(error?.message || "Error in sign up");
    });
  };

  return (
    <AuthForm
      onSubmit={handleSubmit(onSubmit, onError)}
      title="Sign Up for Portfolio Tracker"
    >
      <AuthFormRow error={formErrors?.name?.message}>
        <AuthFormInput
          id="name"
          label="Name"
          disabled={isLoading}
          type="text"
          {...register("name", { required: "Name is required" })}
        />
      </AuthFormRow>

      <AuthFormRow error={formErrors?.email?.message}>
        <AuthFormInput
          id="email"
          label="Email"
          disabled={isLoading}
          type="text"
          {...register("email", {
            required: "Email is required",
            pattern: {
              value: /\S+@\S+\.\S+/,
              message: "Please provide a valid email address",
            },
          })}
        />
      </AuthFormRow>

      <AuthFormRow error={formErrors?.password?.message}>
        <AuthFormInput
          id="password"
          label="Password"
          disabled={isLoading}
          type="password"
          {...register("password", {
            required: "Password is required",
            minLength: {
              value: 8,
              message: "Password must be 8 or more characters long",
            },
          })}
        />
      </AuthFormRow>

      <AuthFormRow error={formErrors?.confirmPassword?.message}>
        <AuthFormInput
          id="confirmPassword"
          label="Confirm Password"
          disabled={isLoading}
          type="password"
          {...register("confirmPassword", {
            required: "This field is required",
            validate: (value) =>
              value === getValues().password || "Passwords do not match",
          })}
        />
      </AuthFormRow>

      <AuthFormButtonBox>
        <Button type="submit" disabled={isLoading}>
          {isLoading ? <Spinner /> : "Sign up"}
        </Button>
        <ButtonLink to="/login">Log in</ButtonLink>
      </AuthFormButtonBox>
    </AuthForm>
  );
};

export default SignupForm;
