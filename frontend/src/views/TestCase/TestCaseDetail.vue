<template>
    <el-card>
      <div slot="header">
        <div style="display: flex; justify-content: space-between; align-items: center;height: 2px">
          <div style="margin-right: 15px">
            <el-button size="large" type="text" icon="el-icon-caret-left" @click="goBack">返回</el-button>
            <span style="margin-left: 15px;font-weight: bold">
              {{ this.case !== null ? '编辑用例' : '新增用例' }}
            </span>
          </div>
          <div>
            <el-button v-if="!isExpand" icon="el-icon-sort" type="primary" @click="rowOpenORFold(true)" round>展开全部</el-button>
            <el-button v-if="isExpand" icon="el-icon-sort" type="primary" @click="rowOpenORFold(false)" round>折叠全部</el-button>
<!--            <el-dropdown style="margin-right: 10px" trigger="click">-->
<!--              <el-button type="warning" round >添加步骤-->
<!--                 <i class="el-icon-arrow-down el-icon&#45;&#45;right"></i>-->
<!--              </el-button>-->
<!--              <template #dropdown>-->
<!--                <el-dropdown-menu>-->
<!--                  <el-dropdown-item command='api' style="color:#61649f" @click="showApiCite">-->
<!--                     <i class="el-icon-connection" style="margin-right: -1px;"></i>-->
<!--                    引用接口-->
<!--                </el-dropdown-item>-->
<!--                <el-dropdown-item command='condition' style="color:#E6A23C" @click="AddController('if')">-->
<!--                     <i class="el-icon-share" style="margin-right: -1px;"></i>-->
<!--                    条件控制器-->
<!--                </el-dropdown-item>-->
<!--                <el-dropdown-item command='cyclic' style="color:#02A7F0FF" @click="AddController('for')">-->
<!--                     <i class="el-icon-refresh" style="margin-right: -1px;"></i>-->
<!--                    循环控制器-->
<!--                </el-dropdown-item>-->
<!--                <el-dropdown-item command='script' style="color:#7B4D12FF" @click="AddController('script')">-->
<!--                     <i class="el-icon-reading" style="margin-right: -1px;"></i>-->
<!--                    自定义脚本-->
<!--                </el-dropdown-item>-->
<!--                <el-dropdown-item command='sql' style="color:#783887FF" @click="AddController('sql')">-->
<!--                     <i class="el-icon-coin" style="margin-right: -1px;"></i>-->
<!--                    SQL控制器-->
<!--                </el-dropdown-item>-->
<!--               <el-dropdown-item command='time' style="color:#67C23AFF" @click="AddController('time')">-->
<!--                     <i class="el-icon-timer" style="margin-right: -1px;"></i>-->
<!--                    等待控制器-->
<!--                </el-dropdown-item>-->
<!--                </el-dropdown-menu>-->
<!--              </template>-->
<!--            </el-dropdown>-->
            <el-button  icon="el-icon-bug" type="success" @click="runCase" round>调试</el-button>
            <el-button v-if="this.case" type="primary" @click="editCaseSave" round>保存</el-button>
            <el-button v-else type="primary" @click="addCaseSave" round>保存</el-button>
          </div>
        </div>
      </div>
    </el-card>
    <el-row :gutter="10">
    <!-- 左边内容-->
    <el-col :span="6">
    <div class="tree-component">
      <el-form :model="editForm"  :rules="rulesCase" ref="CaseRef" label-width="80px" style="max-width: 500px">
      <el-form-item label="用例名称"  prop="name" size="mini">
        <el-input  v-model="editForm.name"  placeholder="请输入用例名称"/>
      </el-form-item>
      <el-form-item prop="project_id" label="所属项目" size="mini">
        <el-input v-model="editForm.project_id"   disabled />
      </el-form-item>
			<el-form-item label="用例描述" prop="desc">
        <el-input type="textarea" v-model="editForm.desc"   placeholder="请输入备注"/>
      </el-form-item>
      <el-form-item label="步骤总数：" label-width="93px"><div style="color: #00aaff;font-weight: bold;">{{editForm.stepCount}}</div></el-form-item>
		</el-form>
    </div>
    </el-col>
    <!-- 右边内容-->
    <el-col :span="18">
      <div class="stepStyle">
        <el-tag class="el-icon-plus" color="#61649f" style="margin-right: 10px;width: 100px" @click="showApiCite">HTTP请求</el-tag>
        <el-tag class="el-icon-plus" color="#E6A23C" style="margin-right: 10px;width: 100px" @click="AddController('if')">条件控制器</el-tag>
        <el-tag class="el-icon-plus" color="#02A7F0FF" style="margin-right: 10px;width: 100px" @click="AddController('for')">循环控制器</el-tag>
        <el-tag class="el-icon-plus" color="#7B4D12FF" style="margin-right: 10px;width: 100px" @click="AddController('script')">自定义脚本</el-tag>
        <el-tag class="el-icon-plus" color="#783887FF" style="margin-right: 10px;width: 100px" @click="AddController('sql')">SQL控制器</el-tag>
        <el-tag class="el-icon-plus" color="#67C23AFF" style="margin-right: 10px;width: 100px" @click="AddController('time')">等待控制器</el-tag>
      </div>
      <el-scrollbar height="calc(100vh - 155px)">
      <div style="margin-left: 20px">
      <el-tree
        :data="steps"
        :props="defaultProps"
        draggable
        :key="treeKey"
			  :default-expand-all="isExpand"
        :expand-on-click-node="false"
        @node-click="handleStepClick"
        :allow-drop="allowDrop"
        @node-drop="updateStepOrder"
        :node-drag-start="handleDragScroll"
      >
    <template v-slot="{ node,data }">
