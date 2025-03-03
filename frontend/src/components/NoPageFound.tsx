import { useNavigate } from "react-router-dom";
import Button from "./Button";

const NoPageFound = () => {
  const navigate = useNavigate();
  return (
    <>
      <h1>Error (404)</h1>
      <h1>Could not find page you are looking for</h1>
      <Button onClick={() => navigate(-1)}>Return</Button>
    </>
  );
};

export default NoPageFound;
