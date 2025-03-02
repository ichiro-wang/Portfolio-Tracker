import "react-router-dom";
import { BrowserRouter, Route, Routes } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/signup" element={<h1>signup</h1>} />
        <Route path="/login" element={<h1>login</h1>} />
        <Route path="*" element={<h1>error</h1>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
