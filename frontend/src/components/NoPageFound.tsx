import { useNavigate } from "react-router-dom";
import Button from "./Button";

const NoPageFound = () => {
  const navigate = useNavigate();
  return (
    <div className="flex flex-col gap-3">
      <h1>Error (404)</h1>
      <h1>Could not find page you are looking for</h1>
      <Button className="w-20" onClick={() => navigate(-1)}>
        Return
      </Button>
    </div>
  );
};

export default NoPageFound;
