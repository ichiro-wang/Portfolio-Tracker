interface Props {
  className?: string;
  type: string;
  id: string;
  label: string;
  disabled: boolean;
}

const AuthFormInput = ({
  className,
  type,
  id,
  label,
  disabled,
  ...rest
}: Props) => {
  return (
    <div className="mt-2">
      <label htmlFor={id}>{label}</label>
      <input
        className={`w-full border border-neutral-600 ${className}`}
        type={type}
        id={id}
        disabled={disabled}
        {...rest}
      />
    </div>
  );
};

export default AuthFormInput;
