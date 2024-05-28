<template>
	<el-row :gutter="10">
		<el-col :span="4">
			<div class="data_box">
          <el-tabs type="border-card" stretch>
					<el-tab-pane label="测试环境">
          </el-tab-pane>
          </el-tabs>
				<el-button @click="addEnv" type="success" plain size="mini" style="width: 100%;" icon="el-icon-plus">添加测试环境</el-button>
				<el-scrollbar height="calc(100vh - 124px);">
					<el-menu :default-active="active" class="el-menu-vertical-demo" active-text-color="#409eff" text-color="#000000" style="background: none;border: none;">
						<el-menu-item  @click='selectEnv(item)' :index="item.id.toString()" v-for="item in testEnvs" style="height: 35px;line-height: 35px;">
							<span class="el-icon-coin"></span>
							<span>{{ item.name }}</span>
						</el-menu-item>
					</el-menu>
				</el-scrollbar>
			</div>
		</el-col>
		<el-col :span="8" v-if="EnvInfo">
			<el-scrollbar height="calc(100vh - 80px )">
				<el-divider content-position="left"><b>基本信息</b></el-divider>
				<el-input v-model="EnvInfo.name" placeholder="环境名称" size="mini">
					<template #prepend>
						环境名
					</template>
				</el-input>
				<el-input v-model="EnvInfo.host" placeholder="hots地址" size="mini" style="margin-top: 5px;">
					<template #prepend>
						服务器域名
					</template>
				</el-input>
				<el-divider content-position="left"><b>基本配置</b></el-divider>
				<el-tabs type="border-card" class="demo-tabs">
					<el-tab-pane label="全局请求头"><Editor v-model="EnvInfo.headers" height="250px"></Editor></el-tab-pane>
					<el-tab-pane label="数据库配置"><Editor v-model="EnvInfo.db" height="250px"></Editor></el-tab-pane>
				</el-tabs>
				<el-divider content-position="left"><b>全局变量</b></el-divider>
				<el-tabs type="border-card" class="demo-tabs">
					<el-tab-pane label="全局变量"><Editor v-model="EnvInfo.global_variable" height="250px"></Editor></el-tab-pane>
					<el-tab-pane label="调试运行变量"><Editor v-model="EnvInfo.debug_global_variable" height="250px"></Editor></el-tab-pane>
				</el-tabs>
				<div :offset="20" style="text-align: center;margin-top: 5px" v-if="EnvInfo">
					<el-button @click='saveEnv' type="success" plain icon="el-icon-circle-check">保存编辑</el-button>
					<el-button @click='copyEnv' type="success" plain icon="el-icon-circle-check">复制环境</el-button>
					<el-button @click="delEnv" type="danger" plain icon="el-icon-delete">删除环境</el-button>
				</div>
			</el-scrollbar>
		</el-col>
		<el-col :span="12" v-if="EnvInfo"><Editor v-model="EnvInfo.global_func" height="calc(100vh - 65px)" lang="python" theme="monokai"></Editor></el-col>
    <el-col class="container" :span="20" v-if="this.testEnvs.length===0">
      <el-empty>
          <el-button type="primary" @click="addEnv">添加测试环境</el-button>
      </el-empty>
    </el-col>
  </el-row>
</template>

<script>
/*
功能实现:
	测试环境的增删查改
*/ 
import { mapState, mapActions } from 'vuex';
import DataList from '../components/common/DataList.vue';
import Editor from '../components/common/Editor.vue';
import { ElMessage, ElMessageBox } from 'element-plus';
export default {
	components: {
		DataList,
		Editor
	},
	data() {
		return {
			active: '1',
			EnvInfo: null,
		};
	},
	computed: {
		...mapState(['pro', 'testEnvs'])
	},
	methods: {
		...mapActions(['getAllEnvs']),
		// 创建环境
		async addEnv() {
			const params = {project :this.pro.id,name:"New Env"}
			const response = await this.$api.createTestEnvs(params);
			if (response.status === 201) {
				this.$message({
					type: 'success',
					message: '添加成功',
					duration: 1000
				});
				this.getAllEnvs();
			}
		},
		// 删除环境
		async delEnv() {
			ElMessageBox.confirm('确定要删除吗?', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning'
			})
				.then(async () => {
					const response = await this.$api.delTestEnvs(this.EnvInfo.id);
					if (response.status === 204) {
						ElMessage({
							type: 'success',
							message: '删除成功',
							duration: 1000
						});
						this.getAllEnvs();
						// 重新选中环境
						if (this.testEnvs.length > 0) {
							// 设置默认显示激活的测试场景
							this.active = this.testEnvs[0].id.toString();
							this.selectEnv(this.testEnvs[0]);
						}
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

		// 保存修改
		async saveEnv(){
			let params = {...this.EnvInfo}
			params.headers = JSON.parse(this.EnvInfo.headers);
			params.db = JSON.parse(this.EnvInfo.db);
			params.debug_global_variable = JSON.parse(this.EnvInfo.debug_global_variable);
			params.global_variable = JSON.parse(this.EnvInfo.global_variable);
			const response = await this.$api.updateTestEnvs(params.id,params)
			if (response.status === 200) {
				this.$message({
					type: 'success',
					message: '保存成功',
					duration: 1000
				});
				this.getAllEnvs();
			}
		},
		// 复制环境
		async copyEnv(){
			let params = {...this.EnvInfo}
			params.name = params.name +'_COPY'
			params.headers = JSON.parse(this.EnvInfo.headers);
			params.db = JSON.parse(this.EnvInfo.db);
			params.debug_global_variable = JSON.parse(this.EnvInfo.debug_global_variable);
			params.global_variable = JSON.parse(this.EnvInfo.global_variable);
			const response = await this.$api.createTestEnvs(params);
			if (response.status === 201) {
				this.$message({
					type: 'success',
					message: '复制成功',
					duration: 1000
				});
				this.getAllEnvs();
			}
		},
		// 选中环境
		selectEnv(env) {
			this.active = env.id.toString()
			this.EnvInfo = { ...env };
			this.EnvInfo.headers = JSON.stringify(this.EnvInfo.headers, null, 4);
			this.EnvInfo.db = JSON.stringify(this.EnvInfo.db, null, 4);
			this.EnvInfo.debug_global_variable = JSON.stringify(this.EnvInfo.debug_global_variable, null, 4);
			this.EnvInfo.global_variable = JSON.stringify(this.EnvInfo.global_variable, null, 4);
		}
	},
	created() {
		this.getAllEnvs();
	},
	mounted() {
		if (this.testEnvs.length > 0) {
			// 设置默认选中的测试场景
			this.selectEnv(this.testEnvs[0]);
		}
	}
};
</script>

<style scoped>
.data_box {
	box-shadow: 0 0 5px #dcdfe6;
}
.title {
	text-align: center;
	font: bold 16px/30px 'microsoft yahei';
	height: 30px;
}
.container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 70vh;
  }
</style>
