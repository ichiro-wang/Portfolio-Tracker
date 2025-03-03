import { BrowserRouter, Route, Routes } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { Toaster } from "react-hot-toast";
import AuthContextProvider from "./contexts/AuthContext";
import FullPage from "./components/FullPage";
import Loader from "./components/Loader";
import ProtectedRoute from "./pages/ProtectedRoute";
import AppLayout from "./pages/AppLayout";
import Home from "./pages/Home";

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
              <Route path="/home" element={<Home />} />
            </Route>
            <Route path="/signup" element={<h1 className="text-red-500">signup</h1>} />
            <Route path="/login" element={<h1>login</h1>} />
            <Route path="*" element={<h1>error page</h1>} />
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
