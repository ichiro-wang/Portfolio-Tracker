import { ReactNode } from "react";

interface Props {
  className?: string;
  children: ReactNode;
}

const FullPage = ({ className, children }: Props) => {
  return (
    <div
      className={`flex h-screen w-screen items-center justify-center ${className}`}
    >
      {children}
    </div>
  );
};

export default FullPage;
