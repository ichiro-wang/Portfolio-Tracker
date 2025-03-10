import { useEffect } from "react";
import { useUser } from "../features/authentication/useUser";
import { Outlet, useNavigate } from "react-router-dom";
import FullPage from "../components/FullPage";
import Loader from "../components/Loader";

const UnprotectedRoute = () => {
  const { user, isLoading } = useUser();
  const navigate = useNavigate();

  useEffect(() => {
    if (user && !isLoading) {
      navigate("/home", { replace: true });
    }
  }, [user, isLoading, navigate]);

  if (isLoading) {
    return (
      <FullPage>
        <Loader />
      </FullPage>
    );
  }

  return <Outlet />;
};

export default UnprotectedRoute;
