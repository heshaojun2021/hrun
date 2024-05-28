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
      chart: null,
      option: {
        xAxis: {
          type: 'category',
          boundaryGap: false,
          axisLine: {
            lineStyle: {
              color: 'rgb(103, 77, 204)', // 修改轴线颜色
              width: 5
            }
          },
          axisTick: {
            show: false,
          },
          axisLabel: {
            color: 'black',
            margin: 15 // 调整标签文字位置
          },
          splitLine: {
            show: false,
          },
          data: [] // 设置 x 轴数据
        },
        yAxis: {
          type: 'value',
          boundaryGap: [0, '30%'],
          axisLine: {
            lineStyle: {
              color: 'rgb(103, 77, 204)', // 修改轴线颜色
              width: 5
            }
          },
          axisLabel: {
            color: 'black'
          },
          splitLine: {
            show: false,
          }
        },
        visualMap: {
          type: 'piecewise',
          show: false,
          dimension: 0,
          seriesIndex: 0,
          pieces: [
            {
              gt: 0,
              lt: 7,
              color: '#66b1ff'
            }
          ]
        },
        series: [
          {
            type: 'line',
            smooth: 0.6,
            symbol: 'none',
            lineStyle: {
              color: '#0d84ff',
              width: 5
            },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(
                0,
                0,
                0,
                1,
                [{
                  offset: 0,
                  color: '#79bbff'
                },
                {
                  offset: 0.5,
                  color: '#a0cfff'
                },
                {
                  offset: 1,
                  color: '#c6e2ff'
                }
                ],
                false
              )
            },
            data: [] // 设置 y 轴数据
          }
        ]
      }
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
      this.chart = echarts.init(this.$refs.chart);
      // 设置 x 轴数据
      this.option.xAxis.data = this.testData.map(item => item.date);
      // 设置 y 轴数据
      this.option.series[0].data = this.testData.map(item => item.clicks);
      this.chart.setOption(this.option);
    }
  }
};
</script>

<style scoped>
</style>
