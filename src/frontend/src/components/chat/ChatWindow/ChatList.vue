<template>
  <div class="chatlist__container">
    <div class="chatlist__head">
      <div class="chatlist__head-title">History</div>
      <div class="chatlist__head-btns">
        <Button
          type="ghost"
          color="primary"
          html-type="button"
          class="new-session-btn"
          @click="() => $emit('createChatSession')"
          >New</Button
        >

        <Button
          type="text"
          html-type="button"
          class="close-btn"
          @click="() => $emit('close')"
        >
          <CloseOutlined
        /></Button>
      </div>
    </div>
    <div class="chatlist__body">
      <div
        v-if="chatSessions && chatSessions.length"
        class="chatlist__body-content"
      >
        <button
          type="button"
          v-for="chatSession in chatSessions"
          :key="chatSession.id"
          class="chatlist__item"
          @click="selectItem(chatSession)"
        >
          <div class="chatlist__item-content">
            <div class="chatlist__item-title">{{ chatSession.name }}</div>
            <div class="chatlist__item-date">
              updated {{ displayTime(chatSession.updatedAt) }}
            </div>
          </div>

          <hr />
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { Button } from "ant-design-vue";
import { CloseOutlined } from "@ant-design/icons-vue";

import { displayTime } from "@/plugins/display";

export default {
  components: { Button, CloseOutlined },
  props: {
    chatSessions: {
      type: Array,
    },
    createChatSession: {
      type: Function,
      default: () => {
        return () => {};
      },
    },
  },
  setup(props, { emit }) {
    const selectItem = (item) => {
      emit("selectItem", item);
    };
    return {
      selectItem,
      displayTime,
    };
  },
};
</script>

<style scoped>
.chatlist__container {
  display: block;
  width: 100%;
  height: 100%;
  background: white;
}

.chatlist__head {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
  height: 3rem;
  padding: 0.5rem 0.5rem;
  font-weight: bold;
}

.chatlist__head-btns {
  display: flex;
  flex-direction: row;
}

.chatlist__head-title {
  width: 100%;
  padding: 0.25rem;
}

.new-session-btn {
  padding-left: 1rem;
  padding-right: 1rem;
}
.chatlist__body {
  width: 100%;
}

.chatlist__body-content {
  width: 100%;
}

.chatlist__item {
  width: 100%;
  background-color: inherit;
  text-align: left;
  border: none;
  margin: 0;
}

hr {
  margin: 0;
}

.chatlist__item:hover {
  background-color: rgba(207, 77, 254, 0.3);
  transition: background-color 300ms ease-in;
}

.chatlist__item-content {
  width: 100%;
  padding: 0.5rem 0.5rem;
}

.chatlist__item-title {
  width: 100%;
  display: flex;
  font-weight: bold;
}
.chatlist__item-date {
  width: 100%;
  font-size: 70%;
  font-weight: light;
}

@media only screen and (min-width: 600px) {
  .close-btn {
    display: none;
  }
}
</style>
