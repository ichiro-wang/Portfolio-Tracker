import { ReactNode } from "react";

interface Props {
  className?: string;
  type?: "submit" | "button";
  onClick?: () => void;
  disabled?: boolean;
  children: ReactNode;
}

const Button = ({
  className = "min-w-20 bg-black text-white hover:bg-zinc-700 ",
  disabled,
  type = "button",
  onClick,
  children,
}: Props) => {
  return (
    <button
      type={type}
      disabled={disabled}
      onClick={onClick}
      className={`flex h-10 items-center justify-center rounded-full px-3 py-1 transition-colors duration-75 ${className}`}
    >
      {children}
    </button>
  );
};

export default Button;