<!--  <el-checkbox v-model="data.checked" @change="handleCheckboxChange(data)" />-->
      <el-card  v-if="data.stepInfo">
        <div slot="header" >
          <el-col :span="20">
            <div class="style">
              <!--api展示-->
              <div v-if="data.stepInfo.type==='api'">
              <span  slot="header" class="card-title">
                  <div style="font-weight: bold;margin-top: -9px">
                    <span class="icon" style="color: rgb(97, 100, 159)">{{ getCardIndex(node.parent, node) }}</span>
                    <el-tag color="#61649f" style="margin-right: 20px;height: 25px;font-size: 12px;line-height: 25px;">HTTP请求</el-tag>
                    <span style=" min-width: 60px;display: inline-block;">
                      <span v-if="data.stepInfo.method === 'POST'">
                        <b style="color: #49cc90;font-size: 15px">{{ data.stepInfo.method }}</b>
                      </span>
                      <span v-if="data.stepInfo.method === 'GET'">
                        <b style="color: #61affe;font-size: 15px">{{ data.stepInfo.method }}</b>
                      </span>
                      <span v-if="data.stepInfo.method === 'PUT'">
                        <b style="color: #fca130;font-size: 15px">{{ data.stepInfo.method }}</b>
                      </span>
                      <span v-if="data.stepInfo.method === 'PATCH'">
                        <b style="color: #50e3c2;font-size: 15px">{{ data.stepInfo.method }}</b>
                      </span>
                      <span v-if="data.stepInfo.method === 'DELETE'">
                        <b style="color: #f93e3e;font-size: 15px">{{ data.stepInfo.method }}</b>
                      </span>
                      <span v-if="data.stepInfo.method === 'DEAD'">
                        <b style="color: rgb(201, 233, 104);font-size: 15px">{{ data.stepInfo.method }}</b>
                      </span>
                    </span>
                  </div>
                  <el-button style="margin-top:-13px;margin-bottom: -2px" type="text" size="max">全局环境</el-button>
                    <b class="card-url">{{ data.stepInfo.url  }}</b>
                    <span class="card-name">{{data.stepInfo.name }}</span>
              </span>
              </div>

              <!--if控制器展示-->
              <div v-if="data.stepInfo.type==='if'">
              <span slot="header" class="card-title">
                <div style="margin-top: -9px">
                  <span class="icon" style="color: rgb(230, 162, 60);">{{ getCardIndex(node.parent, node) }}</span>
                  <el-tag color="rgb(230, 162, 60)" style="font-weight: bold; margin-right: 20px;height: 25px;font-size: 12px;line-height: 25px;">条件控制器</el-tag>
                  <span>
                    <el-input class="input-def" placeholder="变量，例如{{name}}" v-model="data.stepInfo.content.variable"/>
                    <el-select v-model="data.stepInfo.content.JudgmentMode" placeholder="请选择" size="small" style="margin-right: 8px;width: 100px">
                        <el-option
                          v-for="item in options"
                          :key="item.value"
                          :label="item.label"
                          :value="item.value"
                        />
                    </el-select>
                    <el-input class="input-def" placeholder="值" v-model="data.stepInfo.content.value"/>
                    <el-input class="input-def" placeholder="备注"  v-model="data.stepInfo.desc"/>
                  </span>
                </div>
              </span>
              </div>

              <!--循环控制器展示-->
              <div v-if="data.stepInfo.type==='for'" @click="toggleExpand(data.stepInfo)">
              <span slot="header" class="card-title" >
                <div style="margin-top: -12px">
                  <span class="icon" style="color: rgb(2, 167, 240)">{{ getCardIndex(node.parent, node) }}</span>
                  <el-tag color="rgb(2, 167, 240)" style="font-weight: bold; margin-right: 20px;height: 25px;font-size: 12px;line-height: 25px;">循环控制器</el-tag>
