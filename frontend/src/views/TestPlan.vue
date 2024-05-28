<template>
	<el-row :gutter="10">
		<el-col :span="4">
			<div class="data_box">
          <el-tabs type="border-card" stretch>
					<el-tab-pane label="测试计划">
          </el-tab-pane>
          </el-tabs>
				<el-button @click="addPlan" type="success" plain size="mini" style="width: 100%;" icon="el-icon-plus">添加测试计划</el-button>
				<el-scrollbar height="calc(100vh - 134px);">
					<el-menu :default-active="active" class="el-menu-vertical-demo" active-text-color="#409eff" text-color="#000000" style="background: none;border: none;">
						<el-menu-item @click="getPlanData(item)" :index="item.id.toString()" v-for="item in planList" style="height: 35px;line-height: 35px;">
							<span class="el-icon-collection-tag"></span>
							<span>{{ item.name }}</span>
						</el-menu-item>
					</el-menu>
				</el-scrollbar>
			</div>
		</el-col>
		<el-col :span="10" v-if="planInfo">
			<!-- 基本信息 -->
			<el-divider content-position="left"><b>基本信息</b></el-divider>
			<el-row :gutter="5" style="margin-bottom: 20px;">
				<el-col :span="16">
					<el-input v-model="planInfo.name" size="mini">
						<template #prepend>
							计划名称
						</template>
						<template #append>
							<el-button @click="savePlan" plain icon="el-icon-circle-check" size="mini" type="primary">保存</el-button>
						</template>
					</el-input>
				</el-col>
				<el-col :span="8" style="text-align: right;">
					<el-button @click="runPlan" size="mini" type="primary" icon="el-icon-s-promotion">运行</el-button>
					<el-button @click="delPlan" plain icon="el-icon-delete" size="mini" type="danger">删除</el-button>
				</el-col>
			</el-row>
			<!-- 测试场景列表 -->
			<el-divider content-position="left"><b>测试场景</b></el-divider>
			<el-scrollbar height="calc(100vh - 210px)">
				<el-table :data="scents" row-key="id" style="width: 100%;margin-bottom: 10px;" :show-header="false" empty-text="暂无数据">
					<el-table-column>
						<template #default="scope">
							<span class="el-icon-s-help" style="color: #409eff;font-weight: bold;font-size: 14px;margin-right: 5px">{{ '测试场景' + (scope.$index+1)}}</span>
							<span style="font-weight: bold;font-size: 14px;">{{ scope.row.name }}</span>
						</template>
					</el-table-column>
					<el-table-column width="100px">
						<template #default="scope">
							<el-button @click='delPlanInScent' plain size="mini" type="danger" icon="el-icon-delete">删除</el-button>
						</template>
					</el-table-column>
				</el-table>
				<el-button @click="drawer = true" plain icon="el-icon-plus" size="mini" type="success">添加测试场景</el-button>
			</el-scrollbar>
		</el-col>
		<el-col :span="10">
			<el-divider content-position="left"><b>通过率趋势图</b></el-divider>
			<!-- 通过率趋势图 -->
			<div ref="chartTable" class="char_box1"></div>

			<el-divider content-position="left"><b>近三天执行记录</b></el-divider>
			<!-- 执行记录 -->
			<el-scrollbar height="calc(100vh - 380px)">
				<el-table :data="records" class="table-style" size="mini" empty-text="暂无数据">
					<el-table-column prop="create_time" label="执行时间" min-width="140" align="center">
						<template #default="scope">
							{{ $tools.rTime(scope.row.create_time) }}
						</template>
					</el-table-column>
					<el-table-column prop="env_name" label="测试环境" min-width="110" align="center"></el-table-column>
					<el-table-column prop="all" label="总用例" min-width="50" align="center">
						<template #default="scope">
							<span v-if="scope.row.statue !== '执行中'">{{ scope.row.all }}</span>
						</template>
					</el-table-column>

					<el-table-column label="通过数" min-width="50" align="center">
						<template #default="scope">
							<span v-if="scope.row.statue !== '执行中'">{{ scope.row.success }}</span>
						</template>
					</el-table-column>
					<el-table-column label="通过率" min-width="80" align="center">
						<template #default="scope">
							<span v-if="scope.row.statue !== '执行中'">{{ scope.row.pass_rate + '%' }}</span>
						</template>
					</el-table-column>
					<el-table-column label="测试报告" width="100" align="center">
						<template #default="scope">
							<span v-if="scope.row.status === '执行中'">
								<el-tag>{{ scope.row.status }}</el-tag>
							</span>
							<el-button v-else type="success" icon="el-icon-view" plain size="mini" @click="$router.push({ name: 'report', params: { id: scope.row.id } })">
								报告
							</el-button>
						</template>
					</el-table-column>
				</el-table>
			</el-scrollbar>
		</el-col>
	</el-row>

	<!-- 添加测试场景到测试计划中 -->
  <el-drawer v-model="drawer" direction="rtl" size="30%" :show-close="false">
    <template #title><b style="color: #000000;">添加测试场景</b></template>
    <div class="select_content" style="position: relative; height: calc(100vh - 130px); overflow-y: auto;">
      <el-table ref="addRef" @selection-change="selectTable" size="mini" :data="Scents2" tooltip-effect="dark" style="width: 100%" empty-text="暂无数据">
        <el-table-column type="selection" min-width="40"></el-table-column>
        <el-table-column prop="name" label="全选" min-width="120"></el-table-column>
      </el-table>
    </div>
		<div style="margin: 10px; text-align: center">
			<el-tooltip class="item" effect="dark" content="添加选中测试流程到任务中" placement="top-start">
				<el-button  @click="addScentToPlan" plain type="success" size="mini">确认添加</el-button>
			</el-tooltip>
			<el-tooltip class="item" effect="dark" content="清除选中选项" placement="top-start">
				<el-button plain type="warning" size="mini" @click="$refs.addRef.clearSelection()">清除选中</el-button>
			</el-tooltip>
			<el-tooltip class="item" effect="dark" content="关闭当前窗口" placement="top-start">
				<el-button plain type="danger" size="mini" @click="drawer = false">关闭窗口</el-button>
			</el-tooltip>
		</div>
	</el-drawer>
