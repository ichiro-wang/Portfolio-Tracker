import { useForm } from "react-hook-form";
import { useLogin } from "./useLogin";
import "react-hook-form";
import { SignupLoginArgs } from "../../services/apiAuth";
import toast from "react-hot-toast";
import Button from "../../components/Button";

const LoginForm = () => {
  const { login, isLoading } = useLogin();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors: formErrors },
  } = useForm<SignupLoginArgs>();

  const onSubmit = ({ email, password }: SignupLoginArgs) => {
    if (!email || !password) {
      return;
    }
    login({ email, password }, { onSettled: () => reset() });
  };

  const onError = (error: unknown) => {
    toast.error(error as string);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit, onError)}>
      <p>Log in to Portfolio Tracker</p>
      <div>
        <input
          className="border"
          type="text"
          id="email"
          disabled={isLoading}
          {...register("email", { required: "Email is required" })}
        />
        {formErrors.email ? <span>{formErrors.email.message}</span> : null}
      </div>

      <div>
        <input
          className="border"
          type="text"
          id="password"
          disabled={isLoading}
          {...register("password", { required: "Password is required" })}
        />
        {formErrors.password ? <span>{formErrors.password.message}</span> : null}
      </div>

      <Button type="submit" disabled={isLoading}>
        Login
      </Button>
    </form>
  );
};

export default LoginForm;
