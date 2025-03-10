import { createContext, ReactNode, useContext, useEffect, useState } from "react";
import { useUser } from "../features/authentication/useUser";

interface ContextProps {
  user: UserType | undefined;
  isLoading: boolean;
}

const AuthContext = createContext<ContextProps>({
  user: undefined,
  isLoading: false,
});

interface ProviderProps {
  children: ReactNode;
}

const AuthContextProvider = ({ children }: ProviderProps) => {
  const { user: fetchedUser, isLoading } = useUser();
  const [user, setUser] = useState<UserType | undefined>(fetchedUser);
  
  useEffect(() => {
    setUser(fetchedUser)
  }, [fetchedUser])

  return (
    <AuthContext.Provider value={{ user, isLoading }}>
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
