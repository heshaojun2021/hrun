<template>
  <el-scrollbar height="calc(100vh);padding-right:10px;">
  <div style="margin: 10px" >
  <el-divider content-position="left" style="margin-bottom: 30px"><b>Api信息</b></el-divider>
  <el-form :rules="rulesinterface" ref="interfaceRef" :model="caseInfo">
    <!--    复制的操作功能-->
    <el-row v-if="copyDlg===true" :gutter="10" style="margin-bottom: 20px">
    <el-col :span="15">
      <el-form-item prop="url">
          <el-input v-model="caseInfo.url" placeholder="请输入接口地址">
            <template #prepend >
              <el-select v-model="caseInfo.method" placeholder="请求类型" size="small" style="width: 96px;color: black">
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
    <el-col :span="9" style="text-align: right;">
      <el-button @click="runCase" type="success" icon="el-icon-s-promotion">调试</el-button>
      <el-button @click="editClick" type="primary" icon="el-icon-edit-outline">保存</el-button>
      <el-button @click="copyCases" type="primary" icon="el-icon-copy-document">复制</el-button>
    </el-col>
    </el-row>
    <!--    调试的操作功能-->
    <el-row v-else :gutter="10" style="margin-bottom: 20px">
    <el-col :span="18">
      <el-form-item prop="url">
          <el-input v-model="caseInfo.url" placeholder="请输入接口地址">
            <template #prepend >
              <el-select v-model="caseInfo.method" placeholder="请求类型" size="small" style="width: 96px;color: black">
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
      <el-button @click="runCase" type="success" icon="el-icon-s-promotion">调试</el-button>
      <el-button @click="editClick" type="primary" icon="el-icon-edit-outline">保存</el-button>
    </el-col>
    </el-row>
    <el-row :gutter="24" style="margin-bottom: 20px">
    <el-col :span="7">
      <el-form-item label="节点/模块">
        <el-cascader
            v-model="caseInfo.treenode"
            :options="options"
            :props="{label:'name', value:'id',checkStrictly: true}"
            @change="removeCascaderAriaOwns"
            @visible-change="removeCascaderAriaOwns"
            @expand-change="removeCascaderAriaOwns"
            clearable
            change-on-select
            filterable
        />
      </el-form-item>
    </el-col>
    <el-col :span="9">
      <el-form-item label="接口名称" prop="name" >
        <el-input v-model="caseInfo.name" placeholder="请输入接口名称" clearable style="width: 200px"/>
      </el-form-item>
    </el-col>
    <el-col :span="8">
    <el-form-item label="导入数据是否锁定">
      <el-select v-model="selectedStatus" placeholder="请选择">
        <el-option label="已锁定" value="1"></el-option>
        <el-option label="无需锁定" value="0"></el-option>
      </el-select>
    </el-form-item>
    </el-col>
    <el-col :span="12">
      <el-form-item label="描述">
        <el-input v-model="caseInfo.desc"  type="textarea" clearable style="width: 350px"/>
      </el-form-item>
    </el-col>
    <el-col :span="12">
    <el-scrollbar height="60px">
      <el-form-item label="接口标签">
      <el-tag
        v-for="tag in caseInfo.interface_tag"
        :key="tag"
        size="small"
        :type="getRandomType()"
        closable
        :disable-transitions="false"
        style="margin-right: 5px"
        @close="removeTag(tag)"
        effect="light"
      >{{ tag }}</el-tag>
      <el-input
        v-if="state.editTag"
        ref="caseTagInputRef"
        v-model="state.tagValue"
        size="small"
        @keyup.enter="addTag"
        @blur="addTag"
        style="width: 100px"
        maxlength="30"
      />
      <el-button v-else size="small" @click="showEditTag">+ New Tag</el-button>
    </el-form-item>
    </el-scrollbar>
  </el-col>
    <el-col :span="5">
    <el-form-item label="创建用户："  style="margin-top: 10px;">
      <a>{{this.caseInfo.creator}}</a>
    </el-form-item>
    </el-col>
    <el-col :span="7">
    <el-form-item label="创建时间："  style="margin-top: 10px;">
    <template #default="scope">
      <a>{{ $tools.rTime(this.caseInfo.create_time) }}</a>
    </template>
    </el-form-item>
    </el-col>
    <el-col :span="5">
    <el-form-item label="修改用户："  style="margin-top: 10px;">
      <a>{{this.caseInfo.modifier}}</a>
    </el-form-item>
    </el-col>
    <el-col :span="7">
    <el-form-item label="修改时间："   style="margin-top: 10px;">
      <template #default="scope">
        <a v-if="this.caseInfo.update_time">{{$tools.rTime(this.caseInfo.update_time)}}</a>
      </template>
    </el-form-item>
    </el-col>
  </el-row>
  </el-form>
  <el-divider content-position="left" style="margin-top: 0px"><b>请求信息</b></el-divider>
    <!-- ace编辑器 -->
		<el-tabs type="border-card" style="min-height: 370px;" >
			<el-tab-pane label="请求头(headers)"><Editor v-model="headers"></Editor></el-tab-pane>
			<el-tab-pane label="查询参数(Params)"><Editor v-model="params"></Editor></el-tab-pane>
			<el-tab-pane label="请求体(Body)">
				<el-radio-group v-model="paramType" style="margin-bottom: 5px;">
					<el-radio label="json">application/json</el-radio>
					<el-radio label="data">x-www-form-urlencoded</el-radio>
					<el-radio label="formData">form-data</el-radio>
				</el-radio-group>
				<div v-if="paramType === 'json'"><Editor v-model="json"></Editor></div>
				<div v-else-if="paramType === 'data'"><Editor v-model="data"></Editor></div>
				<div v-else-if="paramType === 'formData'">
					<FromData v-model="file"></FromData>
				</div>
			</el-tab-pane>
			<el-tab-pane label="前置脚本">
				<el-row :gutter="10">
					<el-col :span="18"><Editor v-model="caseInfo.setup_script" lang="python" theme="monokai"></Editor></el-col>
					<el-col :span="6">
						<el-divider style="width:195px">脚本模板</el-divider>
						<div class="code_mod"><el-button type="success" size="mini" plain @click="addSetUptCodeMod('ENV')">预设全局变量</el-button></div>
						<div class="code_mod"><el-button type="success" size="mini" plain @click="addSetUptCodeMod('env')">预设局部变量</el-button></div>
						<div class="code_mod"><el-button type="success" size="mini" plain @click="addSetUptCodeMod('func')">调用全局函数</el-button></div>
						<div class="code_mod"><el-button type="success" size="mini" plain @click="addSetUptCodeMod('sql')">执行sql查询</el-button></div>
					</el-col>
				</el-row>
			</el-tab-pane>
			<el-tab-pane label="后置脚本">
				<el-row :gutter="10">
					<el-col :span="18"><Editor v-model="caseInfo.teardown_script" lang="python" theme="monokai"></Editor></el-col>
					<el-col :span="6">
						<el-divider style="width:195px">脚本模板</el-divider>
						<el-scrollbar height="250px">
							<div class="code_mod"><el-button type="success" size="mini" plain @click="addTearDownCodeMod('getBody')">获取响应体</el-button></div>
							<div class="code_mod"><el-button type="success" size="mini" plain @click="addTearDownCodeMod('JSextract')">jsonpath提取数据</el-button></div>
							<div class="code_mod"><el-button type="success" size="mini" plain @click="addTearDownCodeMod('REextract')">正则提取数据</el-button></div>
							<div class="code_mod"><el-button type="success" size="mini" plain @click="addTearDownCodeMod('ENV')">设置全局变量</el-button></div>
							<div class="code_mod"><el-button type="success" size="mini" plain @click="addTearDownCodeMod('env')">设置局部变量</el-button></div>
							<div class="code_mod"><el-button type="success" size="mini" plain @click="addTearDownCodeMod('func')">调用全局函数</el-button></div>
							<div class="code_mod"><el-button type="success" size="mini" plain @click="addTearDownCodeMod('sql')">执行sql查询</el-button></div>
							<div class="code_mod"><el-button type="success" size="mini" plain @click="addTearDownCodeMod('http')">断言HTTP状态码</el-button></div>
							<div class="code_mod"><el-button type="success" size="mini" plain @click="addTearDownCodeMod('eq')">断言相对</el-button></div>
							<div class="code_mod"><el-button type="success" size="mini" plain @click="addTearDownCodeMod('contain')">断言包含</el-button></div>
						</el-scrollbar>
					</el-col>
				</el-row>
			</el-tab-pane>
		</el-tabs>
		<div v-if="runResult">
			<el-divider content-position="left"><b>执行结果</b></el-divider>
			<caseResult :result="runResult"></caseResult>
    </div>
  </div>
  </el-scrollbar>
