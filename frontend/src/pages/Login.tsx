import FullPage from "../components/FullPage";
import Logo from "../components/Logo";
import LoginForm from "../features/authentication/LoginForm";

const Login = () => {
  return (
    <FullPage className="flex gap-5">
      <LoginForm />
      <Logo />
    </FullPage>
  );
};

export default Login;
