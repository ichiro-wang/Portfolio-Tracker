import { Outlet } from "react-router-dom";
import Navbar from "../components/Navbar";

const AppLayout = () => {
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
