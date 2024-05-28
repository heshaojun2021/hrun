<template>
  <div>
    <div ref="chart" style=" height: 400px"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts/core';
import { TitleComponent, LegendComponent } from 'echarts/components';
import { RadarChart } from 'echarts/charts';
import { CanvasRenderer } from 'echarts/renderers';

echarts.use([TitleComponent, LegendComponent, RadarChart, CanvasRenderer]);

// 获取当前日期时间
var today = new Date();

// 定义一个数组用于存储日期数据
var dateArray = [];

// 循环获取近七天的日期
for(var i = 6; i >= 0; i--) {
  var day = new Date(today);
  day.setDate(today.getDate() - i);
  var month = day.getMonth() + 1;
  var date = day.getDate();

  // 格式化日期为 "月-日" 的格式
  var formattedDate = month + '-' + date;

  // 将格式化后的日期添加到数组中
  dateArray.push(formattedDate);
}
export default {
  data() {
    return {
      chartData: null,
    };
  },
  mounted() {
    this.renderChart();
  },
  methods: {
    renderChart() {
      const chartDom = this.$refs.chart;
      const myChart = echarts.init(chartDom);

      const option = {
        xAxis: {
          type: 'category',
          data: dateArray,
          axisTick: { // 隐藏 x 轴刻度线和刻度标签
            show: false
          },
          axisLine: { // 隐藏 x 轴轴线
            show: false
          }
        },
        tooltip: {
          position: 'top', // 将提示框显示在上方
          trigger: 'axis', // 设置触发类型为坐标轴轴触发
          axisPointer: { type: 'none' },// 显示阴影
          formatter: function(params) { // 自定义提示框内容
            const value = params[0].value; // 获取当前点击柱形图的值
            return '用例数：' + value; // 返回数量信息
          }},
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: [120, 200, 150, 80, 315, 110, 130],
            type: 'bar'
          }
        ]
      };

      option && myChart.setOption(option);
    },
  },
};
</script>
