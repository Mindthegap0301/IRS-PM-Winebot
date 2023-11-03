import axios from "axios";

axios.interceptors.request.use(function (config) {
  const token = localStorage.getItem("token");
  config.headers.Authorization = token ? `Bearer ${token}` : "";
  return config;
});

axios.defaults.baseURL = process.env.VUE_APP_API;

export default {
  install: (app, options) => {
    const token = localStorage.getItem("token");

    app.config.globalProperties.$axios = axios.create({
      baseURL: options.baseUrl,
      headers: {
        Authorization: token ? `Bearer ${token}` : "",
      },
    });
    app.config.globalProperties.$axios = axios;
  },
};