</template>

<script>
import caseResult from '@/components/common/caseResult.vue';
import FromData from '@/components/common/FormData.vue'
import Editor from "@/components/common/Editor";
import {mapState} from "vuex";
import {ElMessage,ElNotification} from "element-plus";
export default {
  props: ['Interface_id','copyDlg'],
  components: {
    caseResult,
    FromData,
    Editor
  },
  data() {
    return {
      rulesinterface: {
        // 验证名称是否合法
        name: [
          {
            required: true,
            message: '请输入接口名称',
            trigger: 'blur'
          }
        ],
        // 验证url是否合法
        url: [
          {
            required: true,
            message: '请输入接口信息',
            trigger: 'blur'
          }
        ]
      },
      addForm: {},
      state: {
        form: {
          item: [
            {type: ''},
            {type: 'success'},
            {type: 'info'},
            {type: 'danger'},
            {type: 'warning'}
          ]
        },
        editTag: false, // 标记是否处于编辑状态
        tagValue: '', // 输入框中的值
      },
      options: [],
      caseInfo: {
        method: 'POST',
        interface_tag: [],
        YApi_status:'',
        url: '',
        name: '',
        treenode: this.treeId,
        creator: '',
        modifier: '',
        desc: '',
        headers: {},
        request: {"json": {}, "data": null, "params": {}},
        file: [],
        setup_script: '# 前置脚本(python):\n' +
            '# global_tools:全局工具函数\n' +
            '# data:用例数据 \n' +
            '# env: 局部环境\n' +
            '# ENV: 全局环境\n' +
            '# db: 数据库操作对象',
        teardown_script: '# 后置脚本(python):\n' +
            '# global_tools:全局工具函数\n' +
            '# data:用例数据 \n' +
            '# response:响应对象response \n' +
            '# env: 局部环境\n' +
            '# ENV: 全局环境\n' +
            '# db: 数据库操作对象'
      },
      paramType: 'json',
      json: '{}',
      data: '{}',
      params: '{}',
      headers: '{}',
      interfaceparams: '{}',
      file: [],
      interface_tag: [],
      runResult: "",
    }
  },
  computed: {
    ...mapState(['pro', 'envId']),
  username() {
			return window.sessionStorage.getItem('username');
		},
   selectedStatus: {
      get() {
        // 根据 caseInfo.YApi_status 的值返回对应的文案
        if (this.caseInfo.YApi_status == 1) {
          return '1'; // 已锁定
        } else {
          return '0'; // 无需锁定
        }
      },
      set(value) {
        // 设置 caseInfo.YApi_status 的值
        this.caseInfo.YApi_status = value;
      }
    }

  },
  methods: {
    // 标签功能点击自动聚焦
    focusInput() {
      this.$nextTick(() => {
        this.$refs.caseTagInputRef.focus();
      });
    },
    // 新增标签
    addTag() {
      if (this.state.editTag && this.state.tagValue) {
        if (!this.caseInfo.interface_tag) this.caseInfo.interface_tag = [];
        this.caseInfo.interface_tag.push(this.state.tagValue);
        this.focusInput();
      }
      this.state.editTag = false;
      this.state.tagValue = '';
    },

    // 删除标签
    removeTag(tag) {
      this.caseInfo.interface_tag.splice(this.caseInfo.interface_tag.indexOf(tag), 1);
    },

    // 确定保存标签
    showEditTag() {
      this.state.editTag = true;
      this.focusInput();
    },
    // 随机创建不一样type的标签
    getRandomType() {
      const randomIndex = Math.floor(Math.random() * this.state.form.item.length);
      return this.state.form.item[randomIndex].type;
    },

    // 树结构列表接口
    async allTree() {
      const response = await this.$api.gettreeNode()
      if (response.status === 200) {
        this.options = response.data.result
      }
    },

    // 解决el-cascader组件页面卡顿问题
    removeCascaderAriaOwns() {
      this.$nextTick(() => {
        const $el = document.querySelectorAll(
            '.el-cascader-panel .el-cascader-node[aria-owns]'
        );
        Array.from($el).map(item => item.removeAttribute('aria-owns'));
      });
    },

    // 生成前置脚本的方法
    addSetUptCodeMod(tp) {
      switch (tp) {
        case 'ENV':
          this.caseInfo.setup_script += '\n# 设置全局变量 \ntest.save_global_variable("变量名","变量值")';
          break;
        case 'env':
          this.caseInfo.setup_script += '\n# 设置局部变量  \ntest.save_env_variable("变量名","变量值")';
          break;
        case 'func':
          this.caseInfo.setup_script += '\n# 调用全局工具函数random_mobile随机生成一个手机号码  \nmobile = global_func.random_mobile()';
          break;
        case 'sql':
          this.caseInfo.setup_script +=
              '\n# ----执行sql语句(需要在环境中配置数据库连接信息)----\n# db.连接名.execute_all(sql语句) \nsql = "SELECT count(*) as count FROM futureloan.member"\nres = db.aliyun.execute_all(sql)';
          break;
      }
    },
    // 生成后置脚本的方法
    addTearDownCodeMod(tp) {
      switch (tp) {
        case 'getBody':
          this.caseInfo.teardown_script += '\n# Demo:获取响应体(json)  \nbody = response.json()';
          this.caseInfo.teardown_script += '\n# Demo2:获取响应体(字符串)  \nbody = response.text';
          break;
        case 'JSextract':
          this.caseInfo.teardown_script += '\n# Demo:jsonpath提取response中的msg字段  \nmsg = test.json_extract(response.json(),"$..msg")';
          break;
        case 'REextract':
          this.caseInfo.teardown_script += '\n# Demo:正则提取响应体中的数据  \nres = test.re_extract(response.text,"正则表达式",)';
          break;
        case 'ENV':
          this.caseInfo.teardown_script += '\n# 设置全局变量 \ntest.save_global_variable("变量名","变量值")';
          break;
        case 'env':
          this.caseInfo.teardown_script += '\n# 设置局部变量  \ntest.save_env_variable("变量名","变量值")';
          break;
        case 'func':
          this.caseInfo.teardown_script += '\n# 调用全局工具函数random_mobile随机生成一个手机号码  \nmobile = global_func.random_mobile()';
          break;
        case 'sql':
          this.caseInfo.teardown_script +=
              '\n# ----执行sql语句(需要在环境中配置数据库连接信息)----\n# db.连接名.execute_all(sql语句) \nsql = "SELECT count(*) as count FROM futureloan.member"\nres = db.aliyun.execute_all(sql)';
          break;
        case 'http':
          this.caseInfo.teardown_script += '\n# 断言http状态码 \n# Demo:断言http状态码是否为200  \ntest.assertion("相等",200,response.status_code)';
          break;
        case 'eq':
          this.caseInfo.teardown_script += '\n# 断言相等 \ntest.assertion("相等","预期结果","实际结果")';
          break;
        case 'contain':
          this.caseInfo.teardown_script += '\n# 断言包含:预期结果中的内容在实际结果中是否存在 \ntest.assertion("包含","预期结果","实际结果")';
          break;
      }
    },

    // 获取测试用例的详细信息
    async getInterfaceInfo(id) {
      const response = await this.$api.getnewInterface(id);
      this.runResult = null;
      if (response.status === 200) {
        this.caseInfo = {...response.data};
        this.json = JSON.stringify(this.caseInfo.request.json || {}, null, 4);
        this.data = JSON.stringify(this.caseInfo.request.data || {}, null, 4);
        this.params = JSON.stringify(this.caseInfo.request.params || {}, null, 4);
        this.headers = JSON.stringify(this.caseInfo.headers || {}, null, 4);
        this.caseInfo.interface_tag = Array.from(this.caseInfo.interface_tag.tag);
        this.file = this.caseInfo.file;
      }
    },

    //  组装接口的数据
    getEditData() {
      let caseData = {...this.caseInfo};
      delete caseData.status
      // 获取最后一个节点的id
      if (caseData.treenode && caseData.treenode.length > 0) {  // 检查列表是否存在且不为空
        const lastValue = caseData.treenode[caseData.treenode.length - 1];  // 获取最后一个值
        console.log(lastValue);  // 输出最后一个值
        caseData.treenode = lastValue
      } else {
        console.log('列表为空');  // 如果列表为空，输出提示信息
      }
      // tag标签改成interface_tag:{tag:[值1,值2]}
      caseData.interface_tag = {tag: [...caseData.interface_tag]};
      caseData.modifier = this.username;
      caseData.update_time = this.$tools.newTime()
      try {
        caseData.headers = JSON.parse(this.headers);
      } catch (e) {
        this.$message({
          message: '提交的headers数据 json格式错误，请检查！',
          type: 'warning',
          duration: 1000
        });
        return null;
      }
      // 请求体格式的选择
      if (this.paramType === 'json') {
        try {
          caseData.request = {json: JSON.parse(this.json)};
          caseData.request.data = null;
          caseData.file = [];

        } catch (e) {
          this.$message({
            message: "提交的application/json数据json格式错误，请检查！",
            type: 'warning',
            duration: 1000
          });
          return null;
        }
      } else if (this.paramType === 'data') {
        try {
          caseData.request = {data: JSON.parse(this.data)};
          caseData.request.json = null
          caseData.file = []
        } catch (e) {
          this.$message({
            message: "提交的x-www-form-urlencoded数据json格式错误，请检查！",
            type: 'warning',
            duration: 1000
          });
          return null;
        }
      } else if (this.paramType === 'formData') {
        caseData.file = this.file;
        caseData.request = {}
      }
      try {
        caseData.request.params = JSON.parse(this.params);
        // caseData.interface = this.caseInfo.interface.id;
        return caseData;
      } catch (e) {
        this.$message({
          message: "提交的Params数据json格式错误，请检查！",
          type: 'warning',
          duration: 1000
        });
        return null;
      }

    },


    // 修改接口
    async editClick() {
      this.$refs.interfaceRef.validate(async vaild => {
        // 判断是否验证通过，不通过则直接return
        if (!vaild) return;
        const params = this.getEditData();
        const response = await this.$api.updatenewInterface(this.Interface_id, params);
        if (response.status === 200) {
          ElMessage({
            type: 'success',
            message: '修改成功',
            duration: 1000
          });
        }
        // 关闭Drawer窗口
        // this.$emit('closeDrawer');
      })
    },

    // 运行用例
    async runCase() {
      console.log(this.copyDlg)
      if (!this.envId) {
        this.$message({
          type: 'warning',
          message: '当前未选中执行环境!',
          duration: 1000
        });
        return
      }
      this.$refs.interfaceRef.validate(async vaild => {
        // 判断是否验证通过，不通过则直接return
        if (!vaild) return;
        const runData = this.getEditData();
        runData.interface = {
          url: this.caseInfo.url,
          method: this.caseInfo.method
        };
        const params = {
          data: runData,
          env: this.envId
        };
        const response = await this.$api.runNewCase(params);
        if (response.status === 200) {
          this.runResult = response.data;
          ElNotification({
              duration: 500,
              title: '成功',
              type: 'success',
            })
        }
      })
    },

    // 复制用例
    async copyCases() {
    // 获取编辑后的数据
    const params = this.getEditData();
    params.name = params.name + '_副本';
    params.creator = this.username;
    params.modifier = '';
    params.update_time = null;
    // 发送请求
    const response = await this.$api.createnewInterface(params);
    if (response.status === 201) {
      ElMessage({
        type: 'success',
        message: '复制成功',
        duration: 1000
      });
    }
  },

  },

created() {
    this.allTree();
  },

}
</script>

<style scoped>
.code_mod {
	margin-bottom: 5px;
}
</style>