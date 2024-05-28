<template>
  <el-scrollbar height="calc(100vh - 50px)">
  <div class="box">
    <el-row :gutter="9" style="margin-bottom: 15px">
      <el-col  v-for="(item, index) in proInfo" :key="index" :span="3">
        <el-card shadow="hover">
        <div class="projectinfo_cs">{{item.name}}</div>
              <countTo
                  style="font-size:30px; text-align:right;"
                  :start-val="0"
                  :end-val="item.count"
                  :duration="2600">
              </countTo>
        <div v-if="item.changeType==='lastIncrease'" class="projectinfo">自上周增长<i class="el-icon-top" style="color:#13ce66;margin-left: 5px;font-size: 14px">{{item.percentage}}</i></div>
        <div v-if="item.changeType==='lastDecrease'" class="projectinfo">自上周下降<i class="el-icon-bottom" style="color:#ff4d4f;margin-left: 5px;font-size: 14px">{{item.percentage}}</i></div>
        <div v-if="item.changeType==='yastdayIncrease'" class="projectinfo">自昨日增长<i class="el-icon-top" style="color:#13ce66;margin-left: 5px;font-size: 14px">{{item.percentage}}</i></div>
        <div v-if="item.changeType==='yastdayDecrease'" class="projectinfo">自昨日下降<i class="el-icon-bottom" style="color:#ff4d4f;margin-left: 5px;font-size: 14px">{{item.percentage}}</i></div>
        <div v-if="item.changeType==='job'" style="display: flex; justify-content: space-between; font-size: 14px; margin-top: 20px;">
            <span>运行中：{{item.run_service}}</span>
            <span style="color:#ff4d4f;">已暂停：{{item.paused}}</span>
        </div>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="15" style="margin-bottom: 15px">
        <el-col :span="9" v-if="proCase && proCase.length > 0">
          <el-card shadow="hover">
            <template #header>
              <div style="display: flex; justify-content: space-between; align-items: center; margin: 5px">
                <div>
                  <strong><span style="">接口维护情况统计</span></strong>
                  <i class="el-icon-suitcase" style="margin-left: 5px;"></i>
                </div>
                <div style="display: flex; align-items: center;">
                  <el-date-picker
                    v-model="dataTime"
                    type="datetimerange"
                    start-placeholder="开始时间"
                    end-placeholder="结束时间"
                    value-format="YYYY-MM-DD HH:mm:ss"
                    :default-time="defaultTimeOptions"
                    :shortcuts="shortcuts"
                    range-separator="至"
                    :clearable="true"
                    style="width: 340px; margin-left: auto;"
                  />
                  <el-button type="primary" @click="submitForm" icon="el-icon-search" style="margin-left: 10px;">查询</el-button>
                </div>
              </div>
            </template>
            <ApiChart :testData="proCase"></ApiChart>
          </el-card>
        </el-col>
        <el-col :span="8" v-if="buttonClick && buttonClick.length > 0">
          <el-card shadow="hover">
            <template #header>
              <div style="display: flex; justify-content: space-between; align-items: center; margin: 5px;margin-bottom: 15px">
                <div>
                  <strong><span style="">近七日平台使用频率</span></strong>
                  <i class="el-icon-s-data" style="margin-left: 5px;"></i>
                </div>
              </div>
            </template>
            <WeekLoginChart :testData="buttonClick"></WeekLoginChart>
          </el-card>
        </el-col>
        <el-col :span="7" v-if="proBug && proBug.length > 0">
          <el-card shadow="hover">
            <template #header>
              <div style="display: flex; justify-content: space-between; align-items: center; margin: 5px;margin-bottom: 15px">
                <div>
                  <strong><span style="">bug处理情况</span></strong>
                  <i class="el-icon-pie-chart" style="margin-left: 5px;"></i>
                </div>
              </div>
            </template>
            <BugChart :testData="proBug"></BugChart>
          </el-card>
        </el-col>
    </el-row>
    <el-row :gutter="15">
        <el-col :span="9" v-if="mockLog && mockLog.length > 0">
          <el-card shadow="hover">
            <template #header>
              <div style="display: flex; justify-content: space-between; align-items: center; margin: 5px">
                <div>
                  <strong><span style="">Mock日志</span></strong>
                  <i class="el-icon-tickets" style="margin-left: 5px;"></i>
                </div>
              </div>
            </template>
          <div>
            <el-timeline>
              <el-timeline-item v-for="(activity, index) in mockLog"
                                :key="index"
                                :timestamp="$tools.rTime(activity.create_time)"
                                placement="top"
                                color="#0bbd87">
              <span>
                <el-tag v-if="activity.method==='GET'" type="success">{{activity.method}}</el-tag>
                <el-tag v-else >{{activity.method}}</el-tag>
                <span class="grey-text">{{activity.url}}</span>
                <span style="font-weight: bold;">调用IP：</span>
                <span class="grey-text1">{{activity.ip}}</span>
                <span style="font-weight: bold">HTTP状态码：</span>
                <span v-if="activity.status_code==='200'" class="grey-text1" style="color:#67c23a;">{{activity.status_code}}</span>
                <span v-if="activity.status_code==='400'" class="grey-text1" style="color:#e6a23c;">{{activity.status_code}}</span>
                <span v-if="activity.status_code==='500'" class="grey-text1" style="color:#f56c6c">{{activity.status_code}}</span>
                <span class="grey-text">{{activity.time_consuming}}</span>
              </span>

              </el-timeline-item>
            </el-timeline>
          </div>
          </el-card>
        </el-col>
        <el-col :span="15" v-if="proReport && proReport.length > 0">
          <el-card shadow="hover">
            <template #header>
              <div style="display: flex; justify-content: space-between; align-items: center; margin: 5px">
                <div>
                  <strong><span >近三天报告运行情况统计</span></strong>
                  <i class="el-icon-s-data" style="margin-left: 5px;"></i>
                </div>
                <strong><span style="font-size: 14px; color: grey;">通过率(%)</span></strong>
              </div>
            </template>
            <ReportChart :testData="proReport"></ReportChart>
          </el-card>
        </el-col>
    </el-row>
  </div>
  </el-scrollbar>
