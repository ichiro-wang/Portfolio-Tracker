import { FieldErrors, useForm } from "react-hook-form";
import Form from "../../components/Form";
import { SignupArgs } from "../../services/apiAuth";
import { useSignup } from "./useSignup";
import FormRow from "../../components/FormRow";
import FormInput from "../../components/FormInput";
import Button from "../../components/Button";
import ButtonLink from "../../components/ButtonLink";
import ButtonGroup from "../../components/ButtonGroup";
import Spinner from "../../components/Spinner";
import Box from "../../components/Box";

interface SignupWithConfirm extends SignupArgs {
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

  const onSubmit = ({ name, email, password }: SignupArgs) => {
    signup({ name, email, password }, { onSettled: () => reset() });
  };

  const onError = (errors: FieldErrors<SignupArgs>) => {
    Object.values(errors).map((error) => {
      console.error(error?.message || "Error in sign up");
    });
  };

  return (
    <Box className="w-fit">
      <Form
        onSubmit={handleSubmit(onSubmit, onError)}
        title="Sign Up for Portfolio Tracker"
      >
        <FormRow error={formErrors?.name?.message}>
          <FormInput
            id="name"
            label="Name"
            disabled={isLoading}
            type="text"
            {...register("name", { required: "Name is required" })}
          />
        </FormRow>

        <FormRow error={formErrors?.email?.message}>
          <FormInput
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
        </FormRow>

        <FormRow error={formErrors?.password?.message}>
          <FormInput
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
        </FormRow>

        <FormRow error={formErrors?.confirmPassword?.message}>
          <FormInput
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
        </FormRow>

        <ButtonGroup>
          <Button type="submit" disabled={isLoading}>
            {isLoading ? <Spinner /> : "Sign up"}
          </Button>
          <ButtonLink to="/login">Log in</ButtonLink>
        </ButtonGroup>
      </Form>
    </Box>
  );
};

export default SignupForm;
