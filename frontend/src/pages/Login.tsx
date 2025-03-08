import { Link } from "react-router-dom";
import FullPage from "../components/FullPage";
import Logo from "../components/Logo";
import LoginForm from "../features/authentication/LoginForm";

const Login = () => {
  return (
    <FullPage className="flex gap-5">
      <LoginForm />
      <Logo />
      <Link to="/home">home</Link>
    </FullPage>
  );
};

export default Login;
