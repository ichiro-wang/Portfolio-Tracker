import FullPage from "../components/FullPage";
import Logo from "../components/Logo";
import SignupForm from "../features/authentication/SignupForm";

const Signup = () => {
  return (
    <FullPage className="flex gap-5">
      <Logo />
      <SignupForm />
    </FullPage>
  );
};

export default Signup;
