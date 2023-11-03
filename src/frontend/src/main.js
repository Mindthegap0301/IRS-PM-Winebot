import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import axios from "./plugins/axios";

const app = createApp(App);

app.use(createPinia()).use(axios, {
  baseUrl: process.env.VUE_APP_API,
});

app.mount("#app");
