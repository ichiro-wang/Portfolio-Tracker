import { useEffect, useState } from "react";
import { apiTest } from "./services/apiTest";

function App() {
  const [data, setData] = useState<any>(null);
  useEffect(() => {
    const test = async () => {
      const res = await apiTest();
      setData(res);
    };
    test();
  }, []);

  console.log(data);

  return <h1>test page</h1>;
}

export default App;
