import { defineStore } from "pinia";
import jwt_decode from "jwt-decode";
import axios from "axios";

export const useAuthStore = defineStore("auth", {
  state: () => ({ user: null, loading: false }),

  actions: {
    async init() {
      try {
        const token = localStorage.getItem("token");
        let user;
        if (token) {
          user = jwt_decode(token);
        }

        if (user) {
          // Call user
          this.loading = true;
          const _userInfo = await axios.get("/user");
          if (_userInfo) {
            this.user = user;
          } else {
            await this.onLogout();
          }
          this.loading = false;
        }
      } catch (err) {
        this.onLogout();
        this.loading = false;
        throw Error(err);
      }
    },
    async onRegister(values) {
      try {
        this.loading = true;
        const resp = await axios.post("/register", values);
        const token = resp.data.token;
        localStorage.setItem("token", token);

        let user;
        if (token) {
          user = jwt_decode(token);
        }
        this.user = user;
        this.loading = false;
      } catch (err) {
        this.loading = false;
        throw Error(err);
      }
    },
    async onLogin(values) {
      try {
        this.loading = true;
        const resp = await axios.post("/login", values);
        const token = resp.data.token;
        localStorage.setItem("token", token);

        let user;
        if (token) {
          user = jwt_decode(token);
        }
        this.user = user;
        this.loading = false;
        return user;
      } catch (err) {
        this.loading = false;
        throw Error(err);
      }
    },
    async onLogout() {
      try {
        this.loading = true;
        await axios.post("/logout");
        localStorage.removeItem("token");
        this.user = null;
        this.loading = false;
      } catch (err) {
        this.loading = false;
      }
    },
  },
});
