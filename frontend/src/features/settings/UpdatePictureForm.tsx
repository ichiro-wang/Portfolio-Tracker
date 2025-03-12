import Form from "../../components/Form";
import { FieldErrors, useForm } from "react-hook-form";
import { UpdatePictureArgs } from "../../services/apiSettings";
import { useUpdatePicture } from "./useUpdatePicture";
import FormRow from "../../components/FormRow";
import FormFileInput from "../../components/FormFileInput";
import Button from "../../components/Button";
import Spinner from "../../components/Spinner";

const UpdatePictureForm = () => {
  const { updatePicture, isLoading } = useUpdatePicture();

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<{ image: FileList }>();

  const onSubmit = ({ image }: { image: FileList }) => {
    if (!image) return;

    updatePicture({ image: image[0] }, { onSettled: () => reset() });
  };

  const onError = (errors: FieldErrors<UpdatePictureArgs>) => {
    Object.values(errors).map((error) => {
      console.error(error?.message || "Error in update picture");
    });
  };

  return (
    <Form title="Update Picture" onSubmit={handleSubmit(onSubmit, onError)}>
      <FormRow error={errors?.image?.message}>
        <FormFileInput
          disabled={isLoading}
          id="image"
          label="Picture"
          {...register("image", { required: "Please upload a picture" })}
        />
      </FormRow>
      <Button disabled={isLoading} type="submit" className="mt-3 bg-black text-white hover:bg-zinc-700">
        {isLoading ? <Spinner /> : "Confirm"}
      </Button>
    </Form>
  );
};

export default UpdatePictureForm;
