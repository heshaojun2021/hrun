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
        grid: {
          top: 50,
          bottom: 10,
          left: 20,
          right: 20,
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          formatter: params => {
            const dataIndex = params[0].dataIndex;
            const label = params[0].axisValueLabel;
            const value = params[0].value;
            return `${this.testData[dataIndex].plan_id__name} <br/>${label} <br/> 通过率：${value}%`;
          },
          axisPointer: {
            type: 'line',
            lineStyle: {
              color: '#95d475'
            }
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          axisLabel: {
            show: false
          },
          axisLine: {
            lineStyle: {
              color: 'rgb(251, 212, 55)',
              width: 5
            }
          },
          axisTick: {
            show: false
          },
          data: this.testData.map(item => item.create_time)
        },
        yAxis: {
          type: 'value',
          nameTextStyle: {
            color: '#fff',
            fontSize: 12,
            lineHeight: 40
          },
          splitLine: {
            lineStyle: {
              color: '#eef5f0'
            }
          },
          axisLine: {
            lineStyle: {
              // color: '#00aa7f'
            }
          },
          axisTick: {
            show: false
          }
        },
        series: [{
          name: '通过率',
          type: 'line',
          smooth: true,
          showSymbol: true,
          symbolSize: 8,
          zlevel: 3,
          itemStyle: {
            color: '#67C23A',
            borderColor: '#a3c8d8'
          },
          lineStyle: {
            width: 3,
            color: '#67C23A'
          },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(
              0,
              0,
              0,
              1,
              [{
                offset: 0,
                color: '#95d475'
              },
              {
                offset: 0.5,
                color: '#b3e19d'
              },
              {
                offset: 1,
                color: '#d1edc4'
              }
              ],
              false
            )
          },
          data: this.testData.map(item => parseFloat(item.pass_rate))
        }]
      };
      chart.setOption(option);
    }
  }
};
</script>

<style scoped>
/* 样式可以根据需要自行调整 */
</style>
