import { ReactNode } from "react";

interface Props {
  className?: string;
  onClick: () => void;
  disabled?: boolean;
  children: ReactNode;
}

const Button = ({ className, disabled, onClick, children }: Props) => {
  return (
    <button disabled={disabled} onClick={onClick} className={className}>
      {children}
    </button>
  );
};

export default Button;
