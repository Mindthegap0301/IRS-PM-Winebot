<template>
  <div class="page">
    <Card class="auth-card" style="width: 400px" :title="title">
      <LoginForm v-if="mode === 'login'" @submitLogin="submitLogin"></LoginForm>
      <SignupForm
        v-if="mode === 'register'"
        @submitSignup="submitSignup"
      ></SignupForm>

      <div>
        <p v-if="mode === 'login'">
          Haven't registered for an account?
          <Button :outline="true" @click="toggleMode" type="link"
            >Create one now</Button
          >
        </p>
        <p v-else>
          Have an account?
          <Button :outline="true" @click="toggleMode" type="link"
            >Log in now</Button
          >
        </p>
      </div>
    </Card>
  </div>
</template>

<script>
import { ref, computed } from "vue";

import { useAuthStore } from "@/stores/auth.js";
import LoginForm from "@/components/library/LoginForm/LoginForm.vue";
import SignupForm from "@/components/library/SignupForm/SignupForm.vue";
import { Card, Button } from "ant-design-vue";

// import { storeToRefs } from "pinia";

export default {
  components: {
    Card,
    Button,
    LoginForm,
    SignupForm,
  },
  setup() {
    const { onLogin, onRegister } = useAuthStore();

    const mode = ref("login");

    const toggleMode = () => {
      mode.value = mode.value === "register" ? "login" : "register";
    };

    const title = computed(() => {
      return mode.value === "register" ? "Sign Up" : "Login";
    });

    return {
      mode,
      title,
      toggleMode,
      submitLogin: onLogin,
      submitSignup: onRegister,
    };
  },
};
</script>

<style scoped>
.page {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin: 0 auto;
  padding: 5rem;
  background-image: linear-gradient(
    140deg,
    #fafa6e 0%,
    #d36088 50%,
    #8962a6 75%
  );
}

.auth-card {
  margin: 0 auto;
}
</style>