<!--                  <el-button @click="toggleExpand(data.stepInfo)"-->
<!--                             type="text"-->
<!--                             style="margin-right: 10px;">-->
<!--                    <el-icon v-if=" data.stepInfo.dlg">-->
<!--                      <ArrowDown/>-->
<!--                    </el-icon>-->
<!--                  <el-icon v-else>-->
<!--                    <ArrowRight />-->
<!--                  </el-icon>-->
<!--                  </el-button>-->
                  <el-radio-group v-model="data.stepInfo.content.select" @click.stop>
                    <el-radio label="count" value="count" >次数循环</el-radio>
                    <el-radio label="for" value="for">for循环</el-radio>
                    <el-radio label="while" value="while" disabled>while循环</el-radio>
                  </el-radio-group>
                </div>
              </span>
              <div v-if="data.stepInfo.dlg" :key="data.id" @click.stop>
              <div v-if="data.stepInfo.content.select==='count' || data.stepInfo.content.select===''">
                <div class="loop">
                  <span style="padding-right: 5px">循环次数</span>
                  <el-input v-model="data.stepInfo.content.cycleIndex" style="width: 200px" placeholder="循环次数" />
                  <span style="padding-right: 5px;padding-left: 10px">循环间隔</span>
                    <el-input-number
                      v-model="data.stepInfo.content.cycleInterval"
                      :min="0"
                      :max="999"
                      size="small"
                      controls-position="right"
                      placeholder="秒"
                    />
                  <span style="margin-left: 10px">秒</span>
                </div>
              </div>
              <div v-if="data.stepInfo.content.select==='for'">
                <div class="loop">
                  <el-input style="width: 200px" placeholder="定义变量名称" v-model="data.stepInfo.content.variableName"/>
                  <b style="margin-left: 10px;margin-right: 10px">in</b>
                  <el-input style="width: 200px" placeholder="变量，例如{{name}}" v-model="data.stepInfo.content.variable"/>
                  <span style="padding-right: 5px;padding-left: 10px">循环间隔</span>
                    <el-input-number
                      v-model="data.stepInfo.content.cycleInterval"
                      :min="0"
                      :max="999"
                      size="small"
                      controls-position="right"
                      placeholder="秒"
                    />
                  <span style="margin-left: 10px">秒</span>
                </div>
              </div>
              <div v-if="data.stepInfo.content.select==='while'" ><div class="loop">敬请期待！</div></div>
              </div>
             </div>

              <!--自定义脚本展示-->
              <div v-if="data.stepInfo.type==='script'">
              <span slot="header" class="card-title">
                <div style="margin-top: -9px">
                  <span class="icon" style="color: rgb(123, 77, 18)">{{ getCardIndex(node.parent, node) }}</span>
                  <el-tag color="rgb(123, 77, 18)" style="font-weight: bold; margin-right: 20px;height: 25px;font-size: 12px;line-height: 25px;">自定义脚本</el-tag>
                   <el-input v-if="data.stepInfo.inputDlg" v-model="data.stepInfo.name" @blur="cancelEditing(data.stepInfo)" ref="input" maxlength="50" @click.stop></el-input>
                      <el-button v-else class="script-button" plain type="text" @click="startEditing(data.stepInfo)" @click.stop>{{data.stepInfo.name}} <i class="el-icon-edit"></i></el-button>
                  </div>
              </span>
              <el-row :gutter="10" v-show="data.stepInfo.dlg" @click.stop>
                <el-col :span="18" style="margin-top: 15px"><Editor v-model="data.stepInfo.script" lang="python" theme="chrome"></Editor></el-col>
                <el-col :span="6">
                  <el-divider>脚本模板</el-divider>
                  <div class="code_mod"><el-button type="success" size="mini" plain @click="addSetUptCodeMod(data.stepInfo,'func')">导入变量模块</el-button></div>
                  <div class="code_mod"><el-button type="success" size="mini" plain @click="addSetUptCodeMod(data.stepInfo,'ENV')">预设全局变量</el-button></div>
                  <div class="code_mod"><el-button type="success" size="mini" plain @click="addSetUptCodeMod(data.stepInfo,'env')">预设局部变量</el-button></div>
                  <div class="code_mod"><el-button type="success" size="mini" plain @click="addSetUptCodeMod(data.stepInfo,'sql')">执行sql查询</el-button></div>
                </el-col>
				      </el-row>
            </div>

              <!--sql控制器展示-->
              <div v-if="data.stepInfo.type==='sql'">
              <span slot="header" class="card-title">
                <div style="margin-top: -9px">
                  <span class="icon" style="color: rgb(120, 56, 135)">{{ getCardIndex(node.parent, node) }}</span>
                  <el-tag color="rgb(120, 56, 135)" style="font-weight: bold; margin-right: 20px;height: 25px;font-size: 12px;line-height: 25px;">SQL控制器</el-tag>
                  <el-input v-if="data.stepInfo.inputDlg" v-model="data.stepInfo.name" @blur="cancelEditing(data.stepInfo)" ref="input" maxlength="50" @click.stop></el-input>
                  <el-button v-else class="script-button" plain type="text" @click="startEditing(data.stepInfo)" @click.stop>{{data.stepInfo.name}} <i class="el-icon-edit"></i></el-button>
                </div>
              </span>
              <div v-show="data.stepInfo.dlg" style="margin-left: 50%;margin-top: 30px"><i>该功能敬请期待噢！</i></div>
            </div>

              <!--time控制器展示-->
              <div v-if="data.stepInfo.type==='time'">
              <span slot="header" class="card-title">
                <div style="margin-top: -9px">
                  <span class="icon" style="color: rgb(103, 194, 58)">{{ getCardIndex(node.parent, node) }}</span>
                  <el-tag color="rgb(103, 194, 58)" style="font-weight: bold; margin-right: 20px;height: 25px;font-size: 12px;line-height: 25px;">等待控制器</el-tag>
                    <el-input-number
                      v-model="data.stepInfo.content.time"
                      :min="0"
                      :max="999"
                      size="mini"
                      controls-position="right"
                      placeholder="秒"
                    >
                    </el-input-number>
                  <span style="margin-left: 10px">秒</span>
                </div>
              </span>
            </div>
          </div>
          </el-col>
          <el-col :span="4">
            <span class="card-content" >
            <el-switch
                  v-model="data.status"
                  inline-prompt
                  size="small"
                  @click="switchClick(data)"
                  style="--el-switch-on-color: #53a8ff; --el-switch-off-color: #f56c6c"
                />
            <el-button size="mini" class="el-icon-copy-document"  @click="copyTree(data)" circle style="margin-left: 10px"/>
            <el-button size="mini" class="el-icon-delete" type="danger" @click="delTree(data)" circle />
            </span>
          </el-col>
        </div>
      </el-card>
    </template>
      </el-tree>
      </div>
      </el-scrollbar>
    </el-col>
    </el-row >
    <apiCite v-if="addApiDlg" @childEvent="handleChildData" @close-modal="handleCloseModal"></apiCite>
  	<!-- 调试测试步骤窗口 -->
    <el-drawer v-model="editCaseDlg"   :with-header="false" size="50%"><newEditCase ref="childRef" @closeDrawer="handleClose"  :Interface_id="Interface_id" :copyDlg="copyDlg"  style="padding: 0 10px;"></newEditCase></el-drawer>
    <!-- 显示运行结果 -->
	  <el-drawer v-model="ResultDlg" :with-header="false" size="50%">
		<div style="padding:20px;">
			<el-descriptions title="执行结果" border :column="4" style="text-align: center;">
				<el-descriptions-item label="总数" ><b style="color: #00aaff">{{ runScentResult.all }}</b></el-descriptions-item>
				<el-descriptions-item label="通过"><b style="color: #00aa7f">{{ runScentResult.success }}</b></el-descriptions-item>
				<el-descriptions-item label="失败"><b style="color: orangered">{{ runScentResult.fail }}</b></el-descriptions-item>
				<el-descriptions-item label="错误"><b style="color: #fca130">{{ runScentResult.error }}</b></el-descriptions-item>
			</el-descriptions>
			<div style="height: 40px;line-height: 40px;"><b>执行详情</b></div>
			<el-scrollbar height="calc(100vh - 180px)">
				<el-table :data="runScentResult.cases" style="width: 100%" empty-text="暂无数据">
					<el-table-column type="expand">
						<template #default="props">
							<caseResult :result="props.row"></caseResult>
						</template>
					</el-table-column>
					<el-table-column label="步骤名" prop="name" />
					<el-table-column label="请求方法" prop="method">
            <template #default="props">
               <span v-if="props.row.type === 'api'">{{ props.row.method }}</span>
						</template>
          </el-table-column>
					<el-table-column label="响应状态码" prop="status_cede">
            <template #default="props">
               <span v-if="props.row.type === 'api'">{{ props.row.status_cede }}</span>
						</template>
          </el-table-column>
					<el-table-column label="执行结果" prop="state" min-width="40px">
						<template #default="props">
							<span v-if="props.row.state == '成功'" style="color: #00AA7F;">{{ props.row.state }}</span>
              <span v-else-if="props.row.state == '错误'" style="color: #F56C6C;">{{ props.row.state }}</span>
							<span v-else style="color:#fca130">{{ props.row.state }}</span>
						</template>
					</el-table-column>
				</el-table>
			</el-scrollbar>
		</div>
	</el-drawer>