</template>

<script>
import { mapState } from 'vuex';
import { ElNotification } from 'element-plus';
import { ElMessage, ElMessageBox } from 'element-plus';
export default {
	components: {},
	data() {
		return {
			// 测试计划列表
			planList: [],
			// 当前选中的测试计划
			planInfo: null,
			// 选中激活的测试计划
			active: '1',
			// 测试计划中的所有测试场景
			scents: [],
			// 测试计划中所有运行记录
			records: [],
			// 添加测试场景的弹框
			drawer: false,
			// 存储勾选要添加到计划中的测试场景
			addScentList: []
		};
	},
	computed: {
		...mapState(['pro', 'envId', 'testScents']),
		chartData: function() {
			let runDate = [];
			let passRate = [];

			for (let item of this.records) {
				runDate.push(this.$tools.rTime(item.create_time));
				passRate.push(parseFloat(item.pass_rate).toFixed(2));
			}
			return {
				label: runDate.reverse(),
				// value: passRate.reverse()
				value: passRate
			};
		},
		// 可以添加到任务中的套件
		Scents2: function() {
			// 获取计划中没有添加的所有测试场景
			let newSuites = this.testScents.filter((item, index) => {
				return !this.scents.find(item2 => {
					return item2.id == item.id;
				});
			});
			return newSuites;
		}
	},
	methods: {
		async getAllPlan() {
			const response = await this.$api.getTestPlan(this.pro.id);
			if (response.status === 200) {
				this.planList = response.data;
				// 设置默认激活的测试计划,并获取数据
				if (this.planList.length > 0 && this.planInfo == null) {
					this.active = this.planList[0].id.toString();
					this.getPlanData(this.planList[0]);
				}
			}
		},
		// 获取测试计划下所有的测试场景
		async getPlanData(plan) {
			this.planInfo = { ...plan };
			// 获取测试计划下所有的测试场景
			const response = await this.$api.getTestScent({
				testplan: plan.id
			});
			if (response.status == 200) {
				this.scents = response.data;
			}
			this.getAllRecord();
		},
		// 获取测试计划所有的执行记录
		async getAllRecord() {
			const response2 = await this.$api.getTestRecord({ plan: this.planInfo.id,project: this.pro.id });
			if (response2.status == 200) {
				this.records = response2.data;
			}
		},

		// 添加测试计划
		async addPlan() {
			const params = {
				project: this.pro.id,
				name: "New Plan"
			};
			const response = await this.$api.createTestPlan(params);
			if (response.status === 201) {
				this.$message({
					type: 'success',
					message: '添加成功',
					duration: 1000
				});
				this.getAllPlan();
			}
		},
		// 保存测试计划名
		async savePlan() {
			const response = await this.$api.updateTestPlan(this.planInfo.id, this.planInfo);
			if (response.status === 200) {
				this.$message({
					type: 'success',
					message: '保存成功',
					duration: 1000
				});
				this.getAllPlan();
			}
		},
		// 运行测试计划
		async runPlan() {
			if (this.envId) {
				const params = {
					env: this.envId,
					plan: this.planInfo.id,
          types: 1
				};
				this.$message({
					type: 'success',
					message: '开始运行!',
					duration: 1000
				});
				const response = await this.$api.runPlan(this.planInfo.id, params);
				if (response.status === 200) {
					ElNotification({
						title: '提示',
						message: response.data.status,
						duration: 1000
					});
					this.getAllRecord();
				}
				console.log(response.data);
			} else {
				this.$message({
					type: 'warning',
					message: '当前未选中执行环境!',
					duration: 1000
				});
			}
		},
		// 删除测试计划
		delPlan() {
			ElMessageBox.confirm('确定要删除吗?', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning'
			})
				.then(async () => {
					const response = await this.$api.delTestPlan(this.planInfo.id);
					if (response.status === 204) {
						ElMessage({
							type: 'success',
							message: '删除成功',
							duration: 1000
						});
						this.getAllPlan();
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
		selectTable(val) {
			// 将选中的测试场景id保存到addScentList中
			val.forEach((item)=>{
				this.addScentList.push(item.id)
			})
		},
		// 添加选中的测试场景到测试计划中
		async addScentToPlan(){
      if (this.addScentList.length === 0) {
        this.$message({
          type: 'warning',
          message: '请勾选要添加的测试场景',
          duration: 1000
        });
      return; // 如果没有勾选场景，则不执行后续操作
          }
			let params = {...this.planInfo}
			params.scenes.push(...this.addScentList)
			// 发送请求
			const response = await this.$api.updateTestPlan(params.id,params)
			if(response.status===200){
				this.$message({
					type: 'success',
					message: '添加成功',
					duration: 1000
				});
				// 更新页面数据
				this.planInfo = response.data
				this.getPlanData(this.planInfo);
			}
			// 清空选中的选项
			this.$refs.addRef.clearSelection();
			this.drawer = false;
		},
		// 删除测试计划中的测试场景
		async delPlanInScent(index) {
			let params = {...this.planInfo}
			params.scenes.splice(index, 1);
			const response = await this.$api.updateTestPlan(params.id,params)
			if (response.status === 200) {
				this.$message({
					type: 'success',
					message: '删除成功',
					duration: 1000
				});
				// 更新页面中当前任务的数据
				this.planInfo = response.data
				this.getPlanData(this.planInfo);
			}
		},
	},
	created() {
		this.getAllPlan();
	},
	watch: {
		records() {
			// 渲染通过率趋势图
			this.$chart.chart3(this.$refs.chartTable, this.chartData.value, this.chartData.label);
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
.char_box1 {
	height: 200px;
}
</style>
