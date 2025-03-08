import { ReactNode } from "react";

interface Props {
  className?: string;
  type?: "submit" | "button";
  onClick?: () => void;
  disabled?: boolean;
  children: ReactNode;
}

const Button = ({
  className,
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
      className={`h-10 min-w-20 flex items-center justify-center rounded-full bg-black px-3 py-1 text-white hover:bg-zinc-700 ${className}`}
    >
      {children}
    </button>
  );
};

export default Button;
