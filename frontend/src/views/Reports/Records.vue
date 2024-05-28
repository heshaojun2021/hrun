<template>
		<div class="chartBox2" ref="chart_box"></div>
    <div class="query_model" >
    <span class="spacer">生成时间
      <el-date-picker
        v-model="dataTime"
        type="datetimerange"
        start-placeholder="开始时间"
        end-placeholder="结束时间"
        value-format="YYYY-MM-DD HH:mm:ss"
        :default-time="defaultTimeOptions"
        :shortcuts="shortcuts"
        range-separator="至"
        :clearable="false"
        style="width: 340px"
      />
    </span>
    <span >
      <el-button @click="clearData"  icon="el-icon-refresh">重置</el-button>
      <el-button type="primary" @click="submitForm"  icon="el-icon-search"> 查询</el-button>
    </span>
    </div>
		<el-table :data="records"  v-loading="isLoading" class="table-style" size="mini" height="calc(100vh - 425px)" empty-text="暂无数据">
      <el-table-column label="序号" align="center" width="60">
        <template #default="scope">
          <span>{{ scope.$index + 1 }}</span>
        </template>
      </el-table-column>
			<el-table-column prop="create_time" label="执行时间" min-width="140" width="150" align="center">
				<template #default="scope">
					{{ $tools.rTime(scope.row.create_time) }}
				</template>
			</el-table-column>
			<el-table-column prop="tester" label="执行人" min-width="110" align="center"></el-table-column>
			<el-table-column prop="env_name" label="执行环境" min-width="110" align="center"></el-table-column>
      <el-table-column prop="execute_type" label="执行类型" align="center">
        <template #default="scope">
					<span v-if="scope.row.execute_type === '手动执行'">
						<el-tag effect="dark">{{ scope.row.execute_type }}</el-tag>
					</span>
          <span v-if="scope.row.execute_type === '定时执行'">
            <el-tag color="rgb(201, 233, 104)" >{{ scope.row.execute_type}}</el-tag>
					</span>
					<span v-if="scope.row.execute_type ===null">
            <el-tag effect="dark" type="warning">暂无类型</el-tag>
          </span>
				</template>
      </el-table-column>
			<el-table-column prop="plan_name" label="测试计划" min-width="110" align="center"></el-table-column>
			<el-table-column prop="all" label="总用例" min-width="50" align="center">
				<template #default="scope">
					<span v-if="scope.row.status !== '执行中'">{{ scope.row.all }}</span>
				</template>
			</el-table-column>

			<el-table-column label="通过数" min-width="50" align="center">
				<template #default="scope">
					<span v-if="scope.row.status !== '执行中'">{{ scope.row.success }}</span>
				</template>
			</el-table-column>
			<el-table-column label="通过率" min-width="80" align="center">
				<template #default="scope">
					<span v-if="scope.row.status !== '执行中'">{{ scope.row.pass_rate + '%' }}</span>
				</template>
			</el-table-column>
			<el-table-column label="测试报告" width="140" align="center">
				<template #default="scope">
					<span v-if="scope.row.status === '执行中'">
            <el-tag  effect="dark" color="#61affe" style="width: 100px"> {{ scope.row.status}}</el-tag>
					</span>
					<el-button v-else type="success" icon="el-icon-view" plain size="mini" @click="$router.push({ name: 'report', params: { id: scope.row.id } })">
						测试报告
					</el-button>
				</template>
			</el-table-column>
		</el-table>
</template>
<script>
import { mapState } from 'vuex';

const moment = require('moment-timezone');
function convertToTimeZoneFormat(dateStr, timeZone) {
    const m = moment.tz(dateStr, timeZone);
    return m.format('YYYY-MM-DD HH:mm:ss'); // 格式化为年月日时分秒
}

function getFormattedDate(date, endOfDay = false) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  let hours, minutes, seconds;

  if (endOfDay) {
    hours = '23';
    minutes = '59';
    seconds = '59';
  } else {
    hours = '00';
    minutes = '00';
    seconds = '00';
  }

  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

