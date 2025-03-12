interface Props<T extends readonly string[]> {
  className?: string;
  id: string;
  label: string;
  options: T;
  disabled?: boolean;
}

const FormOptions = <T extends readonly string[]>({
  className,
  id,
  label,
  options,
  disabled,
  ...rest
}: Props<T>) => {
  return (
    <div className="mt-2 flex flex-col">
      <label htmlFor={id}>{label}</label>
      <select
        className={`border border-zinc-500 rounded-full px-2 ${className}`}
        name={id}
        id={id}
        disabled={disabled}
        {...rest}
      >
        {options.map((option) => {
          return (
            <option key={option} value={option}>
              {option.toUpperCase()}
            </option>
          );
        })}
      </select>
    </div>
  );
};

export default FormOptions;
