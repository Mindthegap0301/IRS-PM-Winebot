<template>
  <section class="msger">
    <div :class="`msger__chat-list-container ${isOpenSidebar ? '--open' : ''}`">
      <ChatList
        v-if="chatSessions && chatSessions.length"
        :chatSessions="chatSessions"
        @selectItem="selectChatSession"
        @createChatSession="handleCreateChatSession"
        @close="toggleOpenSidebar"
      />
    </div>

    <div class="msger-content">
      <header class="msger-header">
        <div class="msger-toggle-side">
          <Button
            type="ghost"
            @click="toggleOpenSidebar"
            class="msger-toggle-side-btn btn"
            >More</Button
          >
        </div>

        <div class="msger-header-title">
          <i class="fas fa-bug"></i> {{ get(chatSession, "name", "") }}
          <i class="fas fa-bug"></i>
        </div>

        <div class="msger-logout">
          <Button type="ghost" @click="logout" class="msger-logout-btn btn"
            >Logout</Button
          >
        </div>
      </header>

      <div class="msger-result-body" v-if="results && Array.isArray(results)">
        <ResultsIndex :results="results" :fetchResult="fetchResult" />
      </div>

      <div v-else class="msger-body">
        <main class="msger-chat" ref="chatWindow">
          <ChatMessage
            v-for="(msg, index) in messages"
            :key="msg.id"
            v-bind="msg"
            :username="msg.createdBy === 'user' ? userInfo.id : 'Bot'"
            @select-option="onSelectOption"
            :disableOptions="index !== messages.length - 1"
          />
        </main>

        <div class="msger-inputarea-container">
          <transition name="fade"
            ><Button
              v-if="
                chatSessionStatus === 'ready' ||
                chatSessionStatus === 'complete'
              "
              :block="true"
              html-type="button"
              class="msger__success-btn"
              @click="handleGenerateResults"
              >Get results!</Button
            ></transition
          >

          <form @submit="submitMessage" class="msger-inputarea">
            <Textarea
              v-model:value="messageText"
              class="msger-input"
              id="textInput"
              placeholder="Enter your message..."
              ref="messageInput"
              :auto-size="{ minRows: 4, maxRows: 12 }"
            />
            <Button
              type="primary"
              html-type="submit"
              class="msger-send-btn"
              :disabled="!messageText"
              >Send</Button
            >
          </form>
        </div>
      </div>

      <transition name="fade">
        <div class="msger__load" v-if="isLoading">
          <LoadingBar />
        </div>
      </transition>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref, watch, onUpdated, defineEmits } from "vue";

// plugins
import get from "lodash.get";
import scrollIntoView from "scroll-into-view-if-needed";

// components
import { Button, Textarea } from "ant-design-vue";
import ChatMessage from "@/components/chat/ChatWindow/ChatMessage.vue";
import ChatList from "@/components/chat/ChatWindow/ChatList.vue";
import ResultsIndex from "@/components/chat/Results/ResultsIndex.vue";
import LoadingBar from "@/components/library/LoadingBar/LoadingBar.vue";

// API
import { getUser } from "@/services/user";
import {
  getChatSessions,
  getChatSession,
  createChat,
  createChatSession,
} from "@/services/chats";
import { generateResults, getOccupation } from "@/services/results";

// Template refs
const chatWindow = ref(null);
const messageInput = ref(null);
// Bind message text to this variable
const messageText = ref("");

const isLoading = ref(false);
const isFirstLoad = ref(true);
const chatSessions = ref(null);
const messages = ref([]);
const userInfo = ref(null);
const chatSession = ref(null);
const selectedChatSessionId = ref(null);
const chatSessionStatus = ref(null);
const isOpenSidebar = ref(false);

const emit = defineEmits(["logout"]);

const logout = () => {
  emit("logout");
};

const getChatSessionsList = async () => {
  chatSessions.value = await getChatSessions();
};

const toggleOpenSidebar = () => {
  isOpenSidebar.value = !isOpenSidebar.value;
};

const selectChatSession = (item) => {
  selectedChatSessionId.value = item.id;
  chatSessionStatus.value = item.status;
  isFirstLoad.value = true;
};

onMounted(async () => {
  const _userInfo = await getUser();
  userInfo.value = _userInfo;

  if (userInfo.value?.lastChatSessionId) {
    selectedChatSessionId.value = userInfo.value?.lastChatSessionId;
  } else {
    isLoading.value = true;
    selectedChatSessionId.value = get(
      await createChatSession({
        name: _userInfo.username,
      }),
      "id"
    );
    isLoading.value = false;
  }

  getChatSessionsList();
});

watch([selectedChatSessionId], async ([selectedChatSessionId]) => {
  if (chatSession.value?.id !== selectedChatSessionId) {
    isLoading.value = true;
    const _chatSession = await getChatSession(selectedChatSessionId);
    chatSession.value = _chatSession;
    chatSessionStatus.value = _chatSession?.status;

    if (_chatSession) {
      messages.value = _chatSession.chats;
    }
    isLoading.value = false;
  }
});

const handleCreateChatSession = async () => {
  isLoading.value = true;
  const _chatSession = await createChatSession({
    name: userInfo.value.username,
  });
  chatSession.value = _chatSession;
  chatSessionStatus.value = _chatSession?.status;
  selectedChatSessionId.value = _chatSession?.id;

  messages.value = _chatSession?.chats;

  getChatSessionsList();
  isLoading.value = false;
};

