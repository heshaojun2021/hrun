<template>
  <el-scrollbar height="calc(100vh);padding-right:10px;">
  <div style="margin: 15px">
    <div style="display: flex; justify-content: space-between;margin-bottom: 15px">
      <b style="color: #101828CC; font-size: 15px">请求信息</b>
      <span style="color: #606266; font-size: 14px; display: flex; align-items: center;">开启/禁用Mock
        <el-switch
          v-model="mockData.statusCode"
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
        <el-col :span="13">
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
        <el-col :span="8" >
          <el-form-item prop="name" label="接口名称">
              <el-input v-model="mockData.name" placeholder="请输入接口名称" style="font-size: 14px;">
              </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="3" >
          <el-button @click="addClick" type="primary" icon="el-icon-edit-outline" :disabled="!mockData.statusCode">保存</el-button>
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
              <el-button @click="copyItem(scope.row)" size="mini" type="success" :disabled="!mockData.statusCode">详情</el-button>
              <el-button @click="viewDetails(scope.row)" size="mini" type="primary" :disabled="!mockData.statusCode">编辑</el-button>
              <el-dropdown trigger="click">
                <el-button style="margin-left: 15px" type="text"  size="mini" icon="el-icon-more" :disabled="!mockData.statusCode"></el-button>
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
      :disabled="!mockData.statusCode"
    >
      <i class="el-icon-plus" style="margin-right: 5px;"></i>
      新建期望
    </el-button>
    <div style="margin-bottom: 20px">
      <b style="color: #101828CC; font-size: 15px; margin-bottom: 15px">调用记录</b>
      <el-card style="margin-top: 15px">
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
      </el-card>
    </div>

  </div>
  </el-scrollbar>
  <!--  新建期望弹窗-->
  <el-dialog title="新建期望" v-model="addDlg" width="65%" :before-close="closeDialog" top="40px" custom-class="class_dialog">
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
                <i class="el-icon-question" style="color: #53a8ff; font-size: 16px;"></i>
              </el-tooltip>
              <el-switch
                v-model="detailData.statusCode"
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
                <el-menu-item index="1">响应体(response)</el-menu-item>
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
                      <el-tooltip :content="sampleResponse" placement="top" effect="light">
                        <span class="el-icon-question" style="margin-left: 30px;color: #67c23a;">
                          支持Mock.js语法
                        </span>
                      </el-tooltip>
                    <div ><Editor v-model="json"></Editor></div>
                  </div>

                  <div v-if="activeIndex === '2'" class="munu">
                     <el-tooltip :content="sampleHeader" placement="top" effect="light">
                      <span class="el-icon-question" style="color: #67c23a;">
                        示例
                      </span>
                    </el-tooltip>
                    <div ><Editor v-model="headers"></Editor></div>
                  </div>

                  <div v-if="activeIndex === '3'" class="munu">
                    <el-form-item label="返回 HTTP 状态码" prop="code" label-position="right" label-width="100px">
                      <el-input style="width: 150px;" v-model="confData.code"></el-input>
                    </el-form-item>
                    <el-form-item label="返回延迟" prop="time">
                    <el-input-number
                      v-model="confData.time"
                      :min="0"
                      :max="999"
                      size="mini"
                      controls-position="right"
                      placeholder="秒"
                    >
                    </el-input-number>
                    <span style="margin-left: 10px">秒</span>
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
        statusCode:true,
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
        statusCode:true,
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
				],
        name: [
					{
						required: true,
						message: '请输入接口名称',
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
      mockLog:[{
            "create_time": "2024-02-18T10:30:00",
            "method": "GET",
            "url": "/api/v1/user/login",
            "ip": "192.168.1.1",
            "status_code": "200",
            "time_consuming": "0.1s",
          },
          {
            "create_time": "2024-02-18T10:30:00",
            "method": "GET",
            "url": "/api/v1/user/login",
            "ip": "192.168.1.1",
            "status_code": "200",
            "time_consuming": "0.1s",
          },
          {
            "create_time": "2024-02-18T10:30:00",
            "method": "POST",
            "url": "/api/v1/user/login",
            "ip": "192.168.1.101",
            "status_code": "400",
            "time_consuming": "0.1s",
          },
          {
            "create_time": "2024-02-18T10:30:00",
            "method": "POST",
            "url": "/api/v1/user/login",
            "ip": "192.168.1.1",
            "status_code": "200",
            "time_consuming": "0.5s",
          },
          {
            "create_time": "2024-02-18T10:30:00",
            "method": "POST",
            "url": "/api/v1/user/login",
            "ip": "192.168.1.1",
            "status_code": "200",
            "time_consuming": "0.5s",
          },
          {
            "create_time": "2024-02-18T10:30:00",
            "method": "POST",
            "url": "/api/v1/user/login",
            "ip": "192.168.1.1",
            "status_code": "200",
            "time_consuming": "0.5s",
          },
          {
            "create_time": "2024-02-18T10:30:00",
            "method": "POST",
            "url": "/api/v1/user/login",
            "ip": "192.168.1.1",
            "status_code": "200",
            "time_consuming": "0.5s",
          }
          ],
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
      showActions: false,
      paramType: 'json',
      sampleResponse:"示例\n" +
          "    {\n" +
          "        \"name\": \"@name\",\n" +
          "        \"age\": '@integer(18, 60)',\n" +
          "        \"birth\": \"@date('yyyy-MM-dd')\",\n" +
          "        \"email\": \"@email\"\n" +
          "      }",
      sampleHeader: "{\n" +
          "        \"Content-Type\": \"application/json\",\n" +
          "        \"Authorization\": \"Bearer {{token}}\"\n" +
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