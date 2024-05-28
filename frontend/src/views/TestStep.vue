<template>
	<el-row :gutter="10">
		<!-- 左边内容 -->
		<el-col :span="5">
			<div class="data_box">
				<el-tabs type="border-card" stretch>
					<el-tab-pane label="项目接口">
						<el-button @click="$router.push({ name: 'interface' })" type="success" plain  style="width: 100%;" icon="el-icon-paperclip">接口管理</el-button>
						<el-scrollbar height="calc(100vh - 130px);">
							<el-menu class="el-menu-vertical-demo" active-text-color="#409eff" text-color="#000000" style="background: none;border: none;margin-top: 5px">
                <el-submenu :index="item.id.toString()" v-for="item in interfaces1" style="margin-bottom: 6px;">
									<template #title>
                    <div style="font-weight: bold">
                      <span v-if="item.method === 'POST'" >
                        <el-tag  color="#49cc90">{{ item.method }}</el-tag>
                        {{ item.name }}
                      </span>
                    <span v-if="item.method === 'GET'">
                      <el-tag  color="#61affe" >{{ item.method}}</el-tag>
                      {{ item.name }}
                    </span>
                    <span v-if="item.method === 'PUT'">
                      <el-tag  color="#fca130" >{{ item.method}}</el-tag>
                      {{ item.name }}
                    </span>
                    <span v-if="item.method === 'PATCH'">
                      <el-tag   color="#50e3c2" >{{ item.method}}</el-tag>
                      {{ item.name }}
                    </span>
                    <span v-if="item.method === 'DELETE'">
                      <el-tag  color="#f93e3e" >{{ item.method}} </el-tag>
                      {{ item.name }}
                    </span>
                    <span v-if="item.method === 'DEAD'">
                      <el-tag color="rgb(201, 233, 104)">{{ item.method}}</el-tag>
                      {{ item.name }}
                    </span>
                    </div>
									</template>

									<el-menu-item :index="item.id.toString() + step.id.toString()" v-for="step in item.steps" @click="stepId = step.id" style="padding-left: 25px">
										<span class="el-icon-link"></span>
										<span>{{ step.title }}</span>
									</el-menu-item>
									<el-menu-item :index="item.id.toString()" @click="clickAdd(item.id)" style="padding-left: 25px" >
										<div style="color: #ffaa00;">
											<span class="el-icon-circle-plus-outline"></span>
											<span>添加用例</span>
										</div>
									</el-menu-item>
								</el-submenu>
							</el-menu>
						</el-scrollbar>
					</el-tab-pane>
					<el-tab-pane label="外部接口">
						<el-button @click="$router.push({ name: 'interface' })" type="success" plain  style="width: 100%;" icon="el-icon-paperclip">接口管理</el-button>
						<el-scrollbar height="calc(100vh - 130px);">
							<el-menu class="el-menu-vertical-demo" active-text-color="#00aa7f" text-color="#000000" style="background: none;border: none;">
								<el-submenu :index="item.id.toString()" v-for="item in interfaces2">
									<template #title>
                    <div style="font-weight: bold">
                      <span v-if="item.method === 'POST'" >
                        <el-tag  color="#49cc90" >{{ item.method }}</el-tag>
                        {{ item.name }}
                      </span>
                    <span v-if="item.method === 'GET'">
                      <el-tag  color="#61affe" >{{ item.method}}</el-tag>
                      {{ item.name }}
                    </span>
                    <span v-if="item.method === 'PUT'">
                      <el-tag  color="#fca130" >{{ item.method}}</el-tag>
                      {{ item.name }}
                    </span>
                    <span v-if="item.method === 'PATCH'">
                      <el-tag   color="#50e3c2" >{{ item.method}}</el-tag>
                      {{ item.name }}
                    </span>
                    <span v-if="item.method === 'DELETE'">
                      <el-tag  color="#f93e3e" >{{ item.method}} </el-tag>
                      {{ item.name }}
                    </span>
                    <span v-if="item.method === 'DEAD'">
                      <el-tag   color="rgb(201, 233, 104)" >{{ item.method}}</el-tag>
                      {{ item.name }}
                    </span>
                   </div>
									</template>
									<el-menu-item  :index="item.id.toString() + step.id.toString()" v-for="step in item.steps" @click="stepId = step.id" style="padding-left: 25px">
										<span class="el-icon-link"></span>
										<span>{{ step.title }}</span>
									</el-menu-item>
									<el-menu-item :index="item.id.toString()" @click="clickAdd(item.id)" style="padding-left: 25px">
										<div style="color: #ffaa00;">
											<span class="el-icon-circle-plus-outline"></span>
											<span>添加用例</span>
										</div>
									</el-menu-item>
								</el-submenu>
							</el-menu>
						</el-scrollbar>
					</el-tab-pane>
				</el-tabs>
			</div>
		</el-col>
		<!-- 右边内容 -->
		<el-col :span="19" style="padding: 0 20px">
			<!-- 用例编辑页面 -->
			<editCase :step="stepId"></editCase>
		</el-col>
		
	</el-row>
	<!-- 添加用例的弹框 -->
	<el-dialog v-model="addDlg" title="添加用例" width="35%">
		<el-form :model="addCaseForm">
			<el-form-item label="用例名称"><el-input v-model="addCaseForm.title" autocomplete="off" /></el-form-item>
		</el-form>
		<template #footer>
			<span class="dialog-footer">
				<el-button @click="addDlg = false" >取消</el-button>
				<el-button type="success" @click="addCase" >确定</el-button>
			</span>
		</template>
	</el-dialog>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex';
import editCase from '../components/common/editCase.vue';
import DataList from '../components/common/DataList.vue';
export default {
	components: {
		DataList,
		editCase
	},
	data() {
		return {
			// 选中的测试用例
			stepId: null,
			// 选中的测试环境
			env: null,
			addDlg: false,
			addCaseForm: {
				title: ''
			}
		};
	},
	computed: {
		...mapState(['interfaces', 'testEnvs']),
		...mapGetters(['interfaces1', 'interfaces2'])
	},
	methods: {
		...mapActions(['getAllInter']),
		// 点击添加用例
		clickAdd(interId) {
			this.addDlg = true;
			this.addCaseForm.interface = interId;
		},
		async addCase() {
			const response = await this.$api.createTeststep(this.addCaseForm);
			if (response.status === 201) {
				this.addDlg = false;
				this.$message({
					type: 'success',
					message: '添加成功',
					duration: 1000
				});
				this.getAllInter();
			}
		}
	},
	created() {
	  this.getAllInter()
  }
};
</script>

<style scoped>

.el-tag {
  color: #ffffff;
  width:60px;
  text-align: center;
}

.el-tag--small {
    height: 30px;
    padding: 0 8px;
    line-height: 28px;
}
#menu {
  list-style: none;
  padding-left: 0;
}
.data_box {
  resize: horizontal;
  overflow: auto;
}
</style>
