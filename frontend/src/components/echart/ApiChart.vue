<template>
  <div ref="echarts" style="height: 400px;"></div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  props: {
    testData: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      option: {
        color: ['#409eff', '#67c23a', '#e6a23c'],
        legend: { x: 'center', y: 'bottom' },
        tooltip: {},
        dataset: {
          dimensions: ['product', '接口调试', '新增接口', '新增用例'],
          source: [] // 使用 testData 设置数据
        },
        xAxis: { type: 'category' },
        yAxis: { max: null },
        series: [{ type: 'bar' }, { type: 'bar' }, { type: 'bar' }]
      }
    };
  },
  mounted() {
    this.renderChart();
  },
  updated() {
    this.renderChart();
  },
  methods: {
    renderChart() {
      // 设置数据
      this.option.dataset.source = this.testData.map(item => [
        item.user,
        item.interface_debug_count,
        item.interface_new_count,
        item.testcase_new_count
      ]);

      const chartDom = this.$refs.echarts;
      const myChart = echarts.init(chartDom);
      myChart.setOption(this.option);
    }
  }
};
</script>

<style scoped>
/* 可以添加样式 */
</style>