export default {
	data() {
		return {
		  isLoading: false,
			records: [],
      dataTime: [getFormattedDate(new Date(new Date().getTime() - 2 * 24 * 60 * 60 * 1000)),
                  getFormattedDate(new Date(), true)],
      defaultTimeOptions: ['0000-01-01 00:00:00', '0000-01-01 23:59:59'], // 设置默认时间数组
      shortcuts: [
        {
          text: '今天',
          value: (() => {
            const end = new Date();
            const start = new Date();
            start.setHours(0, 0, 0);
            end.setHours(23, 59, 59);
            return [start, end];
          })
        },
        {
          text: '近三天',
          value: (() => {
            const end = new Date();
            const start = new Date();
            start.setDate(end.getDate() - 2);
            start.setHours(0, 0, 0);
            end.setHours(23, 59, 59);
            return [start, end];
          })
        },
        {
          text: '近七天',
          value: (() => {
            const end = new Date();
            const start = new Date();
            start.setDate(end.getDate() - 6);
            start.setHours(0, 0, 0);
            end.setHours(23, 59, 59);
            return [start, end];
          })
        },
       {
          text: '近一个月',
          value: (() => {
            const end = new Date();
            const start = new Date();
            start.setMonth(end.getMonth() - 1);
            start.setHours(0, 0, 0); // 设置时分秒为 00:00:00
            end.setHours(23, 59, 59); // 设置时分秒为 23:59:59
            return [start, end];
          })
        }],

		};
	},


	methods: {

    submitForm(){
    this.getAllRecord()
    },

    clearData() {
      console.log(this.dataTime)
      this.dataTime = [getFormattedDate(new Date(new Date().getTime() - 2 * 24 * 60 * 60 * 1000)),
                      getFormattedDate(new Date(), true)]

    },

		async getAllRecord() {
		  this.isLoading=true
      const startDate = convertToTimeZoneFormat(this.dataTime[0],'Asia/Shanghai');
      const endDate = convertToTimeZoneFormat(this.dataTime[1],'Asia/Shanghai');
      console.log(startDate,endDate)
			const response = await this.$api.getTestRecord({ project: this.pro.id,start_time:startDate,end_time:endDate});
			// 判断http状态码
			if (response.status == 200) {
				this.records = response.data;
				this.chartView();
				this.isLoading=false
			}
		},
		// 通过率图表
		chartView() {
			this.$chart.chart3(this.$refs.chart_box, this.pateData.value, this.pateData.label);
		}
	},
	computed: {
		...mapState(['pro']),
		//执行记录图表展示数据
		pateData: function() {
			let run_date = [];
			let pass_rate = [];
			for (let item of this.records) {
				run_date.push(this.$tools.rTime(item.create_time));
				pass_rate.push(item.pass_rate);
			}
			return {
				label: run_date,
				value: pass_rate
			};
		}
	},
	created() {
		this.getAllRecord();
	}
};
</script>

<style scoped>

.query_model {
  height: 50px;
  padding: 20px;
  margin:10px;
  border-radius: 10px;
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.2);
}


.spacer + span {
        margin-left: 10px;
        padding-left: 5px;
    }
/*.buttons {*/
/*  margin-left: 100px;*/
/*  float:right;*/
/*}*/
.pro_title {
	height: 50px;
	color: #00aa7f;
	text-align: center;
	font: bold 24px/50px 'microsoft yahei';
	background: #f7f7f7;
}
.title {
	font-weight: bold;
	line-height: 40px;
	color: #545454;
}
/* 第一行图表样式 */
.chartBox1 {
	height: 220px;
	background: rgba(198, 198, 202, 0.1);
	margin-bottom: 10px;
}
.chartBox2 {
	height: 260px;
	background: rgba(198, 198, 202, 0.1);
}

/* 信息图样式 */
.info {
	margin: 5px;
	padding: 10px;
	text-align: center;
	background: #f8f8f8;
}

.percentage-value {
	display: block;
	margin-top: 10px;
	font-size: 16px;
}
.percentage-label {
	display: block;
	margin-top: 10px;
	font-size: 12px;
}
.element.style {
    height: 265px;
}
.el-tag {
  color: #ffffff;
}
.el-tag--small {
    height: 28px;
    padding: 0 8px;
    line-height: 26px;
}
</style>