const createMessage = async ({ messageText, optionId }) => {
  const res = await createChat({
    chat_session_id: selectedChatSessionId.value,
    message_text: messageText,
    option_id: optionId,
  });

  const _messages = [...(messages.value || []), res?.user, res?.bot];
  chatSessionStatus.value = res?.status;
  messages.value = _messages;
};

const submitMessage = async (e) => {
  e.preventDefault();
  const messageText = get(e, "target[0].value");
  await createMessage({ messageText });
  e.target[0].value = "";
};

const onSelectOption = async (option) => {
  if (option) {
    await createMessage({ messageText: option.label, optionId: option.id });

    if (messageInput.value) {
      messageInput.value.value = "";
    }
  }
};

onUpdated(() => {
  if (chatWindow.value) {
    const children = chatWindow.value.children;
    const lastChild =
      children && children.length ? children[children.length - 1] : null;

    if (lastChild) {
      scrollIntoView(lastChild, {
        behavior: isFirstLoad.value ? "auto" : "smooth",
        block: "end",
        scrollMode: "if-needed",
      });

      if (isFirstLoad.value) {
        isFirstLoad.value = false;
      }
    }
  }
});

// RESULTS
const results = ref(null);

watch(
  [selectedChatSessionId, chatSessionStatus],
  ([selectedChatSessionId, chatSessionStatus]) => {
    if (chatSessionStatus === "complete") {
      handleGenerateResults(selectedChatSessionId);
    } else {
      // Clear results
      results.value = null;
    }
  }
);

const handleGenerateResults = async () => {
  if (
    chatSessionStatus.value === "ready" ||
    chatSessionStatus.value === "complete"
  ) {
    isLoading.value = true;
    const res = await generateResults(selectedChatSessionId.value);
    results.value = res;
    isLoading.value = false;
    return res;
  } else {
    results.value = null;
    return null;
  }
};

const fetchResult = async (item) => {
  return await getOccupation(item.occupationId);
};
</script>

<style scoped>
:root {
  --body-bg: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  --msger-bg: #fff;
  --border: 2px solid #ddd;
  --left-msg-bg: #ececec;
  --right-msg-bg: #579ffb;
}

html {
  box-sizing: border-box;
}

*,
*:before,
*:after {
  margin: 0;
  padding: 0;
  box-sizing: inherit;
}

body {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.msger {
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 100%;
}

.msger-content {
  display: flex;
  position: relative;
  flex-flow: column;
  justify-content: space-between;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.msger-result-body {
  position: relative;
  width: 100%;
  height: calc(100% - 3rem);
}

.msger-body {
  display: flex;
  position: relative;
  flex-flow: column;
  justify-content: space-between;
  width: 100%;
  height: calc(100% - 3rem);
  border: var(--border);
  border-radius: 5px;
}

.msger-header {
  display: flex;
  flex-direction: row;
  font-size: medium;
  justify-content: space-between;
  padding: 10px;
  text-align: center;
  border-bottom: var(--border);
  height: 3rem;
  /* background: #eee; */
  color: #666;
}

.msger__chat-list-container {
  width: 0%;
  visibility: hidden;
  transition: width 200ms ease-in;
  box-shadow: 0 10px 10px 2px rgba(0, 0, 0, 0.2);
  overflow-x: hidden;
  position: absolute;
  z-index: 10;
}

.msger__chat-list-container.--open {
  visibility: visible;
  width: 100%;
  transition: width 200ms ease-in;
  top: 0;
  bottom: 0;
  left: 0;
}

.msger-toggle-side {
  display: inline-flex;
  width: 8rem;
  visibility: visible;
}

.msger-toggle-side-btn {
  padding: 0 0.5rem;
}

@media only screen and (min-width: 600px) {
  .msger__chat-list-container {
    visibility: visible;
    width: 400px;
    background-color: lightblue;
    transition: all 500ms ease-in;
    position: relative;
  }

  .msger-toggle-side {
    display: none;
  }
}

.msger-chat {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.msger-inputarea-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  position: relative;
}

.msger__load {
  display: block;
  width: 100%;
  height: 100%;
  position: absolute;
}

.msger-inputarea {
  display: flex;
  flex-direction: row;
  padding: 10px;
  width: 100%;
  border-top: var(--border);
}
.msger-inputarea * {
  padding: 10px;
  border: none;
  border-radius: 3px;
  font-size: 1em;
}
.msger-input {
  flex: 1;
  background: rgb(232, 228, 228, 0.4);
}
.msger-send-btn {
  margin-left: 0.75rem;
  font-weight: bold;
  height: 100%;
}

.msger-chat {
  background-color: #fcfcfe;
  /* background-image: url("@/assets/images/Job-Board-Header-Background.png"); */
}

.msger__success-btn {
  color: white;
  font-weight: bold;
  text-align: center;
  background-color: rgb(21, 197, 21);
  animation: pulse-green 2s infinite;
  border: none;
  cursor: pointer;
}

@keyframes pulse-green {
  0% {
    transform: scale(0.96);
    box-shadow: 0 0 0 0 rgba(21, 197, 21, 0.7);
  }

  70% {
    transform: scale(1);
    box-shadow: 0 0 0 10px rgba(21, 197, 21, 0);
  }

  100% {
    transform: scale(0.96);
    box-shadow: 0 0 0 0 rgba(21, 197, 21, 0);
  }
}
</style>
