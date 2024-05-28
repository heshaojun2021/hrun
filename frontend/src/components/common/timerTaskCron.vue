<template>
  <div style="display: inline-block">
    <div class="form">
      <el-row>
        <el-col :span="60">
          <el-radio-group v-model="type" size="large" style="margin-bottom: 20px">
            <el-radio-button label="每天" />
            <el-radio-button label="每周" />
            <el-radio-button label="每月" />
          </el-radio-group>
        </el-col>
        <el-col :span="8" style="margin-left: 20px">
          <el-time-picker
            v-model="time"
            placeholder="选择时间"
            size="large"
            style="width: 140px"
            value-format="H:m"
          ></el-time-picker>

        </el-col>
      </el-row>
      <el-row>

        <el-radio-group v-if="weekRadio" v-model="week">
          <template v-for="item in weekOption">
            <el-radio :label="item.cron">{{ item.value }}</el-radio>
          </template>
        </el-radio-group>

        <el-radio-group v-if="monthRadio" v-model="month" style="width: 640px">
          <template v-for="item in monthOption">
            <el-radio :label="item.cron">{{ item.value }}</el-radio>
          </template>
        </el-radio-group>
      </el-row>

      <div class="footer">
        <el-button size="mini" type="text" @click="closeCron">取消</el-button>
        <el-button size="mini" type="primary" @click="handleSummit"
          >确定</el-button
        >
      </div>
    </div>
  </div>
</template>
<script>
import { ref } from "vue";

export default {
  name: "timerTaskCron",
  props: {
    runTimeStr: ref(),
    timeCronStr: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      visible: false,
      weekRadio: false,
      monthRadio: false,
      value: "",
      type: "每天", // 天\周\月
      week: 1, // 星期几
      month: 1, // 几号
      time: "", // 时间
      weekOption: [
        {
          title: "星期一",
          value: "星期一",
          cron: 1,
        },
        {
          title: "星期二",
          value: "星期二",
          cron: 2,
        },
        {
          title: "星期三",
          value: "星期三",
          cron: 3,
        },
        {
          title: "星期四",
          value: "星期四",
          cron: 4,
        },
        {
          title: "星期五",
          value: "星期五",
          cron: 5,
        },
        {
          title: "星期六",
          value: "星期六",
          cron: 6,
        },
        {
          title: "星期日",
          value: "星期日",
          cron: 7,
        },
      ],
      monthOption: [],
    };
  },
  watch: {
    type(a, b) {
      if (this.type === "每天") {
        this.weekRadio = false;
        this.monthRadio = false;
      }
      if (this.type === "每周") {
        this.weekRadio = true;
        this.monthRadio = false;
      }
      if (this.type === "每月") {
        this.weekRadio = false;
        this.monthRadio = true;
      }
    },
    week(a, b) {},
    month(a, b) {},
  },
  created() {
    this.initData();
  },
  mounted() {},
  methods: {
    initData() {
      let arr = [];
      var hao = "";
      for (let i = 1; i < 32; i++) {
        hao = i < 10 ? "\xa0\xa0号" : "号";

        arr.push({
          title: i + hao,
          value: i + hao,
          cron: i,
        });
      }
      this.monthOption = arr;
    },

    closeCron() {
      this.$emit("closeTime", false);
      this.type = "每天";
      this.week = 1;
      this.month = 1;
      this.time = '';
    },
    handleSummit() {
      if (!this.time) {
        this.$message({
          message: "请选择时间!",
          type: "warning",
        });
        return;
      }
      let timeCron;
      let clockCornArr = this.time.split(":").reverse();
      if (this.type === "每天") {
        timeCron = clockCornArr.join(" ") + " * * *";
      }
      if (this.type === "每月") {
        timeCron = clockCornArr.join(" ") + " " + "* " + this.month + " *";
      }
      if (this.type === "每周") {
        // 每周
        timeCron = clockCornArr.join(" ") + " " + this.week + " * *";
      }
      // 每月,1号,14:52:36 和 36 52 14 1 * ?
      this.$emit("runTime", timeCron);
      this.$emit("closeTime", false);
      this.type = "每天";
      this.week = 1;
      this.month = 1;
      this.time = '';
    },
  },
};
</script>
<style scoped>
.form {
  padding: 12px;
}

.footer {
  text-align: right;
  margin-top: 10px;
}
.el-radio-group {
    display: inline-block;
    line-height: 35;
    vertical-align: middle;
    font-size: 1px;
}


</style>
