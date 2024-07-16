<template>
  <el-scrollbar height="calc(100vh);padding-right:10px;">
  <div style="margin: 15px">
    <div style="display: flex; justify-content: space-between;margin-bottom: 15px">
      <b style="color: #101828CC; font-size: 15px">请求信息</b>
      <span style="color: #606266; font-size: 14px; display: flex; align-items: center;">开启/禁用Mock
        <el-switch
          v-model="mockData.statussCode"
          inline-prompt
          size="small"
          @click="switchClick(data)"
          style="--el-switch-on-color: #53a8ff; margin-left: 10px"
        />
      </span>
    </div>
    <el-alert style="margin-bottom: 10px" class="el-icon-circle-check" :title="mockTitle" type="success" />
    <el-form :rules="rulesInterface" ref="interfaceRef" :model="mockData">
      <el-row :gutter="24" >
        <el-col :span="18">
          <el-form-item prop="url">
              <el-input v-model="mockData.url" placeholder="请输入接口地址" style="font-size: 14px;">
                <template #prepend >
                    <el-select v-model="mockData.method" placeholder="请求类型" size="small" style="width: 100px;color: black">
                    <el-option label="GET" value="GET" style="color: rgba(204,73,145,0.87)"/>
                    <el-option label="POST" value="POST" style="color: #61affe"/>
                    <el-option label="PUT" value="PUT" style="color: #fca130"/>
                    <el-option label="PATCH" value="PATCH" style="color: #50e3c2"/>
                    <el-option label="DELETE" value="DELETE" style="color: #f93e3e"/>
                    <el-option label="HEAD" value="HEAD" style="color: rgb(201, 233, 104)"/>
                  </el-select>
                </template>
              </el-input>
            </el-form-item>
            </el-col>
        <el-col :span="6" style="text-align: right;">
          <el-button @click="runCase" type="success" icon="el-icon-s-promotion" :disabled="!mockData.statussCode">调试</el-button>
          <el-button @click="addClick" type="primary" icon="el-icon-edit-outline" :disabled="!mockData.statussCode">保存</el-button>
        </el-col>
    </el-row>
    </el-form>
    <div><b style="color: #101828CC; font-size: 15px">Mock 期望</b></div>
    <div style="margin-top: 15px">
      <el-table :data="mockDatas"  stripe empty-text="暂无数据" border>
        <el-table-column label="名称" width="180" prop="name"  align="center" />
        <el-table-column label="条件" prop="condition" align="center"/>
        <el-table-column label="创建人" width="140" prop="creator" align="center" />
        <el-table-column label="操作" width="200" align="center">
          <template #default="scope">
            <div>
              <el-button @click="copyItem(scope.row)" size="mini" type="success" :disabled="!mockData.statussCode">详情</el-button>
              <el-button @click="viewDetails(scope.row)" size="mini" type="primary" :disabled="!mockData.statussCode">编辑</el-button>
              <el-dropdown trigger="click">
                <el-button style="margin-left: 15px" type="text"  size="mini" icon="el-icon-more" :disabled="!mockData.statussCode"></el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item command="复制" style="color:#409eff" @click="statusClick('已发布',scope.row.id)">
                        复制
                      </el-dropdown-item>
                      <el-dropdown-item command="删除" style="color:#409eff" @click="statusClick('测试中',scope.row.id)">
                        删除
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
              </el-dropdown>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-button
      type="primary"
      style="margin-bottom: 20px; margin-top: 10px;"
      @click="clickAdd"
      :disabled="!mockData.statussCode"
    >
      <i class="el-icon-plus" style="margin-right: 5px;"></i>
      新建期望
    </el-button>
    <div v-if="runResult" style="margin-bottom: 20px">
      <b style="color: #101828CC; font-size: 15px; margin-bottom: 15px">返回响应</b>
    </div>
    <caseResult v-if="runResult" :result="runResult"></caseResult>
  </div>
  </el-scrollbar>
  <!--  新建期望弹窗-->
  <el-dialog title="新建期望" v-model="addDlg" width="60%" :before-close="closeDialog" top="40px" custom-class="class_dialog">
    <el-scrollbar height="82vh" style="padding-right: 20px;">
        <div class="system-icon-content">
          <el-form :model="detailData" :rules="rulesDetail" ref="detailRef" label-position="top">
            <el-form-item label="期望名称" prop="name">
                <el-input v-model="detailData.name"></el-input>
            </el-form-item>
            <el-form-item label="参数条件" prop="conditionData">
              <el-table :data="detailData.conditionData"  stripe empty-text="暂无数据" border>
                <el-table-column label="参数位置" width="180" prop="location"  align="center">
                  <template #default="scope">
                    <el-select v-model="scope.row.location" placeholder="请选择参数位置" style="width: 155px;color: black;padding: 0px">
                      <el-option label="query" value="query"/>
                      <el-option label="path" value="path"/>
                      <el-option label="header" value="header"/>
                      <el-option label="body" value="body"/>
                    </el-select>
                  </template>
                </el-table-column>
                <el-table-column label="参数名" prop="paramName" align="center">
                  <template #default="scope">
                    <el-input v-model="scope.row.paramName"></el-input>
                  </template>
                </el-table-column>
                <el-table-column label="比较" width="180" prop="comparison" align="center" >
                  <template #default="scope">
                    <el-select v-model="scope.row.comparison" placeholder="请选择"  style="width: 155px;color: black;padding: 0px">
                            <el-option
                              v-for="item in options"
                              :key="item.value"
                              :label="item.label"
                              :value="item.value"
                            />
                    </el-select>
                  </template>
                </el-table-column>
                <el-table-column label="参数值" prop="value" align="center">
                  <template #default="scope">
                    <el-input v-model="scope.row.value"></el-input>
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="100" align="center">
                  <template #default="scope">
                      <el-button
                        type="text"
                        size="small"
                        :disabled="scope.$index < 1"
                        @click.prevent="deleteRow(scope.$index)"
                      >  删除
                      </el-button>
                  </template>
                  </el-table-column>
              </el-table>
              <el-button style="width: 100%;margin-top: 20px; background-color: #ecf5ff; color: #409eff;" @click="onAddItem" >
                add Data
              </el-button>
            </el-form-item>
            <div style="margin-bottom: 30px; font-size: 16px">IP 条件
              <el-tooltip content="开启后该期望仅对 指定IP 的地址生效" placement="top" effect="light">
                <i class="el-icon-question" style="margin-left: 4px; color: #909399; font-size: 16px;"></i>
              </el-tooltip>
              <el-switch
                v-model="mockData.statussCode"
                inline-prompt
                size="small"
                @click="switchClick(data)"
                style="--el-switch-on-color: #53a8ff; margin-left: 10px"
              />
            </div>
            <el-form-item label="返回数据" prop="backData">
              <el-menu
                  :default-active="activeIndex"
                  mode="horizontal"
                  @select="handleSelect"
                >
                <el-menu-item index="1">响应体(Response)</el-menu-item>
                <el-menu-item index="2">响应头(headers)</el-menu-item>
                <el-menu-item index="3">更多设置</el-menu-item>
              </el-menu>
                  <div v-if="activeIndex === '1'" class="munu">
                      <el-radio-group v-model="paramType" >
                        <el-radio label="json">application/json</el-radio>
                        <el-radio label="xml">application/xml</el-radio>
                        <el-radio label="text">text/plain</el-radio>
                      </el-radio-group>
          <!--				<div v-if="paramType === 'json'"><Editor v-model="json"></Editor></div>-->
          <!--				<div v-else-if="paramType === 'data'"><Editor v-model="data"></Editor></div>-->
          <!--				<div v-else-if="paramType === 'formData'">-->
                      <el-tooltip :content="sample" placement="top" effect="light">
                        <span class="el-icon-question" style="margin-left: 30px;margin-top:-10px;color: #67c23a;">
                          支持Mock.js语法
                        </span>
                      </el-tooltip>
                    <div ><Editor v-model="json"></Editor></div>
                  </div>

                  <div v-if="activeIndex === '2'" class="munu">
                    <span>示例</span>
                    <div ><Editor v-model="json"></Editor></div>
                  </div>

                  <div v-if="activeIndex === '3'" class="munu">
                    <el-form-item label="返回 HTTP 状态码" prop="code" label-position="right" label-width="100px">
                      <el-input style="width: 150px;" v-model="confData.code"></el-input>
                    </el-form-item>
                    <el-form-item label="返回延迟" prop="time">
                      <el-input style="width: 150px;" v-model="confData.time"></el-input>
                      S
                    </el-form-item>
                  </div>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer" style="text-align: right;">
              <el-button @click="closeDialog" >取 消</el-button>
              <el-button type="primary" @click="createCron" >保 存</el-button>
          </div>
        </div>
    </el-scrollbar >
  </el-dialog>
