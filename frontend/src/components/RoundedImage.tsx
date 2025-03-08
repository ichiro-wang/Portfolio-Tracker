interface Props {
  src: string;
  width?: number;
}

const RoundedImage = ({ src, width = 100 }: Props) => {
  return <img src={src} alt="image" width={width} />;
};

export default RoundedImage;
