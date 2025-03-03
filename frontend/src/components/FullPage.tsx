import { ReactNode } from "react";

interface Props {
  children: ReactNode;
}

const FullPage = ({ children }: Props) => {
  return <div className="w-screen h-screen flex justify-center items-center">{children}</div>;
};

export default FullPage;
