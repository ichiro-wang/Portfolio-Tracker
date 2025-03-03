import { ReactNode } from "react";
import { Link } from "react-router-dom";

interface Props {
  className?: string;
  to: string;
  children: ReactNode;
}

const ButtonLink = ({ className, to, children }: Props) => {
  return (
    <Link className={className} to={to}>
      {children}
    </Link>
  );
};

export default ButtonLink;
