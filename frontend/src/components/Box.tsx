import { ReactNode } from "react";

interface Props {
  children: ReactNode;
  onClick?: () => void;
  className?: string;
}

const Box = ({ children, onClick, className }: Props) => {
  return (
    <div
      onClick={onClick}
      className={`flex rounded-lg border-[0.15rem] border-black px-6 py-2 ${className}`}
    >
      {children}
    </div>
  );
};

export default Box;
