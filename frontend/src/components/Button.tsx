import { ReactNode } from "react";

interface Props {
  className?: string;
  type?: "submit" | "button";
  onClick?: () => void;
  disabled?: boolean;
  children: ReactNode;
}

const Button = ({ className, disabled, type="button", onClick, children }: Props) => {
  return (
    <button type={type} disabled={disabled} onClick={onClick} className={className}>
      {children}
    </button>
  );
};

export default Button;
