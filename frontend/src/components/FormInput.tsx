interface Props {
  className?: string;
  type: string;
  id: string;
  label: string;
  defaultValue?: string | number;
  disabled: boolean;
  placeholder?: string;
}

const FormInput = ({
  className,
  type,
  id,
  label,
  defaultValue = "",
  disabled,
  placeholder,
  ...rest
}: Props) => {
  return (
    <div className="mt-2">
      <label htmlFor={id}>{label}</label>
      <input
        className={`w-full rounded-full border border-neutral-600 px-3 ${className}`}
        type={type}
        id={id}
        defaultValue={defaultValue}
        disabled={disabled}
        placeholder={placeholder}
        {...rest}
      />
    </div>
  );
};

export default FormInput;
