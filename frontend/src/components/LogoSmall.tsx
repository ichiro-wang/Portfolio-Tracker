interface Props {
  className?: string;
}

const LogoSmall = ({ className }: Props) => {
  return (
    <img
      className={`hover:rotate-12 transition-transform duration-[200]  ${className}`}
      src="/logo-small.png"
      alt="Logo"
      width={50}
    />
  );
};

export default LogoSmall;
