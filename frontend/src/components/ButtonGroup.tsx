import { ReactNode } from "react";

interface Props {
  className?: string;
  children: ReactNode;
}

const ButtonGroup = ({ className, children }: Props) => {
  return <div className={`mt-7 flex gap-3 ${className}`}>{children}</div>;
};

export default ButtonGroup;
