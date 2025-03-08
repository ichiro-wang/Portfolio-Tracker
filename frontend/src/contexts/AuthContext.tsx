import { createContext, ReactNode, useContext } from "react";
import { useUser } from "../features/authentication/useUser";
import { QueryObserverResult, RefetchOptions } from "@tanstack/react-query";

interface ContextProps {
  user: UserType | undefined;
  isLoading: boolean;
  refetch?: (
    options?: RefetchOptions | undefined,
  ) => Promise<QueryObserverResult<UserType, Error>>;
}

const AuthContext = createContext<ContextProps>({
  user: undefined,
  isLoading: false,
  refetch: async () =>
    ({ data: undefined, error: null }) as QueryObserverResult<UserType, Error>,
});

interface ProviderProps {
  children: ReactNode;
}

const AuthContextProvider = ({ children }: ProviderProps) => {
  const { user, isLoading, refetch } = useUser();

  return (
    <AuthContext.Provider value={{ user, isLoading, refetch }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuthContext = () => {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("AuthContext used outside Provider");
  }

  return context;
};

export default AuthContextProvider;
