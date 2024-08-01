<template>
  <el-scrollbar height="calc(100vh);padding-right:10px;">
  <div style="margin: 15px">
    <div style="display: flex; justify-content: space-between;margin-bottom: 15px">
      <b style="color: #101828CC; font-size: 15px">请求信息</b>
      <span style="color: #606266; font-size: 14px; display: flex; align-items: center;">开启/禁用Mock
        <el-switch
          v-model="mockData.status"
          inline-prompt
          size="small"
          style="--el-switch-on-color: #53a8ff; margin-left: 10px"
        />
      </span>
    </div>
    <el-alert v-if="mockData.mockTitle" style="margin-bottom: 10px" class="el-icon-circle-check" :title="mockData.mockTitle" type="success" />
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
          <el-button v-if="mockData.mockTitle" @click="editMock()" type="primary" icon="el-icon-edit-outline">保存</el-button>
          <el-button v-else @click="addMock()" type="primary" icon="el-icon-edit-outline">保存</el-button>

        </el-col>
    </el-row>
    </el-form>
    <div><b style="color: #101828CC; font-size: 15px">Mock 期望</b></div>
    <div style="margin-top: 15px">
      <el-table :data="mockData.MockDetail"  stripe empty-text="暂无数据" border>
        <el-table-column label="名称" width="180" prop="name"  align="center" />
        <el-table-column label="条件" prop="remark" align="center">
          <template #default="scope">
            <div style="color: #66b1ff" v-html="scope.row.remark"></div>
          </template>

        </el-table-column>
        <el-table-column label="创建人" width="140" prop="creator" align="center" />
        <el-table-column label="操作" width="200" align="center">
          <template #default="scope">
            <div>
              <el-button @click="openDialog('view', scope.row)" size="mini" type="success" :disabled="!mockData.status">详情</el-button>
              <el-button @click="openDialog('edit', scope.row)" size="mini" type="primary" :disabled="!mockData.status">编辑</el-button>
              <el-dropdown trigger="click">
                <el-button style="margin-left: 15px" type="text"  size="mini" icon="el-icon-more" :disabled="!mockData.status"></el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item command="复制" style="color:#409eff" @click="copyMockDetail(scope.row)">
                        复制
                      </el-dropdown-item>
                      <el-dropdown-item command="删除" style="color:#409eff" @click="clickDel(scope.row.id)">
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
      @click="openDialog('add')"
      :disabled="!mockData.status"
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
  <el-dialog :title="dialogTitle" v-model="dialogVisible" width="65%" :before-close="closeDialog" top="40px" destroy-on-close custom-class="class_dialog">
    <el-scrollbar height="82vh" style="padding-right: 20px;">
        <div class="system-icon-content">
          <el-form :model="detailData" :rules="rulesDetail" ref="detailRef" label-position="top">
            <el-form-item label="期望名称" prop="name">
                <el-input v-model="detailData.name"></el-input>
            </el-form-item>
            <el-form-item label="参数条件" prop="conditionForm" >
              <el-table :data="detailData.conditionForm"  stripe empty-text="暂无数据" border>
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
              <el-button v-if="dialogTitle !== '查看期望'" style="width: 100%;margin-top: 20px; background-color: #ecf5ff; color: #409eff;" @click="onAddItem" >
                add Data
              </el-button>
            </el-form-item>
            <div style="margin-bottom: 30px; font-size: 16px">IP 条件
              <el-tooltip content="开启后该期望仅对 指定IP 的地址生效; 填写示例：http://127.0.0.1:8080" :enterable="false" placement="top" effect="light">
                <i class="el-icon-question" style="color: #53a8ff; font-size: 16px;"></i>
              </el-tooltip>
              <el-switch
                v-model="detailData.ipCode"
                inline-prompt
                size="small"
                style="--el-switch-on-color: #53a8ff; margin-left: 10px"
              />
              <el-input v-if="detailData.ipCode" style="margin-top: 10px" v-model="detailData.ipInput"></el-input>
            </div>
            <el-form-item label="返回数据">
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
                      <el-radio-group v-model="detailData.response.paramType" >
                        <el-radio label="json">application/json</el-radio>
                        <el-radio label="xml">application/xml</el-radio>
                        <el-radio label="html">html/plain</el-radio>
                      </el-radio-group>
                      <el-tooltip :content="sampleResponse" placement="top" effect="light">
                        <span class="el-icon-question" style="margin-left: 30px;color: #67c23a;">
                          支持Mock.js语法
                        </span>
                      </el-tooltip>
                    <div>
                    <el-row>
                      <el-col :span="18">
                        <Editor v-model="detailData.response.data"></Editor>
                      </el-col>
                      <el-col style="margin-top: -15px" :span="6">
                        <el-divider>脚本模板</el-divider>
                          <el-scrollbar height="380px">
                            <div style="margin-left: 10px">
                            <div v-for="tag in mockTags" :key="tag" style="margin-bottom: 7px;">
                              <el-tooltip :content="`${tag.txt}`" placement="top" effect="light">
                                <el-check-tag checked @click="copyText(tag.mockJS)" style="margin-right: 10px">
                                  {{ tag.mockJS }}
                                </el-check-tag>
                              </el-tooltip>
                            </div>
                          </div>
                          </el-scrollbar>
                      </el-col>
                    </el-row>
                    </div>
                  </div>

                  <div v-if="activeIndex === '2'" class="munu">
                     <el-tooltip :content="sampleHeader" placement="top" effect="light">
                      <span class="el-icon-question" style="color: #67c23a;">
                        示例
                      </span>
                    </el-tooltip>
                    <el-row>
                      <el-col :span="18">
                        <Editor v-model="detailData.response.data"></Editor>
                      </el-col>
                      <el-col style="margin-top: -15px" :span="6">
                        <el-divider>脚本模板</el-divider>
                          <el-scrollbar height="380px">
                            <div style="margin-left: 10px">
                            <div v-for="tag in mockTags" :key="tag" style="margin-bottom: 7px;">
                              <el-tooltip :content="`${tag.txt}`" placement="top" effect="light">
                                <el-check-tag checked @click="copyText(tag.mockJS)" style="margin-right: 10px">
                                  {{ tag.mockJS }}
                                </el-check-tag>
                              </el-tooltip>
                            </div>
                          </div>
                          </el-scrollbar>
                      </el-col>
                    </el-row>
                  </div>

                  <div v-if="activeIndex === '3'" class="munu">
                    <el-form-item label="返回 HTTP 状态码" prop="statusCode" label-position="right" label-width="100px">
                      <el-input style="width: 150px;" v-model="detailData.config.statusCode"></el-input>
                    </el-form-item>
                    <el-form-item label="返回延迟" prop="time">
                    <el-input-number
                      v-model="detailData.config.time"
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
          <div slot="footer" class="dialog-footer" style="text-align: center;">
              <el-button @click="closeDialog" >取 消</el-button>
              <el-button v-if="dialogTitle === '新建期望'" type="primary" @click="addMockDetail" >保 存</el-button>
              <el-button v-if="dialogTitle === '编辑期望'" type="primary" @click="editMockDetail" >保 存</el-button>
          </div>
        </div>
    </el-scrollbar >
  </el-dialog>
