<template>
  <div>
    <div>
      <em>{{ `${item.university}  | ${item.school}` }}</em>
    </div>
    <div style="margin: 1rem 0">
      <div v-if="latestTrend.grossMonthlyMedian">
        Fresh graduates get a monthly salary of
        <span
          ><strong style="font-size: 120%"
            >${{ latestTrend.grossMonthlyMedian.toLocaleString() }} ({{
              latestTrend.year
            }})</strong
          ></span
        >
      </div>
      <div v-if="latestTrend.employmentRateFtPerm">
        <div></div>
        <span
          ><strong style="font-size: 120%"
            >{{ latestTrend.employmentRateFtPerm }}%</strong
          >
          are hired full-time</span
        >
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, defineProps } from "vue";

const props = defineProps({
  item: { type: Object },
});

const latestTrend = computed(() =>
  props.item?.programTrends?.length
    ? props.item?.programTrends[props.item?.programTrends?.length - 1]
    : null
);
</script>
