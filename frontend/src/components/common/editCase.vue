<template>
	<el-scrollbar height="calc(100vh - 60px);padding-right:30px;">
		<el-divider content-position="left"><b>Api信息</b></el-divider>
		<el-row :gutter="10">
			<el-col :span="18">
				<el-input v-model="caseInfo.interface.url" placeholder="接口地址">
					<template #prepend>
						<el-select v-model="caseInfo.interface.method" placeholder="请求方法" size="small" style="width: 100px;">
							<el-option label="GET" value="GET" />
							<el-option label="POST" value="POST" />
							<el-option label="PUT" value="PUT" />
							<el-option label="PATCH" value="PATCH" />
							<el-option label="DELETE" value="DELETE" />
							<el-option label="OPTION" value="OPTION" />
							<el-option label="HEAD" value="HEAD" />
						</el-select>
					</template>
				</el-input>
			</el-col>
			<el-col :span="6" style="text-align: right;"><el-button @click="runCase" type="success" icon="el-icon-s-promotion">发送</el-button></el-col>

		</el-row>
		<div class="case_info" v-if="caseInfo.id">
			<el-divider content-position="left"><b>用例信息</b></el-divider>
			<el-row>
				<el-col :span="12">
					<el-input v-model="caseInfo.title" placeholder="用例名">
						<template #prepend>
							用例名称
						</template>
					</el-input>
				</el-col>
				<el-col :span="12" style="text-align: right;">
					<el-button v-if='$route.path==="/testStep"' @click="deleteCase" type="danger" icon="el-icon-delete" plain>删除</el-button>
					<el-button v-if='$route.path==="/testStep"' @click="copyCase" type="success" icon="el-icon-document-copy" plain>复制</el-button>
					<el-button @click="saveCase" type="success" icon="el-icon-s-claim" plain>保存</el-button>
				</el-col>
			</el-row>
		</div>
		<el-divider content-position="left"><b>请求信息</b></el-divider>
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
						<el-divider>脚本模板</el-divider>
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
						<el-divider>脚本模板</el-divider>
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
		<div style="height: 20px;"></div>
	</el-scrollbar>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import Editor from './Editor.vue';
import caseResult from './caseResult.vue';
import FromData from './FormData.vue'
import { ElMessage, ElMessageBox } from 'element-plus';
export default {
	components: {
		Editor,
		caseResult,
		FromData
	},
	data() {
		return {
			caseInfo: {
				interface: {
					method: 'POST',
					url: ''
				},
				title: '接口用例',
				headers: {},
				request: { json: { pwd: 'xxxxx', mobile_phone: 'xxxxxxxx' } },
				file: [],
				setup_script: '',
				teardown_script: ''
			},
			paramType: 'json',
			json: '{}',
			data: '{}',
			params: '{}',
			headers: '{}',
      interfaceparams: '{}',
			file: [],
			runResult: null
		};
	},
	computed: {
		...mapState(['interfaces', 'envId'])
	},
	props: ['step'],
	methods: {
		...mapActions(['getAllInter']),
		// 删除用例
		deleteCase() {
			ElMessageBox.confirm('确定要删除该用例吗?', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning'
			})
				.then(async () => {
					const response = await this.$api.delTeststep(this.caseInfo.id);
					if (response.status === 204) {
						ElMessage({
							type: 'success',
							message: '删除成功',
							duration: 1000
						});
						this.getAllInter();
					}
				})
				.catch(() => {
					ElMessage({
						type: 'info',
						message: '取消删除',
						duration: 1000
					});
				});
		},
		// 修改用例
		async saveCase() {
			// 获取编辑后的数据
			const params = this.getEditData();
			const par = this.getInerfaceData();
			// 发送请求
			const response = await this.$api.updateTeststep(this.caseInfo.id, params);
			if (response.status === 200) {
        const UpdateInterfaceApi = await this.$api.updateInterface(par.id, par);
        if (UpdateInterfaceApi.status === 200) {
          			ElMessage({
                  type: 'success',
                  message: '保存成功',
                  duration: 1000
				          });
        }
        this.getStepInfo(this.caseInfo.id)
        this.getAllInter()
			}
		},
		// 复制用例
		async copyCase() {
			// 获取编辑后的数据
			const params = this.getEditData();
			params.title = params.title + '_副本';
			// 发送请求
			const response = await this.$api.createTeststep(params);
			if (response.status === 201) {
				ElMessage({
					type: 'success',
					message: '复制成功',
					duration: 1000
				});
				this.getAllInter();
			}
		},
		// 运行用例
		async runCase() {
		  if (!this.envId) {
        this.$message({
					type: 'warning',
					message: '当前未选中执行环境!',
					duration: 1000
				});
        return
      };
			const runData = this.getEditData();
			runData.interface = {
				url: this.caseInfo.interface.url,
				method: this.caseInfo.interface.method
			};
			const params = {
				data: runData,
				env: this.envId
			};
			const response = await this.$api.runCase(params);
			if (response.status === 200) {
				this.runResult = response.data;
				ElMessage({
					type: 'success',
					message: '执行完毕',
					duration: 1000
				});
			}
		},
		// 获取测试用例的详细信息
		async getStepInfo(id) {
			const response = await this.$api.getTestStepInfo(id);
			this.runResult = null;
			if (response.status === 200) {
				this.caseInfo = { ...response.data };
				this.json = JSON.stringify(this.caseInfo.request.json || {}, null, 4);
				this.data = JSON.stringify(this.caseInfo.request.data || {}, null, 4);
				this.params = JSON.stringify(this.caseInfo.request.params || {}, null, 4);
				this.headers = JSON.stringify(this.caseInfo.headers || {}, null, 4);
				this.file = this.caseInfo.file ;
			}
		},
		// 获取编辑后的用例数据
		getEditData() {
			let caseData = { ...this.caseInfo };
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
          caseData.request = { json: JSON.parse(this.json) };
          caseData.request.data = null;
          caseData.file = [];

        }catch (e) {
          this.$message({
              message: "提交的application/json数据json格式错误，请检查！",
              type: 'warning',
              duration: 1000
            });
      return null;
        }
			} else if (this.paramType === 'data') {
			    try {
            caseData.request = { data: JSON.parse(this.data) };
            caseData.request.json = null
            caseData.file = []
          }catch (e) {
            this.$message({
                message: "提交的x-www-form-urlencoded数据json格式错误，请检查！",
                type: 'warning',
                duration: 1000
              });
          return null;
        }
			} else if (this.paramType === 'formData') {
				caseData.file =  this.file ;
        caseData.request = {}
			}
			 try {
          caseData.request.params = JSON.parse(this.params);
          caseData.interface = this.caseInfo.interface.id;
          return caseData;
          }catch (e) {
            this.$message({
                message: "提交的Params数据json格式错误，请检查！",
                type: 'warning',
                duration: 1000
              });
          return null;
        }
		},
    getInerfaceData() {
		  let InerfaceData = {...this.caseInfo};
		  let json_data = InerfaceData.interface
      return json_data


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
		}
	},
	watch: {
		step(val) {
			if (val) {
				// 发送请求获取用例详细数据
				this.getStepInfo(val);
			}
		}
	},
	created() {
		if (this.step) {
			this.getStepInfo(this.step);
		}
	}
};
</script>

<style scoped>
.code_mod {
	margin-bottom: 5px;
}
</style>
