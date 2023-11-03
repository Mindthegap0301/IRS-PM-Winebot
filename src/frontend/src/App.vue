<template>
  <LoadingBar v-if="loading"></LoadingBar>
  <ChatWindow @logout="onLogout" v-else-if="user" />
  <AuthPage v-else></AuthPage>
</template>

<script setup>
import "ant-design-vue/es/form/style/css";
import "ant-design-vue/es/button/style/css";
import "ant-design-vue/es/input/style/css";
import "ant-design-vue/es/card/style/css";
import "ant-design-vue/es/collapse/style/css";
import "ant-design-vue/es/table/style/css";
import "ant-design-vue/es/list/style/css";

import { onMounted } from "vue";

import AuthPage from "@/components/auth/AuthPage.vue";
import ChatWindow from "@/components/chat/ChatWindow/ChatWindow.vue";
import LoadingBar from "@/components/library/LoadingBar/LoadingBar.vue";

import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";

const { user, loading } = storeToRefs(useAuthStore());
const { init, onLogout } = useAuthStore();

onMounted(async () => {
  init();
});
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Roboto");

:root {
  --body-bg: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  --msger-bg: #fff;
  --border: 2px solid #ddd;
  --primary-color: rgba(207, 77, 254, 1);
}

#app {
  font-family: Roboto, Helvetica, Arial, sans-serif;
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100vh;
  width: 100vw;
}

.btn {
  padding: 0 0.5rem;
}

::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-track {
  background: #ddd;
}
::-webkit-scrollbar-thumb {
  background: #bdbdbd;
}

/* Animations */
.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
