import {loginTest, logoutTest, getMeTest, signupTest} from "./services/apiAuth.ts";

function App() {
  return (
      <>
        <button onClick={() => signupTest()}>signup</button>
        <button onClick={() => loginTest()}>login</button>
        <button onClick={() => logoutTest()}>logout</button>
        <button onClick={() => getMeTest()}>get me</button>
      </>
  )
}

export default App;
