import { ReactNode } from "react";
import { Link } from "react-router-dom";

interface Props {
  className?: string;
  to: string;
  children: ReactNode;
}

const ButtonLink = ({ className, to, children }: Props) => {
  return (
    <Link
      className={`flex items-center justify-center underline underline-offset-4 hover:no-underline ${className}`}
      to={to}
    >
      {children}
    </Link>
  );
};

export default ButtonLink;
