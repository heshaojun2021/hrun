<template>
	<el-row :gutter="10">
		<!-- 左边内容 -->
		<el-col :span="4">
			<div class="data_box">
          <el-tabs type="border-card" stretch>
					<el-tab-pane label="测试场景">
          </el-tab-pane>
          </el-tabs>
				<el-button @click="addScent" type="success" plain size="mini" style="width: 100%;" icon="el-icon-plus">添加测试场景</el-button>
				<el-scrollbar height="calc(100vh - 126px);">
					<el-menu :default-active="active" class="el-menu-vertical-demo" active-text-color="#409eff" text-color="#000000" style="background: none;border: none;">
						<el-menu-item @click="getScentData(item)" :index="item.id.toString()" v-for="item in testScents" style="height: 35px;line-height: 35px;">
							<span class="el-icon-s-help"></span>
							<span>{{ item.name }}</span>
						</el-menu-item>
					</el-menu>
				</el-scrollbar>
			</div>
		</el-col>
		<!-- 右边内容 -->
		<el-col :span="20" style="padding: 0 20px;">
			<div class="scent-data-box" v-if="steps">
				<el-divider content-position="left"><b>场景信息</b></el-divider>
				<el-row :gutter="5" style="margin-bottom: 20px;">
					<el-col :span="8">
						<el-input v-model="scentInfo.name" size="mini" maxlength="50" clearable>
							<template #prepend>
								场景名称
							</template>
							<template #append>
								<el-button @click="saveScent" plain icon="el-icon-circle-check" size="mini" type="success">保存</el-button>
							</template>
						</el-input>
					</el-col>
					<el-col :span="5" style="text-align: right;">
						<el-button @click="runScent" plain size="mini" type="success" icon="el-icon-s-promotion" >运行</el-button>
						<el-button @click="deleteScent" plain icon="el-icon-delete" size="mini" type="danger">删除场景</el-button>
					</el-col>
				</el-row>
				<el-divider content-position="left"><b>执行步骤</b></el-divider>
				<el-scrollbar height="calc(100vh - 210px)">
					<el-table :data="steps" row-key="id" style="width: 100%;margin-bottom: 10px;" :show-header="false" empty-text="暂无数据">
						<el-table-column>
							<template #default="scope">
                 <div style="cursor: pointer;">
								<span class="el-icon-map-location" style="color: #409eff;font-weight: bold;font-size: 14px;">{{ '步骤' +  (scope.$index+1)}}</span>
								<span style="font-weight: bold;font-size: 14px;margin-left: 10px">{{ scope.row.stepInfo.title }}</span>
                 </div>
							</template>
						</el-table-column>
						<el-table-column width="200px">
							<template #default="scope">
								<el-button @click="clickEditStep(scope.row.stepInfo.id)"  size="mini" type="primary" icon="el-icon-edit-outline">调试</el-button>
								<el-button @click="clickDelete(scope.row.id)" plain size="mini" type="danger" icon="el-icon-delete">删除</el-button>
							</template>
						</el-table-column>
					</el-table>
					<el-button @click="addStepDlg = true" plain icon="el-icon-plus" size="mini" type="success">新增步骤</el-button>
				</el-scrollbar>
			</div>
      <div class="container" v-if="testScents.length===0">
      <el-empty>
          <el-button type="primary" @click="addScent">添加测试场景</el-button>
      </el-empty>
      </div>
		</el-col>
	</el-row>
	<!-- 显示运行结果 -->
	<el-drawer v-model="ResultDlg" :with-header="false" size="50%">
		<div style="padding:20px;">
			<el-descriptions title="执行结果" border :column="4">
				<el-descriptions-item label="总数">{{ runScentResult.all }}</el-descriptions-item>
				<el-descriptions-item label="通过">{{ runScentResult.success }}</el-descriptions-item>
				<el-descriptions-item label="失败">{{ runScentResult.fail }}</el-descriptions-item>
				<el-descriptions-item label="错误">{{ runScentResult.error }}</el-descriptions-item>
			</el-descriptions>
			<div style="height: 40px;line-height: 40px;"><b>执行详情</b></div>
			<el-scrollbar height="calc(100vh - 180px)">
				<el-table :data="runScentResult.cases" style="width: 100%" empty-text="暂无数据">
					<el-table-column type="expand">
						<template #default="props">
							<caseResult :result="props.row"></caseResult>
						</template>
					</el-table-column>
					<el-table-column label="用例名" prop="name" />
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
							<span v-if="props.row.state == '成功'" style="color: #00AA7F;">成功</span>
							<span v-else style="color:#F56C6C">{{ props.row.state }}</span>
						</template>
					</el-table-column>
				</el-table>
			</el-scrollbar>
		</div>
	</el-drawer>
	<!-- 编辑用例的窗口 -->
	<el-drawer v-model="editStepDlg" :with-header="false" size="40%"><EditCase :step="editStepId" style="padding: 0 10px;"></EditCase></el-drawer>
	<!-- 添加测试步骤窗口 -->
	<el-drawer v-model="addStepDlg" :with-header="false">
		<template #default>
			<el-tabs type="card" style="height: calc(100vh - 100px);">
				<el-tab-pane label="内部接口">
					<el-tree ref="treeM1" :data="interfaces1" show-checkbox :props="addTreeProps" node-key="id" default-expand-all highlight-current empty-text="暂无数据">
						<template #default="{ node, data }">
							<span class="custom-tree-node">
								<div v-if="data.name">
									<b style="color:#409eff ;">
										<i class="el-icon-paperclip"></i>
										{{ data.name }}
									</b>
								</div>
								<div v-if="data.title">
									<b style="color:#409eff ;">
										<i class="el-icon-map-location"></i>
										用例
									</b>
									<span style="margin-left: 5px">{{ data.title }}</span>
								</div>
							</span>
						</template>
					</el-tree>
				</el-tab-pane>
				<el-tab-pane label="外部接口" name="second">
					<el-tree ref="treeM2" :data="interfaces2" show-checkbox :props="addTreeProps" node-key="id" default-expand-all :expand-on-click-node="false" empty-text="暂无数据">
						<template #default="{ node, data }">
							<span class="custom-tree-node">
								<div v-if="data.name">
									<b style="color:#409eff ;">
										<i class="el-icon-paperclip"></i>
										{{ data.name }}
									</b>
								</div>
								<div v-if="data.title">
									<b style="color:#409eff ;">
										<i class="el-icon-map-location"></i>
										用例
									</b>
									<span style="margin-left: 5px">{{ data.title }}</span>
								</div>
							</span>
						</template>
					</el-tree>
				</el-tab-pane>
			</el-tabs>
			<div class="add-btns">
				<el-tooltip class="item" effect="dark" content="将选择的用例,加入到测试场景中" placement="top-start">
					<el-button plain type="success" size="mini" @click="addToScent()">确认添加</el-button>
				</el-tooltip>
				<el-tooltip class="item" effect="dark" content="关闭当前窗口" placement="top-start">
					<el-button plain type="danger" size="mini" @click="addStepDlg = false">关闭窗口</el-button>
				</el-tooltip>
			</div>
		</template>
	</el-drawer>
