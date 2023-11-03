import axios from "axios";

export const generateResults = async (chatSessionId) => {
  const res = await axios.post("/chat_sessions/" + chatSessionId + "/results");
  return res?.data;
};

export const getResult = async (chatSessionId, resultId) => {
  const res = await axios.get(
    "/chat_sessions/" + chatSessionId + "/results/" + resultId
  );
  return res?.data;
};

export const getProduct = async (id) => {
  const res = await axios.get("/products/" + id);
  return res?.data;
};
