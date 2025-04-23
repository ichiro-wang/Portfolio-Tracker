import { ReactNode } from "react";

interface Props {
  children: ReactNode;
}
const FullDimensions = ({ children }: Props) => {
  return (
    <div className="flex h-full w-full items-center justify-center">
      {children}
    </div>
  );
};

export default FullDimensions;