</template>

<script>
/*
组件内实现的功能：
1、测试场景列表展示(使用菜单组件)
2、选中测试场景，显示测试场景详细的信息
3、测试场景的添加、删除、修改功能
4、测试场景内，添加测试步骤，删除测试步骤、编辑测试步骤
5、运行测试场景、运行单个测试步骤

*/
import { mapState, mapActions, mapGetters } from 'vuex';
import { ElNotification } from 'element-plus';
import { ElMessage, ElMessageBox } from 'element-plus';
import Sortable from 'sortablejs';
import EditCase from '../components/common/editCase.vue';
import caseResult from '../components/common/caseResult.vue';
export default {
	components: {
		EditCase,
		caseResult
	},
	data() {
		return {
			active: '1',
			// 当前选中的测试场景
			scentInfo: null,
			// 测试场景中的测试步骤列表
			steps: null,
			// 添加步骤到测试套件,添加用例弹窗显示
			addStepDlg: false,
			// 树形数据子元素的字段
			addTreeProps: {
				children: 'steps'
			},

			// 编辑用例的窗口显示
			editStepDlg: false,
			//编辑用例的id
			editStepId: null,
			// 运行结果
			runScentResult: null,
			// 是否显示运行结果
			ResultDlg: false
		};
	},
	computed: {
		...mapState(['pro', 'testScents', 'envId']),
		...mapGetters(['interfaces1', 'interfaces2'])
	},
	methods: {
		...mapActions(['getAllScent', 'getAllInter']),
		// 添加测试场景
		async addScent() {
			const params = {
				name: 'New Scent',
				project: this.pro.id
			};
			const response = await this.$api.createTestScent(params);
			if (response.status === 201) {
				this.$message({
					type: 'success',
					message: '添加成功',
					duration: 1000
				});
				this.getAllScent();
			}
		},
		// 删除测试场景
		async deleteScent() {
			ElMessageBox.confirm('确定要删除吗?', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning'
			})
				.then(async () => {
					const response = await this.$api.delTestScent(this.scentInfo.id);
					if (response.status === 204) {
						ElMessage({
							type: 'success',
							message: '删除成功',
							duration: 1000
						});
            this.getAllScent();
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
		// 编辑场景名保存
		async saveScent() {
			const response = await this.$api.updateTestScent(this.scentInfo.id, this.scentInfo);
			if (response.status === 200) {
				this.$message({
					type: 'success',
					message: '保存成功',
					duration: 1000
				});
			}
			this.getAllScent()
		},
		// 运行测试场景
		async runScent() {
			if (this.envId) {
				const params = {
					env: this.envId,
					scene: this.scentInfo.id
				};
				this.$message({
					type: 'success',
					message: '开始运行!',
					duration: 1000
				});
				const response = await this.$api.runScene(this.scentInfo.id, params);
				console.log(response.data);
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
		// 点击编辑用例
		clickEditStep(stepId) {
			this.editStepDlg = true;
			this.editStepId = stepId;
		},
		// 获取树形控件中被选中的用例
		getcheckedCase() {
			const Nodes1 = this.$refs.treeM1.getCheckedNodes();
			const Nodes2 = this.$refs.treeM2.getCheckedNodes();
			const Nodes = [...Nodes1, ...Nodes2];
			// 过滤出选中的用例
			const result = Nodes.filter(function(item, index) {
				return item.title;
			});
			return result;
		},
		// 获取测试场景下所有的测试步骤
		async getScentData(scent) {
			this.scentInfo = {...scent};
			const response = await this.$api.getScentDatas(scent.id);
			if (response.status === 200) {
				this.steps = response.data;
			}
		},
		// 删除测试场景中的数据
		async clickDelete(id) {
			const response = await this.$api.delScentData(id);
			if (response.status === 204) {
				this.$message({
					type: 'success',
					message: '删除成功',
					duration: 1000
				});
				this.getScentData(this.scentInfo);
			}
		},
		// 往测试场景中添加用例数据
		async addToScent() {
			this.checkedCase = this.getcheckedCase();
			let order_s = this.steps.length;
			for (let value of this.checkedCase) {
				let item = { ...value };
				order_s += 1;
				const response = await this.$api.addScentData({ step: item.id, scene: this.scentInfo.id, sort: order_s });
				if (response.status === 201) {
				  this.$message({
            type: 'success',
            message: '添加成功',
            duration: 1000
				})
				} else {
          this.$message({
            type: 'error',
            message: '添加失败',
            duration: 1000
				})

				}
			}
			this.addStepDlg = false;
			this.getScentData(this.scentInfo);
			this.getAllInter();
		},
		// 拖动套件中的用例顺序
		initSort() {
			// 选择表格
			const tbody = document.querySelector('.scent-data-box .el-table__body-wrapper tbody');
			const _this = this;
			Sortable.create(tbody, {
				onEnd({ newIndex, oldIndex }) {
					const currRow = _this.steps.splice(oldIndex, 1)[0];
					_this.steps.splice(newIndex, 0, currRow);
					// 修改后端用例数据的顺序
					_this.updateScentOrder();
				}
			});
		},
		// 修改后端套件内用例顺序
		async updateScentOrder() {
			// 修改caseList中的order字段
			this.steps.forEach((item, index, array) => {
				item.sort = index + 1;
			});
			// 发送请求后端修改用例顺序
			const response = await this.$api.updateScentDataOrder(this.steps);
			if (response.status === 200) {
				this.$message({
					type: 'success',
					message: '调整排序成功',
					duration: 500
				});
			}
		}
	},
	async mounted() {
		if (this.testScents.length > 0) {
			// 设置默认显示激活的测试场景
			this.active = this.testScents[0].id.toString();
			this.scentInfo = { ...this.testScents[0] };
			await this.getScentData(this.scentInfo);
			// 监听表格拖动
      try {
        const tbody = document.querySelector('.scent-data-box .el-table__body-wrapper tbody');
        console.log(tbody); // 打印 tbody
        this.initSort(); // 尝试执行排序初始化操作
      } catch (error) {
        // 捕获到异常时执行特定的逻辑
        console.error('初始化排序时出现异常：', error);
        // 在这里可以添加特定的处理逻辑，比如给出提示或者执行备用方案
      }
		}
	}
};
</script>

<style scoped>
.data_box {
	box-shadow: 0 0 5px #dcdfe6;
}
.add-btns {
	text-align: center;
	margin-top: 50px;
	height: 150px;
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
