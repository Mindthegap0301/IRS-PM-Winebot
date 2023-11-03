<template>
  <canvas ref="container"></canvas>
</template>

<script setup>
import { ref, defineProps, onMounted, onUnmounted } from "vue";
import { Chart } from "chart.js";

import { getGradient, getMinTick, getMaxTick } from "@/plugins/occupation.js";

const props = defineProps({
  data: {
    type: Array,
    default: () => {
      return null;
    },
  },
});

const container = ref(null);

const chartInstance = ref(null);

onMounted(() => {
  if (props.data && props.data.length && container.value) {
    const yKey = "grossMonthlyMedian";
    const xKey = "year";

    const processedData = props.data
      .filter((item) => item[yKey])
      .sort((item1, item2) => item1[xKey] - item2[xKey])
      .map((item) => {
        return {
          x: item[xKey],
          y: item[yKey],
        };
      });

    if (processedData && processedData.length) {
      const dataY = processedData.map((item) => {
        return item.y;
      });

      const dataX = processedData.map((item) => {
        return item.x;
      });
      const minMaxY = [Math.min(...dataY), Math.max(...dataY)];
      const minMaxX = [Math.min(...dataX), Math.max(...dataX)];

      const datasets = [
        {
          label: "Median monthly salary",
          data: processedData,
          borderColor: function (context) {
            const chart = context.chart;
            const { ctx, chartArea } = chart;

            if (!chartArea) {
              return;
            }
            return getGradient(ctx, chartArea);
          },
        },
      ];

      chartInstance.value = new Chart(container.value, {
        type: "line",
        data: {
          labels: dataX,
          datasets,
        },
        options: {
          layout: {
            autoPadding: true,
          },
          plugins: {
            legend: {
              display: false,
              labels: {
                usePointStyle: false,
              },
            },
          },
          scales: {
            x: {
              grid: {
                display: false,
              },
              border: {
                display: false,
              },
              ticks: {
                major: {
                  enabled: false,
                },
                backdropPadding: {
                  x: 10,
                  y: 10,
                },
                callback(_, index, values) {
                  return index === 0
                    ? minMaxX[0]
                    : index === values.length - 1
                    ? minMaxX[1]
                    : null;
                },
              },
            },
            y: {
              grid: {
                display: false,
              },
              border: {
                display: false,
              },
              min: getMinTick(minMaxY[0]),
              max: getMaxTick(minMaxY[1]),
              ticks: {
                major: {
                  enabled: true,
                },
                maxTicksLimit: 2,
                backdropPadding: {
                  x: 10,
                  y: 10,
                },
                callback(value) {
                  return "$" + value.toLocaleString();
                },
              },
            },
          },
        },
      });
    }
  }
});

onUnmounted(() => {
  if (chartInstance.value) {
    chartInstance.value.destroy();
  }
});
</script>
