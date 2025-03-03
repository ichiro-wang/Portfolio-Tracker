import axios from "axios";

export interface SignupLoginArgs {
  name?: string;
  email: string;
  password: string;
}

export const signup = async ({ name, email, password }: SignupLoginArgs): Promise<UserType> => {
  const res = await axios.post("/api/auth/signup", { name, email, password });

  if (res.data.error) {
    throw new Error(res.data.error);
  }

  return res.data;
};

export const login = async ({ email, password }: SignupLoginArgs): Promise<UserType> => {
  const res = await axios.post("/api/auth/login", { email, password });
  return res.data;
};

export const logout = async (): Promise<SimpleMessageType> => {
  const res = await axios.post("/api/auth/logout");

  if (res.data.error) {
    throw new Error(res.data.error);
  }

  return res.data;
};

export const getMe = async (): Promise<UserType> => {
  const res = await axios.get("/api/auth/me");

  if (res.data.error) {
    throw new Error(res.data.error);
  }

  return res.data;
};
