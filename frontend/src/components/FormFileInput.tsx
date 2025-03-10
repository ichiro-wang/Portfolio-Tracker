interface Props {
  className?: string;
  id: string;
  label: string;
  defaultValue?: string;
  disabled: boolean;
}

const FormFileInput = ({ className, id, label, disabled, ...rest }: Props) => {
  return (
    <div className="mt-2 flex flex-col">
      <label htmlFor={id}>{label}</label>
      <input
        className={`w-full border ${className}`}
        type="file"
        accept="image/*"
        id={id}
        disabled={disabled}
        {...rest}
      />
    </div>
  );
};

export default FormFileInput;
