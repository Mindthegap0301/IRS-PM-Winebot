<template>
  <div>
    <canvas ref="sankeyDiagram"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, defineProps, onUnmounted } from "vue";

import { Chart, registerables } from "chart.js";
import { SankeyController, Flow } from "chartjs-chart-sankey";
import { careerPathsToSankey } from "@/plugins/occupation";

Chart.register(SankeyController, Flow, ...registerables);

const props = defineProps({
  currentItem: {
    type: Object,
    default: () => {
      return null;
    },
  },
});

const sankeyDiagram = ref(null);
const chartInstance = ref(null);

const buildData = (data) => {
  return careerPathsToSankey(data);
};

onMounted(() => {
  if (sankeyDiagram.value) {
    const configs = buildData(props.currentItem?.careerPaths);

    chartInstance.value = new Chart(sankeyDiagram.value, {
      type: "sankey",
      ...configs,
    });
  }
});

onUnmounted(() => {
  if (chartInstance.value) {
    chartInstance.value.destroy();
  }
});
</script>
