import { FormEventHandler, ReactNode } from "react";

interface Props {
  onSubmit: FormEventHandler<HTMLFormElement>;
  title?: string;
  children: ReactNode;
}

const Form = ({ onSubmit, title, children }: Props) => {
  return (
    <form onSubmit={onSubmit}>
      {title && <h1 className="mb-4 text-2xl font-semibold">{title}</h1>}
      {children}
    </form>
  );
};

export default Form;
