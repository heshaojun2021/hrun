<script>
import { ref, onMounted } from 'vue';
const { num = 0, duration = 2 } = defineProps<{
  num: number;
  duration: number;
}>();

let current = ref('0');

function numberGrow() {
  let step = parseInt((num * 100) / (duration * 1000) + '');
  let start = 0;
  let timer = setInterval(() => {
    start += step;
    if (start > num) {
      clearInterval(timer);
      start = num;
      timer = null;
    }
    if (start === 0) {
      start = num;
      clearInterval(timer);
    }
    current.value = start.toString().replace(/(\d)(?=(\d{3})+$)/g, '$1,');
  }, duration * 100);
}

onMounted(() => {
  numberGrow();
})
</script>

<template>
  <div style="font-size:20px; text-align:right;">{{ current }}</div>
</template>