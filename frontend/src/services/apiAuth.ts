import axios from "axios";

export interface SignupArgs {
  name: string;
  email: string;
  password: string;
}

export const signup = async ({
  name,
  email,
  password,
}: SignupArgs): Promise<UserType> => {
  const res = await axios.post("/api/auth/signup", { name, email, password });

  if (res.data.error) {
    throw new Error(res.data.error);
  }

  return res.data;
};

export interface LoginArgs {
  email: string;
  password: string;
}

export const login = async ({
  email,
  password,
}: LoginArgs): Promise<UserType> => {
  const res = await axios.post("/api/auth/login", { email, password });

  if (res.data.error) {
    throw new Error(res.data.error);
  }

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
