interface Props {
  className?: string;
  width?: number;
}

const Logo = ({ className, width = 300 }: Props) => {
  return (
    <img className={className} src="logo-main.png" alt="Logo" width={width} />
  );
};

export default Logo;
