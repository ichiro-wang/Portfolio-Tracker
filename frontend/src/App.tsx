import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { Toaster } from "react-hot-toast";
import AuthContextProvider from "./contexts/AuthContext";
import ProtectedRoute from "./pages/ProtectedRoute";
import AppLayout from "./pages/AppLayout";
import Home from "./pages/Home";
import Login from "./pages/Login";
import NoPageFound from "./components/NoPageFound";
import Portfolios from "./pages/Portfolios";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 0,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthContextProvider>
        <ReactQueryDevtools initialIsOpen={false} />
        <BrowserRouter>
          <Routes>
            <Route
              element={
                <ProtectedRoute>
                  <AppLayout />
                </ProtectedRoute>
              }
            >
              <Route index element={<Navigate replace to="/home" />} />
              <Route path="/home" element={<Home />} />
              <Route path="/portfolios" element={<Portfolios />} />
            </Route>
            <Route path="/signup" element={<h1 className="text-red-500">signup</h1>} />
            <Route path="/login" element={<Login />} />
            <Route path="*" element={<NoPageFound />} />
          </Routes>
        </BrowserRouter>
        <Toaster
          position="top-center"
          gutter={12}
          containerStyle={{ margin: "8px" }}
          toastOptions={{
            success: { duration: 3000 },
            error: { duration: 5000 },
            style: {
              fontSize: "2.5rem",
              maxWidth: "500px",
              padding: "16px 24px",
              backgroundColor: "white",
              color: "grey",
            },
          }}
        />
      </AuthContextProvider>
    </QueryClientProvider>
  );
}

export default App;
