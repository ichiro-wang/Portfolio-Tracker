import { ReactNode, useEffect } from "react";
import { useUser } from "../features/authentication/useUser";
import { useNavigate } from "react-router-dom";
import FullPage from "../components/FullPage";
import Loader from "../components/Loader";

interface Props {
  children: ReactNode;
}

const ProtectedRoute = ({ children }: Props) => {
  const { user, isLoading } = useUser();
  const navigate = useNavigate();

  useEffect(() => {
    if (!user && !isLoading) navigate("/login", { replace: true });
  }, [user, isLoading, navigate]);

  if (isLoading) {
    return (
      <FullPage>
        <Loader />
      </FullPage>
    );
  }

  return children;
};

export default ProtectedRoute;
