import axios from "axios";

export const apiTest = async () => {
  return await axios.get("/api/test");
};
