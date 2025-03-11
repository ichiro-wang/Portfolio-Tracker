import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { Toaster } from "react-hot-toast";
import ProtectedRoute from "./pages/ProtectedRoute";
import AppLayout from "./pages/AppLayout";
import Home from "./pages/Home";
import Login from "./pages/Login";
import NoPageFound from "./components/NoPageFound";
import Portfolios from "./pages/Portfolios";
import Settings from "./pages/Settings";
import Signup from "./pages/Signup";
import UnprotectedRoute from "./pages/UnprotectedRoute";
import Portfolio from "./pages/Portfolio";
import FullPage from "./components/FullPage";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60000,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
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
            <Route path="/portfolios/:id" element={<Portfolio />} />
            <Route path="/settings" element={<Settings />} />
          </Route>
          <Route element={<UnprotectedRoute />}>
            <Route path="/signup" element={<Signup />} />
            <Route path="/login" element={<Login />} />
          </Route>
          <Route
            path="*"
            element={
              <FullPage>
                <NoPageFound />
              </FullPage>
            }
          />
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
            fontSize: "1.3rem",
            maxWidth: "500px",
            padding: "16px 24px",
            backgroundColor: "white",
            color: "grey",
          },
        }}
      />
    </QueryClientProvider>
  );
}

export default App;