</template>

<script >
import { ElCard, ElRow, ElCol} from 'element-plus';
import ApiChart from '../../components/echart/ApiChart.vue'
import WeekLoginChart from '../../components/echart/WeekLoginChart.vue'
import BugChart from '../../components/echart/BugChart.vue'
import ReportChart from '../../components/echart/ReportChart.vue'
import {mapMutations, mapState} from 'vuex';
import countTo from '../../components/to'
export default {
  components: {
    ElCard, ElRow, ElCol,
    ApiChart, countTo,WeekLoginChart,
    BugChart,ReportChart
  },
  data() {
    return {
      proall: null,
      proInfo: null,
      proBug:null,
      proCase:null,
      proReport:null,
      buttonClick:null,
      mockLog:null,
      defaultTimeOptions: ['0000-01-01 00:00:00', '0000-01-01 23:59:59'], // 设置默认时间数组
      dataTime: [],
    };
  },
 	methods: {
		...mapMutations(['selectPro']),
    async getProInfo(starttime, endtime) {
		  let data = {"project": this.pro.id};
		  if(starttime && endtime){
		      data = {"project": this.pro.id,"starttime": starttime, "endtime": endtime}};
			const response = await this.$api.getProjectBoard(data);
			if (response.status === 200) {
				this.proall = response.data;
				this.proInfo = this.proall.project_info;
				this.proBug = this.proall.project_bug;
				this.proCase = this.proall.project_case;
				this.proReport = this.proall.project_report;
				this.buttonClick = this.proall.track_button_click;
				this.mockLog = this.proall.mock_log;
			}
		},
    submitForm() {
		  if (!this.dataTime){
		  this.dataTime = []}
		  const starttime = this.dataTime[0]
      const endtime = this.dataTime[1]
		  this.getProInfo(starttime, endtime)
    },

	},
	computed: {
		...mapState(['pro']),
	},
	created() {
		this.getProInfo();
	}
};
</script>

<style scoped>
.box{
  padding:10px;
  background:#f6f8f9
}
.el-row {
cursor: pointer;
}
.el-card {
    --el-card-border-color: var(--el-border-color-light, #ebeef5);
    --el-card-border-radius: 4px;
    --el-card-padding: 10px;
    border-radius: 12px;
    border: 1px solid var(--el-card-border-color);
    background-color: #fff;
    overflow: hidden;
    color: var(--el-text-color-primary);
    -webkit-transition: var(--el-transition-duration);
    transition: var(--el-transition-duration);
}

.projectinfo{
  --un-text-opacity: 1;
  color: rgb(156 163 175 / var(--un-text-opacity));
  font-size: 14px;
  margin-top: 20px;

}

.projectinfo_cs{
  font-size: 15px;
  margin-bottom: 15px;
}

.grey-text {
  color: grey;
  margin: 5px;
}
.grey-text1 {
  color: grey;
  margin-right: 5px;
}


</style>
