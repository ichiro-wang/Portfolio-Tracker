import axios from "axios";

export interface UpdateNameArgs {
  name: string;
}
export const updateName = async ({ name }: UpdateNameArgs) => {
  const res = await axios.post("/api/settings/update/name", { name });

  if (res.data.error) {
    throw new Error(res.data.error);
  }

  return res.data;
};
 
export interface UpdatePictureArgs {
  image: File;
}

export const updatePicture = async ({ image }: UpdatePictureArgs) => {
  const formData = new FormData();
  formData.append("image", image);

  const res = await axios.post("/api/settings/update/picture", formData);

  if (res.data.error) {
    throw new Error(res.data.error);
  }

  return res.data;
};
