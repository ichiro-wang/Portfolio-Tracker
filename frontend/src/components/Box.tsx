import { ReactNode } from "react";

interface Props {
  children: ReactNode;
  className?: string;
}

const Box = ({ children, className }: Props) => {
  return (
    <div
      className={`flex rounded-lg border-[0.15rem] border-black px-6 py-2 ${className}`}
    >
      {children}
    </div>
  );
};

export default Box;
