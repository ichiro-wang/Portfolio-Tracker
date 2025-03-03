import { memo } from "react";
import { useLogout } from "../features/authentication/useLogout";
import Button from "./Button";
import ButtonLink from "./ButtonLink";

const Navbar = memo(function Navbar() {
  const { logout, isLoading } = useLogout();

  return (
    <nav className="my-5 mx-3 flex items-center gap-2">
      <img src="logo-small.png" alt="Logo" width={60} />
      <ButtonLink to="/home">Home</ButtonLink>
      <ButtonLink to="/portfolios">Portfolios</ButtonLink>
      <ButtonLink to="/settings">Settings</ButtonLink>
      <Button disabled={isLoading} onClick={logout}>
        Logout
      </Button>
    </nav>
  );
});

export default Navbar;
