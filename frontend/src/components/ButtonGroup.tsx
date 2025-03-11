import { ReactNode } from "react";

interface Props {
  children: ReactNode;
}

const ButtonGroup = ({ children }: Props) => {
  return <div className="mt-7 flex gap-3">{children}</div>;
};

export default ButtonGroup;
