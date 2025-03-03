import { Outlet } from "react-router-dom";

const AppLayout = () => {
  return (
    <>
      <h1>app layout</h1>
      <Outlet />
    </>
  );
};

export default AppLayout;
