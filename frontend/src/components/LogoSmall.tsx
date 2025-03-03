interface Props {
  className?: string;
}

const LogoSmall = ({ className }: Props) => {
  return (
    <img className={className} src="logo-small.png" alt="Logo" width={60} />
  );
};

export default LogoSmall;