</template>

<script>
import caseResult from '@/components/common/caseResult.vue';
import Editor from "@/components/common/Editor";
import {ElMessage, ElMessageBox} from "element-plus";
import {mapState} from "vuex";
export default {
  props: ['interfaceData'],
  components:{
    caseResult,
    Editor,
    ElMessage
  },
  computed: {
    username() {
			return window.sessionStorage.getItem('username');
		},
  },
  data() {
    return {
      mockDlg:true,
      dialogVisible: false,
      dialogType: '', // 对话框类型，用于区分不同类型的对话框
      dialogTitle: '', // 对话框标题，根据不同类型动态设置
      activeIndex:'1',
      mockData:{
        id:'',
        newInterface:'',
        method:'',
        name:'',
        url:'',
        status:null,
        mockTitle:'',
        MockDetail:[],
      },
      detailData:{
        id:'',
        name:'',
        conditionForm:[
            {
              location:'',
              paramName:'',
              comparison:'',
              value:''
            },

        ],
        ipCode:false,
        ipInput:'',
        response:{paramType: 'json',data:'{}'},
        headers:'{}',
        config:{statusCode:'200', time:'0'},
        creator:'',
        remark:''
      },
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
      rulesDetail: {
        name: [
          {
            required: true,
            message: '请输入期望名称',
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
          "      }",
      mockTags: [
          {mockJS: '@name()',txt:'随机生成名字'},
          {mockJS: '@integer(20, 40)',txt:'随机生成20到40之间的值'},
          {mockJS: '@email',txt:'随机生成邮箱'},
          {mockJS: '@telephone()',txt:'返回一个随机的11位手机号码'},
          {mockJS: '@natural(1,100)',txt:'返回一个随机的1-100的自然数（大于等于 0 的整数）'},
          {mockJS: '@float( 1, 10, 2, 5 )',txt:'返回一个随机的浮点数，整数1-10，小数部分位数的最小值2，最大值5'},
          {mockJS: '@character(pool)',txt:'从字符串池返回随机的字符'},
          {mockJS: '@string( pool, 1, 10 )',txt:'从字符串池返回一个随机字符串，字符数1-10'},
          {mockJS: '@range( 1, 100, 1 )',txt:'返回一个整型数组，参数分别：start：起始值，stop：结束值，step：步长'},
          {mockJS: '@now(\'yyyy-MM-dd HH:mm:ss\')',txt:'返回当前日期字符串。例：2014-04-29 20:08:38'},
          {mockJS: '@date(\'yyyy-MM-dd\')',txt:'返回一个随机的日期字符串。例：1983-01-29'},
          {mockJS: '@guid()',txt:'随机生成一个 GUID。例：eFD616Bd-e149-c98E-a041-5e12ED0C94Fd'},
          {mockJS: '@increment(1)',txt:'随机生成主键，从1起，整数自增的步长'},
          {mockJS: '@url(\'http\')',txt:'随机生成一个http URL'},
          {mockJS: '@protocol()',txt:'随机生成一个 URL 协议。例：http ftp'},
          {mockJS: '@domain()',txt:'随机生成一个域名'},
          {mockJS: '@province()',txt:'随机生成一个（中国）省（或直辖市、自治区、特别行政区）'},
          {mockJS: '@city()',txt:'随机生成一个（中国）市'},
          {mockJS: '@county()',txt:'随机生成一个（中国）县'},
          {mockJS: '@county(true)',txt:'随机生成一个（中国）县（带省市）。例：甘肃省 白银市 会宁县'},
          {mockJS: '@zip()',txt:'随机生成一个邮政编码'},
          {mockJS: '@color()',txt:'随机生成颜色，格式为 \'#RRGGBB\''},
          {mockJS: '@paragraph()',txt:'随机生成一段文本'},
          {mockJS: '@cparagraph()',txt:'随机生成一段中文文本'},
          {mockJS: '@word()',txt:'随机生成一个单词'}

          ]
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

    // 期望弹窗关闭
    closeDialog() {
      this.dialogVisible = false;
      this.getMockData();
      this.detailData = {
                          name:'',
                          conditionForm:[
                              {
                                location:'',
                                paramName:'',
                                comparison:'',
                                value:''
                              },
                          ],
                          ipCode:false,
                          ipInput:'',
                          response:{paramType: 'json',data:''},
                          headers:'',
                          config:{statusCode:'200', time:'0'}
      };
    },

    // 新增表格数据
    onAddItem() {
      const newItem = {
        location: '',
        paramName: '',
        comparison: '',
        value: ''
      };
      this.detailData.conditionForm.push(newItem);
    },
    // 删除表格数据
    deleteRow(index) {
      this.detailData.conditionForm.splice(index, 1);
    },

    handleSelect(index) {
      this.activeIndex = index;
    },

    // 获取mock数据
    async getMockData() {
      const response = await this.$api.getMock(this.interfaceData.id);
      if (response.status === 200) {
        this.mockData.id = response.data.id;
        this.mockData.name = this.interfaceData.name;
        this.mockData.url = this.interfaceData.url;
        this.mockData.method = this.interfaceData.method;
        this.mockData.newInterface = this.interfaceData.id;
        this.mockData.status = response.data.status;
        this.mockData.mockTitle = response.data.MockUrl;
        this.mockData.MockDetail = response.data.MockDetail;
        }
      },

    // 保存接口信息
    async editInterface() {
      const params = {
        method:this.mockData.method,
        name:this.mockData.name,
        url:this.mockData.url
      }
      await this.$api.updatenewInterface(this.interfaceData.id, params);
    },

    // 保存mock信息
    async editMock() {
      const params = {...this.mockData}
      delete params.mockTitle;
      delete params.MockDetail;
      const response = await this.$api.updateMock(this.mockData.id,params);
      if (response.status === 200) {
          ElMessage({
            type: 'success',
            message: '保存成功',
            duration: 1000
          });
          this.editInterface();
          this.getMockData()
      }

    },

    // 新增mock信息
    async addMock() {
      const params = {...this.mockData}
      params.creator = this.username;
      delete params.id;
      delete params.mockTitle;
      delete params.MockDetail;
      const response = await this.$api.createMock(params);
      if (response.status === 201) {
          this.editInterface();
          this.getMockData()
      }
    },

    // 新增mock详情信息
    async addMockDetail() {
      const params = {...this.detailData}
      delete params.id;
      params.creator = this.username;
      params.mock = this.mockData.id;
      console.log(params)
      const response = await this.$api.createDetail(params);
      if (response.status === 201) {
          ElMessage({
            type: 'success',
            message: '保存成功',
            duration: 1000
          });
          this.getMockData();
          this.closeDialog();
      }
    },

    // 修改mock详情信息
    async editMockDetail() {
      const params = {...this.detailData}
      delete params.creator;
      params.modifier = this.username;
      const response = await this.$api.updateDetail(params.id,params);
      if (response.status === 200) {
          ElMessage({
            type: 'success',
            message: '保存成功',
            duration: 1000
          });
          this.getMockData();
          this.closeDialog();
      }
    },

    // 复制mock详情信息
    async copyMockDetail(data) {
      const params = data
      delete params.id;
      params.creator = this.username;
      params.name = params.name + '_副本';
      const response = await this.$api.createDetail(params);
      if (response.status === 201) {
          ElMessage({
            type: 'success',
            message: '保存成功',
            duration: 1000
          });
          this.getMockData()
      }
    },

    clickDel(id) {
			ElMessageBox.confirm('确定要删除该期望吗?', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning'
			})
				.then(() => {
					this.delMockDetail(id);
				})
				.catch(() => {
					ElMessage({
						type: 'info',
						message: '取消删除',
						duration: 1000
					});
				});
		},

    // 删除mock详情信息
    async delMockDetail(id) {
      const response = await this.$api.delDetail(id);
			if (response.status === 204) {
        ElMessage({
          type: 'success',
          message: '删除成功',
          duration: 1000
        });
        this.getMockData();
      }

		},

    openDialog(type, data) {
      this.dialogType = type;
      this.dialogVisible = true;

      // 根据不同的对话框类型设置标题
      switch (type) {
        case 'add':
          this.dialogTitle = '新建期望';
          break;

        case 'edit':
          this.dialogTitle = '编辑期望';
          this.detailData = data;
          break;

        case 'view':
          this.dialogTitle = '查看期望';
          this.detailData = data;
          break;

        default:
          this.dialogTitle = '';
          break;
      }
    },
    copyText(text) {
      const textarea = document.createElement('textarea');
      textarea.value = text;
      document.body.appendChild(textarea);
      textarea.select();
      try {
        const success = document.execCommand('copy');
        if (success) {
            this.$message({
              message: '已复制到剪贴板',
              type: 'success'
            });
        }
        else {
            this.$message.error('复制失败，请手动复制');
        }
      } catch (error){
            console.error('复制失败:', error);
            this.$message.error('复制失败，请手动复制');
          }
      document.body.removeChild(textarea);
    },


  },
created() {
  this.getMockData();
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