import axios from "axios";

export const createChatSession = async (data) => {
  const res = await axios.post("/chat_sessions", data);
  return res?.data;
};

export const getChatSession = async (chatSessionId) => {
  const res = await axios.get("/chat_sessions/" + chatSessionId);
  return res?.data;
};

export const getChatSessions = async () => {
  const res = await axios.get("/chat_sessions");
  return res?.data;
};

export const createChat = async (data) => {
  const res = await axios.post("/chats", data);
  return res?.data;
};

export const deleteChat = async (chatId) => {
  const res = await axios.delete("/chats/" + chatId);
  return res?.data;
};

export const deleteChatSession = async (chatSessionId) => {
  const res = await axios.delete("/chat_sessions/" + chatSessionId);
  return res?.data;
};
