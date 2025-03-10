import { ReactNode } from "react";

interface Props {
  error: string | undefined;
  children: ReactNode;
}

const FormRow = ({ error, children }: Props) => {
  return (
    <div>
      {children}
      {error && <span className="text-red-500">{error}</span>}
    </div>
  );
};

export default FormRow;
