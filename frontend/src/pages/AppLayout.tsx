import { Outlet } from "react-router-dom";
import Navbar from "../components/Navbar";
import { useUser } from "../features/authentication/useUser";
import FullPage from "../components/FullPage";
import Loader from "../components/Loader";

const AppLayout = () => {
  const{ isLoading }=useUser()
  
  if (isLoading) {
    return <FullPage><Loader /></FullPage>
  }

  return (
    <>
      <Navbar />
      <div className="flex items-center justify-center">
        <Outlet />
      </div>
    </>
  );
};

export default AppLayout;
