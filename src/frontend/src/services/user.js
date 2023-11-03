import axios from "axios";

export const getUser = async () => {
  const res = await axios.get("/user");
  return res?.data;
};
