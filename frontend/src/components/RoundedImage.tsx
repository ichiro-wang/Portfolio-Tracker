interface Props {
  src: string | undefined;
  alt: string;
}

const RoundedImage = ({ src, alt }: Props) => {
  return (
    <img
      className="h-28 w-28 rounded-full border border-black object-cover object-center leading-[7rem]"
      src={src}
      alt={alt}
    />
  );
};

export default RoundedImage;