</template>

<script>
import {mapMutations, mapState} from "vuex";
import {ElMessage, ElNotification} from "element-plus";
import apiCite from '../../views/TestCase/apiCiteDlg.vue';
import newEditCase from '../../components/common/InterfaceNew/neweditCase.vue';
import caseResult from '../../components/common/caseResult.vue';
import Editor from'../../components/common/Editor.vue';
export default {
  components:{
    apiCite,
    newEditCase,
    caseResult,
    Editor
  },
  data() {
    return{
      editForm:{
        name:'',
        project_id:'',
        desc:'',
        stepCount:0,
        creator:''
      },
      rulesCase: {
				name: [
					{
						required: true,
						message: '请输入用例名称',
						trigger: 'blur'
					}
				],
				project_id: [
					{
						required: true,
						message: '请选择项目',
						trigger: 'blur'
					}
				],
			},
      steps:[],
      addApiDlg:false,
      editCaseDlg: false,
      Interface_id: '',
      copyDlg: false,
      ResultDlg:false,
      runScentResult:'',
      ControllerData:{
        name: "",
        type: "",
        content: {},
        script:"",
        desc:"",
        creator:"",
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
      test:'',
      treeKey: '',
      isExpand: false
      }
    },

  computed: {
		...mapState(['pro','case','envId']),
    username() {
			return window.sessionStorage.getItem('username');
		},
    defaultProps() {
      return {
        children: 'children',
        label: 'name',
      }
    },
	},
  watch: {
    steps: {
      deep: true
    }
  },
  methods: {
    ...mapMutations(['CaseInfo','clearCaseInfo']),
  getCardIndex(parent, node) {
    const index = parent.childNodes.indexOf(node);
    return index + 1;
  },

   async addCaseSave() {
    this.$refs.CaseRef.validate(async vaild => {
    // 判断是否验证通过，不通过则直接retrue
    if (!vaild) return;
    const params = {...this.editForm}
    params.creator = this.username
    params.project_id = this.pro.id
    const response = await this.$api.createTestCase(params);
      if (response.status === 201) {
        ElMessage({
          type: 'success',
          message: '保存成功',
          duration: 1000
        });
      }
    })},

   // 保存用例信息
   async editCaseSave() {
    this.$refs.CaseRef.validate(async vaild => {
    // 判断是否验证通过，不通过则直接retrue
    if (!vaild) return;
    const params = {...this.editForm}
    params.project_id = this.pro.id
    params.modifier = this.username;
    params.update_time = this.$tools.newTime()
    delete params.create_time
    delete params.creator
    delete params.project
    const response = await this.$api.updateTestCase(params.id, params);
        if (response.status === 200) {
          ElMessage({
            type: 'success',
            message: '保存成功',
            duration: 1000
          });
        this.editStepSave()
        }
    })
   },

  // 保存步骤信息
  async editStepSave() {
    const ControllerStepsData = this.steps
      .filter(step => step.stepInfo && step.stepInfo.type !== "api")
      .map(step => step);
    const response = await this.$api.updatesStepControll(ControllerStepsData)
      if (response.status === 201) {
        this.getCaseStep(this.case.id)
      }
  },

   reaiTime() {
      if (this.case) {
        this.editForm = this.case;
        this.editForm.project_id = this.pro.name;
      } else {
      this.editForm.project_id = this.pro.name;
      }
   },

   goBack() {
      if (this.case && this.case.back_type) {
      this.$router.push({ name: 'new-testplan' });
      this.clearCaseInfo();
      } else {
        this.$router.push({ name: 'TestCase' });
        this.clearCaseInfo()}
    },
   handleStepClick(data) {
      if (data.stepInfo.type==='api'){
      this.Interface_id = data.interfaceStep
      this.editCaseDlg = true
      this.$nextTick(() => {
        this.$refs.childRef.getInterfaceInfo(this.Interface_id);
          }
        )
      }
      else if(data.stepInfo.type==='script') {
           data.stepInfo.dlg = !data.stepInfo.dlg;
      }
      else if(data.stepInfo.type==='sql'){
        data.stepInfo.dlg = !data.stepInfo.dlg
      }
      else {}
    },
   handleClose() {
      this.addCaseDlg = false;
      this.editCaseDlg = false;
    },
    getRowClassName(row) {
      switch (row) {
        case 'api':
          return '--el-card-border-color:rgb(97, 100, 159);'
        case 'if':
          return '--el-card-border-color:rgb(230, 162, 60);'
        case 'for':
          return '--el-card-border-color:rgb(2, 167, 240);'
        case 'script':
          return '--el-card-border-color:rgb(123, 77, 18);'
        case 'time':
          return '--el-card-border-color:rgb(103, 194, 58);'
        case 'sql':
          return '--el-card-border-color:rgb(120, 56, 135);'
        default:
          return '';
    }
  },
   allowDrop(draggingNode, dropNode,type) {
      // 只有 type 为 api, for, if 的节点可以作为父级节点
      const allowedParentTypes = ['for', 'if'];
      if (!allowedParentTypes.includes(dropNode.data.stepInfo.type)) {
        return type === "prev" || type === "next";

      }else {
        return true
      };
  },
async copyTree(data, parentId = null, isLastCall = true) {
  event.stopPropagation();
  let order_s = this.steps.length > 0 ? this.steps.length + 1 : 1;

  // if (data.parent_id) {
  //       parentId = data.parent_id;
  //   }
  if (data.stepInfo.type === 'api') {
    await this.$api.createTestCaseStep({ case: this.case.id, interfaceStep: data.interfaceStep, sort: order_s, parent_id: parentId });
  } else {
    data.stepInfo.case = this.case.id;
    data.stepInfo.sort = order_s;
    data.stepInfo.parent_id = parentId;
    const Controllerresponse = await this.$api.copyStepControll(data.stepInfo);
    const setpId = Controllerresponse.data.setpId;
    // 递归复制子节点
    if (data.children) {
      let childCalls = data.children.map((child, index) => {
        const isLast = isLastCall && index === data.children.length - 1; // 是否为最后一次调用
        return this.copyTree(child, setpId, isLast); // 递归调用 copyTree 函数
      });
      await Promise.all(childCalls); // 等待所有子节点的递归调用完成
    }
  }

  // 所有递归调用完成后再刷新页面
  if (isLastCall) {
    this.getCaseStep(this.case.id);
  }
},

  async delTree(data) {
    event.stopPropagation();
    if (data.stepInfo.type==='api'){
          const response = await this.$api.delTestCaseStep(data.id);
			if (response.status === 204) {
			    this.getCaseStep(this.case.id)
			}
    }
    else {
      const response = await this.$api.delTestCaseStep(data.id);
			if (response.status === 204) {
			  const res = await this.$api.delStepControll(data.controllerStep);
			  if (res.status === 204){
			    this.getCaseStep(this.case.id)
          }
			}}
  },
  showApiCite() {
   this.$refs.CaseRef.validate(async vaild => {
    // 判断是否验证通过，不通过则直接return
    if (!vaild) return;
    this.addApiDlg = true;})
  },
  handleCloseModal() {
      this.addApiDlg = false; // 关闭弹窗
    },
  async handleChildData(data) {
    let order_s = this.steps.length > 0 ? this.steps.length + 1 : 1;
    let newDataArray = [];
    data.forEach(item => {
      // 遍历data数组中的每个元素，为每个元素创建一个新的对象，其中包含 sort、case 和 interfaceStep 字段
      let newItem = {
        sort: order_s,
        case: this.case.id,
        interfaceStep: item
      };
      newDataArray.push(newItem); // 将新创建的对象添加到新数组中
      order_s++;
    });
    const response = await this.$api.createsTestCaseStep(newDataArray)
      if (response.status === 201) {
          this.getCaseStep(this.case.id)
      }
  },
  async getCaseStep(cases) {
    const response = await this.$api.getTestCaseStep(cases)
        if (response.status === 200) {
        this.steps = response.data
        this.editForm.stepCount = this.steps.length;
        }
  },

  async switchClick() {
    event.stopPropagation();
    this.updateStepOrder()

  },
  async updateStepOrder() {
    const setParentIds = (node, parentId, parentSort) => {
    // 设置父节点的排序字段
    node.sort = parentSort;
    // 如果节点有子节点，则递归设置子节点的 parent_id 和排序字段
    if (node.children && node.children.length > 0) {
        node.children.forEach((child, childIndex) => {
            // 设置子节点的 parent_id 为当前节点的 id
            child.parent_id = node.id;
            // 设置子节点的排序字段
            child.sort = childIndex + 1;
            // 递归调用，处理子节点的子节点
            setParentIds(child, node.id, child.sort);
          });
        }
    };
    // 遍历步骤数组，设置父节点的排序字段和子节点的 parent_id 和排序字段
    this.steps.forEach((parent, parentIndex) => {
        // 设置父节点的排序字段
        parent.sort = parentIndex + 1;
        // 如果父节点有子节点，则设置子节点的 parent_id 和排序字段
        if (parent.children && parent.children.length > 0) {
            // 调用函数设置父节点和子节点的属性
            setParentIds(parent, parent.id, parent.sort);
        }
    });
			// 发送请求后端修改用例顺序
			const response = await this.$api.updateCaseStepOrder(this.steps);
			if (response.status === 200) {
          ElNotification({
              duration: 500,
              title: '调整成功',
              type: 'success',
            })
			}
		},

  // 运行测试用例
  async runCase() {
			if (this.envId) {
				const params = {
					env: this.envId,
					scene: this.case.id
				};
          ElNotification({
            title: '开始运行',
            message: '运行过程中请稍等片刻噢',
            type: 'success',
            duration:1000
          });
				const response = await this.$api.runCases(this.case.id, params);
				if (response.status == 200) {
					// 显示执行结果到窗口页面
					this.runScentResult = response.data;
					this.ResultDlg = true;
				}
			} else {
				this.$message({
					type: 'warning',
					message: '当前未选中执行环境!',
					duration: 1000
				});
			}
		},

  toggleExpand(data) {
    data.dlg = ! data.dlg;
  },

  startEditing(data) {
    if(data.type==='script'){data.inputDlg = true}else {data.inputDlg = true}
    this.$nextTick(() => {
      this.$refs.input.focus();
    });
  },
  cancelEditing(data) {
    data.inputDlg = false;
  },
  addSetUptCodeMod(data,tp) {
			switch (tp) {
				case 'ENV':
					data.script += '\n# 设置全局变量 \nBaseTest().save_global_variable("变量名","变量值")';
					break;
				case 'env':
					data.script += '\n# 设置局部变量  \nBaseTest().save_env_variable("变量名","变量值")';
					break;
				case 'func':
					data.script += '\nfrom apitestengine.core.cases import BaseTest';
					break;
				case 'sql':
					data.script +=
						'\n# ----执行sql语句(需要在环境中配置数据库连接信息)----\n# db.连接名.execute_all(sql语句) \nsql = "SELECT count(*) as count FROM futureloan.member"\nres = db.aliyun.execute_all(sql)';
					break;
			}
		},
  // tree拖动到最顶层或最底层时滚动屏幕
  handleDragScroll() {
    document.addEventListener('mousemove', function(event) {
      const mouseY = event.clientY;
      const elementTop = document.querySelector('.el-tree').getBoundingClientRect().top;

      if (mouseY < 100 && elementTop > 0) {
        window.scrollBy(0, -10);
      } else if (mouseY > window.innerHeight - 100) {
        window.scrollBy(0, 10);
      }
    });
  },

  // 添加条件控制器
  async AddController(types) {
    let order_s = this.steps.length > 0 ? this.steps.length + 1 : 1;
    if(types ==='if'){
      this.ControllerData = {
        name: "条件控制器",
        type: "if",
        content: {
          variable:"",
          JudgmentMode:"",
          value:"",
        },
        script:"",
        desc:"",
        creator:this.username,
      }
    }
    else if(types ==='for'){
        this.ControllerData = {
          name: "循环控制器",
          type: "for",
          content: {
            select:"count",
            cycleIndex:"",
            cycleInterval:"",
            variable:"",
            variableName:""
          },
          script:"",
          desc:"",
          creator:this.username,
      }

    }
    else if(types ==='script'){
      this.ControllerData = {
        name: "自定义脚本",
        type: "script",
        content: {},
        script:"",
        desc:"",
        creator:this.username,
      }
    }
    else if(types ==='time'){
      this.ControllerData = {
        name: "定时控制器",
        type: "time",
        content: {
          time:""
        },
        script:"",
        desc:"",
        creator:this.username,
      }
    }
    else if(types ==='sql'){
      this.ControllerData = {
        name: "数据库操作",
        type: "sql",
        content: {},
        script:"",
        desc:"",
        creator:this.username,
      }
    }else {
      throw new Error('types is not defined');
    }
    const Controllerresponse = await this.$api.createStepControll(this.ControllerData)
      if (Controllerresponse.status === 201) {
            const response = await this.$api.createTestCaseStep({ case: this.case.id, controllerStep:Controllerresponse.data.id, sort: order_s })
              if (response.status === 201) {
                this.getCaseStep(this.case.id)
              }
          }
    },

  rowOpenORFold(isExpand) {
	      this.treeKey = +new Date()
	      this.isExpand = isExpand
	    },

  },
  created() {
    this.reaiTime();
    if (this.case && this.case.id) {
       this.getCaseStep(this.case.id)
    }
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
.el-tree {
    --el-tree-node-hover-background-color: #ecf5ff;
    margin-right: 50px;
}
.tree-component {
  height: 100vh;
  margin-left: 15px;
  padding-right: 10px;
  padding-top: 15px;
  box-shadow: 5px 0 5px rgba(0, 0, 0, 0.06); /* 添加此样式来设置阴影 */
}

/deep/ .el-tree-node__content {
    padding: 4px 4px 4px 0px;
    height: auto;
}

.style {
    line-height: 12px;
    margin-bottom:6px
}
.card-title {
  display: flex;
  width: 1200px;
}
.card-content {
  float:right;
  justify-content: flex-end;
  margin-left: 50px;
  margin-top: -8px;
}

.card-url {
  margin-left: 10px;
  margin-right: 10px;
  font-size: 15px;
}
.card-of {
  margin-right: 10px;
  font-size: 15px;
  font-weight: normal;
}
.card-name {
  font-size: 14px;
}
.el-tag {
  color: #ffffff;
  width: 80px;
  height: 30px;
  text-align: center;
  font-size: 13px;
  line-height: 30px;

}
.icon {
  display: inline-block;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  text-align: center;
  line-height: 28px;
  border: 2px solid;
  margin-left: -10px;
  margin-right: 6px;
  font-weight: normal;
}
.input-def{
  height: 20px;
  width: 180px;
  margin-right: 8px;
}


.el-input--small .el-input__inner {
    height: 27px;
    line-height: 32px;
}

.loop {
  margin: 10px 60px 10px 60px;
}

.script-button{
  color:black;
  border: none;
  outline: none;
  font-size: 15px;
}
.code_mod {
	margin-bottom: 5px;
}
.el-card {
  border-radius: 10px;
}

.stepStyle{
  margin-top: 15px;
  margin-left: 45px;
  margin-bottom: 10px;
  cursor: pointer
}
.custom-button .el-icon {
  margin-top: 10px; /* 调整箭头图标向下的距离 */
}
</style>