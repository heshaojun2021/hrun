<template>
  <div ref="chart" style="height: 400px;"></div>
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
    };
  },
  mounted() {
    this.initChart();
  },
  updated() {
    this.initChart();
  },
  methods: {
    initChart() {
      const chart = echarts.init(this.$refs.chart);
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{d}%【{c}条】',
        },
        legend: {
          orient: 'vertical',
          left: '75%', // 居左
          top: '35%', // 居中
        },
        series: [
          {
            name: 'Access From',
            type: 'pie',
            center: ['40%', '50%'],
            radius: ['50%', '60%'],
            avoidLabelOverlap: false,
            padAngle: 5,
            itemStyle: {
              borderRadius: 10
            },
            label: {
              show: false,
              position: 'center'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: 20,
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: false
            },
            data: this.testData // 使用数据
          }
        ]
      };
      chart.setOption(option);
    }
  }
};
</script>

<style>
</style>
