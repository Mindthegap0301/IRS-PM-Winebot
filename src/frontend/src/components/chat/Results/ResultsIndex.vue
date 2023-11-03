<template>
  <div class="results__container">
    <div class="results__head">
      <div class="results__head-title">Wine</div>
    </div>
    <div class="results__body">
      <div v-if="results && results.length" class="results__body-content">
        <div
          v-for="result in results"
          :key="result.id"
          class="results__item"
          @click="selectItem(result)"
        >
          <div class="results__item-content">
            <div class="results__item-title">
              {{ result.products.product_name }}
            </div>
            <div class="results__item-code">
              O*Net SOC {{ result.products.id }}
            </div>
            <div class="results__item-description">
              {{ result.products.product_desc }}

              <div class="results__item-fade"></div>
            </div>

            <Button htmlType="button" type="primary"> More </Button>
          </div>

          <hr />
        </div>
      </div>
    </div>
    <transition>
      <div class="results__result-container" v-if="result">
        <ResultDetail :product="result" @close="closeResult"></ResultDetail>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from "vue";
import { Button } from "ant-design-vue";
import ResultDetail from "./ResultDetail";

const props = defineProps({
  fetchResult: {
    type: Function,
    default: () => {
      return () => {};
    },
  },
  chatSessionId: {
    type: String,
  },
  results: {
    type: Array,
    default: () => {
      return [];
    },
  },
});

const result = ref(null);

const emit = defineEmits(["close", "selectItem"]);

const selectItem = async (item) => {
  result.value = await props.fetchResult(item);
  emit("selectItem", item);
};

const closeResult = () => {
  result.value = null;
};
</script>

<style scoped>
.results__container {
  position: relative;
  width: 100%;
  height: 100%;
  background: white;
}

.results__head {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
  height: 3rem;
  padding: 0.5rem 0.5rem;
  font-weight: bold;
}

.results__head-btns {
  display: flex;
  flex-direction: row;
}

.results__head-title {
  width: 100%;
  padding: 0.25rem;
}

.new-session-btn {
  padding-left: 1rem;
  padding-right: 1rem;
}
.results__body {
  position: relative;
  width: 100%;
  height: calc(100% - 3rem);
}

.results__body-content {
  position: relative;
  overflow-y: auto;
  width: 100%;
  height: 100%;
}

.results__item {
  width: 100%;
  background-color: inherit;
  text-align: left;
  border: none;
  margin: 0;
}

hr {
  margin: 0;
}

.results__item-content {
  width: 100%;
  padding: 0.5rem 2rem;
}

.results__item-title {
  width: 100%;
  display: flex;
  font-weight: bold;
}
.results__item-code {
  width: 100%;
  font-size: 70%;
  font-weight: light;
}

.results__item-description {
  width: 100%;
  font-size: 80%;
  height: 5rem;
  position: relative;
  padding: 0.25rem 0;
  overflow: hidden;
}

.results__item-fade {
  width: 100%;
  height: 2rem;
  bottom: 0;
  left: 0;
  position: absolute;
  background-image: -webkit-gradient(
    linear,
    left top,
    left bottom,
    from(rgba(255, 255, 255, 0)),
    to(rgba(255, 255, 255, 1))
  );
}

.results__result-container {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
}

@media only screen and (min-width: 600px) {
  .close-btn {
    display: none;
  }
}
</style>