</template>

<script>
import caseResult from '@/components/common/caseResult.vue';
import Editor from "@/components/common/Editor";
export default {
  props: ['interfaceData'],
  components:{
    caseResult,
    Editor
  },
  data() {
    return {
      mockDlg:true,
      addDlg: false,
      activeIndex:'1',
      mockTitle:'MockUrl: http://139.207.0.0:8080/mock/71b06af7b9c44e17aada1f67e33d81c9/tms/base/otw/uaa/account',
      mockData:{
        method:'',
        statussCode:true,
      },
      detailData:{
        name:'',
        conditionData:[
            {
              location:'',
              paramName:'',
              comparison:'',
              value:''
            },
        ],
        backData:'',
      },
      mockDatas:[
          {
            name:'测试测试1',
            condition:'Query 参数code等于11',
            creator:'何某',
            id:'1'
          },
          {
            name:'测试测试2',
            condition:'Query 参数code等于11',
            creator:'何某',
            id:'2'
          }
      ],
      rulesInterface: {
				url: [
					{
						required: true,
						message: '请输入接口路径信息',
						trigger: 'blur'
					}
				]
			},
      confData:{
          code:'200',
          time:'0'
        },
      rulesDetail: {
        name: [
          {
            required: true,
            message: '请输入期望名称',
            trigger: 'blur'
          },
        ],
        code: [
          {
            required: true,
            message: 'code不可为空',
            trigger: 'blur'
          },
        ],
        time: [
          {
            required: true,
            message: 'time不可为空',
            trigger: 'blur'
          },
        ]
      },
      runResult:{
        "name": "None",
        "type": "api",
        "log_data": [
            [
                "INFO",
                "【INFO】  |   ▶️开始单条用例执行：创建订单"
            ],
            [
                "DEBUG",
                "【DEBUG】  |   临时变量：\n{}"
            ],
            [
                "DEBUG",
                "【DEBUG】  |   全局变量：\n{'host': 'https://tmstest.gree.com', 'headers': {}}"
            ],
            [
                "INFO",
                "【INFO】  |   执行前置脚本"
            ],
            [
                "INFO",
                "【INFO】  |   发送 POST 请求 : 请求地址：https://tmstest.gree.com/tms/business/out/order/create"
            ],
            [
                "DEBUG",
                "【DEBUG】  |   请求头：\n{'User-Agent': 'python-requests/2.28.1', 'Accept-Encoding': 'gzip, deflate, br', 'Accept': '*/*', 'Connection': 'keep-alive', 'Content-Type': 'application/json', 'Content-Length': '981'}"
            ],
            [
                "DEBUG",
                "【DEBUG】  |   请求体：\n{\n  \"fromWarehouseCode\": \"发货实仓地址\",\n  \"fromFinanceWarehouseCode\": \"发货账仓地址\",\n  \"senderName\": \"发货人\",\n  \"senderMobile\": \"发货人荻花\",\n  \"toAddressDetail\": \"目的地\",\n  \"toProvinceCode\": \"目的省\",\n  \"toProvinceName\": \"\",\n  \"toCityCode\": \"目的室\",\n  \"toCityName\": \"\",\n  \"toCountyCode\": \"目的区\",\n  \"toCountyName\": \"\",\n  \"toStreetCode\": \"目的街道\",\n  \"toStreetName\": \"目的\",\n  \"receiverName\": \"收货人\",\n  \"carrierCode\": \"承运商编码\",\n  \"carrierName\": \"\",\n  \"transportTypeCode\": \"承运类型编码\",\n  \"transportTypeName\": \"承运类型名称\",\n  \"num\": \"货物数量\",\n  \"totalVolume\": \"货物总体积\",\n  \"totalWeight\": \"货物总重量\",\n  \"materialName\": \"货物名称\",\n  \"priority\": \"1-一般 2紧急\",\n  \"remark\": \"备注\"\n}"
            ],
            [
                "INFO",
                "【INFO】  |   请求响应状态码:401"
            ],
            [
                "DEBUG",
                "【DEBUG】  |   响应头：\n{'Date': 'Sun, 14 Jul 2024 15:51:01 GMT', 'Content-Type': 'application/json;charset=UTF-8', 'Content-Length': '24', 'Connection': 'keep-alive', 'Vary': 'Origin, Access-Control-Request-Method, Access-Control-Request-Headers, Origin, Access-Control-Request-Method, Access-Control-Request-Headers', 'Server': 'elb'}"
            ],
            [
                "DEBUG",
                "【DEBUG】  |   响应体：\n{\n  \"data\": {},\n  \"result\": 401\n}"
            ],
            [
                "INFO",
                "【INFO】  |   执行后置脚本"
            ],
            [
                "INFO",
                "【INFO】  |   ⏹️步骤运行结束"
            ]
        ],
        "url": "https://tmstest.gree.com/tms/business/out/order/create",
        "method": "POST",
        "status_cede": 401,
        "response_header": {
            "Date": "Sun, 14 Jul 2024 15:51:01 GMT",
            "Content-Type": "application/json;charset=UTF-8",
            "Content-Length": "24",
            "Connection": "keep-alive",
            "Vary": "Origin, Access-Control-Request-Method, Access-Control-Request-Headers, Origin, Access-Control-Request-Method, Access-Control-Request-Headers",
            "Server": "elb"
        },
        "requests_header": {
            "User-Agent": "python-requests/2.28.1",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "*/*",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Content-Length": "981"
        },
        "response_body": "{\n  \"data\": {},\n  \"result\": 401\n}",
        "requests_body": "{\n  \"fromWarehouseCode\": \"发货实仓地址\",\n  \"fromFinanceWarehouseCode\": \"发货账仓地址\",\n  \"senderName\": \"发货人\",\n  \"senderMobile\": \"发货人荻花\",\n  \"toAddressDetail\": \"目的地\",\n  \"toProvinceCode\": \"目的省\",\n  \"toProvinceName\": \"\",\n  \"toCityCode\": \"目的室\",\n  \"toCityName\": \"\",\n  \"toCountyCode\": \"目的区\",\n  \"toCountyName\": \"\",\n  \"toStreetCode\": \"目的街道\",\n  \"toStreetName\": \"目的\",\n  \"receiverName\": \"收货人\",\n  \"carrierCode\": \"承运商编码\",\n  \"carrierName\": \"\",\n  \"transportTypeCode\": \"承运类型编码\",\n  \"transportTypeName\": \"承运类型名称\",\n  \"num\": \"货物数量\",\n  \"totalVolume\": \"货物总体积\",\n  \"totalWeight\": \"货物总重量\",\n  \"materialName\": \"货物名称\",\n  \"priority\": \"1-一般 2紧急\",\n  \"remark\": \"备注\"\n}",
        "state": "成功",
        "run_time": "0.0385s"
      },
      options: [
          { value: 'equal', label: '等于' },
          { value: 'notEqual', label: '不等于' },
          { value: 'contains', label: '包含' },
          { value: 'notContains', label: '不包含' },
          { value: 'greaterThan', label: '大于' },
          { value: 'lessThan', label: '小于' },
          { value: 'greaterThanOrEqual', label: '大于等于' },
          { value: 'lessThanOrEqual', label: '小于等于' },
          { value: 'empty', label: '空' },
          { value: 'notEmpty', label: '非空' }
        ],
      statussCode: true,
      showActions: false,
      paramType: 'json',
      sample:"示例\n" +
          "    {\n" +
          "        \"name\": \"@name\",\n" +
          "        \"age\": '@integer(18, 60)',\n" +
          "        \"birth\": \"@date('yyyy-MM-dd')\",\n" +
          "        \"email\": \"@email\"\n" +
          "      }"
    }
  },
  methods:{
    closeModal() {
      this.$emit('close-modal');
    },

    clickClear(){
      this.closeModal()
    },

    // 点击新建期望
    clickAdd() {
      this.addDlg = true;
    },

    // 新建期望弹窗关闭
    closeDialog() {
      this.addDlg = false;
    },

    // 新增表格数据
    onAddItem() {
      const newItem = {
        location: '',
        paramName: '',
        comparison: '',
        value: ''
      };
      this.detailData.conditionData.push(newItem);
    },
    // 删除表格数据
    deleteRow(index) {
      this.detailData.conditionData.splice(index, 1);
    },

    handleSelect(index) {
      this.activeIndex = index;
    }

  },
created() {
    this.mockData = this.interfaceData
  }
}
</script>

<style scoped>
.el-dropdown-menu__item {
  color: #606266;
  &:hover {
    background-color: #ebf5ff;
  }
}
/deep/ .el-form-item--small .el-form-item__label {
    line-height: 32px;
    font-size: 16px;
}

.system-icon-content {
  max-height: 82vh;
}
.munu{
  margin-top: 5px;
  margin-left: 20px;
  margin-bottom: 5px;
}
</style>