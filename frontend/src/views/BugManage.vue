<template>
  <div>
    <el-scrollbar height="calc(100vh - 55px)">
	<div class="bug_box">
		<div  style="color: #00aa7f; margin: 10px;font-size: 15px"><b>bug统计</b></div>
		<el-row :gutter="10">
			<el-col :span="12"><div class="chartBox" ref="chart1Box"></div></el-col>
			<el-col :span="12"><div class="chartBox" ref="chart2Box"></div></el-col>
		</el-row>
		<el-card class="bug_list">
			<el-row style="margin-bottom: 10px">
				<el-button @click="showBugs = bugs" type="info" plain size="mini">全部</el-button>
				<el-badge :value="bugs1.length" :hidden="bugs1.length === 0" class="item" :max="99" style="margin: 0 10px;">
					<el-button @click="showBugs = bugs1" type="danger" plain size="mini">待处理</el-button>
				</el-badge>
				<el-button @click="showBugs = bugs2" type="warning" plain size="mini">处理中</el-button>
				<el-button @click="showBugs = bugs3" type="success" plain size="mini">处理完成</el-button>
				<el-button @click="showBugs = bugs4" type="primary" plain size="mini">无需处理</el-button>
        <el-button @click="showBugs = bugs5" type="info" plain size="mini">已关闭</el-button>
			</el-row>
			<el-table :data="showBugs" style="width: 100%;" size="mini" empty-text="暂无数据">
        <el-table-column label="序号" align="center" width="60">
          <template #default="scope">
            <span>{{ scope.$index + 1 }}</span>
          </template>
        </el-table-column>
				<el-table-column label="提交时间" min-width="120" align="center" show-overflow-tooltip>
					<template #default="scope">
						<span>{{ $tools.rTime(scope.row.create_time) }}</span>
					</template>
				</el-table-column>
				<el-table-column show-overflow-tooltip prop="desc" align="center" label="bug描述" min-width="120"></el-table-column>
				<el-table-column show-overflow-tooltip prop="interface_url" align="center" label="所属接口" min-width="00"></el-table-column>
				<el-table-column prop="status" label="bug状态" min-width="80" align="center">
          <template #default="scope">
              <span v-if="scope.row.status === '待处理'">
                  <el-tag  color="#f56c6c" size="large">{{ scope.row.status }}</el-tag>
              </span>
              <span v-if="scope.row.status === '处理中'">
                <el-tag  color="#e6a23c" size="large">{{ scope.row.status}}</el-tag>
              </span>
              <span v-if="scope.row.status === '处理完成'">
                <el-tag  color="#67c23a" size="large">{{ scope.row.status}}</el-tag>
              </span>
              <span v-if="scope.row.status === '无需处理'">
                <el-tag  color="#d3d4d6" size="large">{{ scope.row.status}}</el-tag>
              </span>
              <span v-if="scope.row.status === '已关闭'">
                <el-tag  color="rgb(0, 170, 127)" size="large">{{ scope.row.status}}</el-tag>
              </span>
          </template>
        </el-table-column>
				<el-table-column min-width="180">
					<template #default="scope">
						<div style="text-align: right;">
							<el-tooltip class="item" effect="dark" content="查看bug详情" placement="top">
								<el-button icon="el-icon-view" @click="showBugInfo(scope.row)" size="mini" type="success" plain>查看</el-button>
							</el-tooltip>
							<el-tooltip class="item" effect="dark" content="更新bug" placement="top">
								<el-button
									icon="el-icon-edit-outline"
									@click="clickUpdate(scope.row)"
									size="mini"
									type="primary"
									plain
								>编辑</el-button>
							</el-tooltip>
							<el-tooltip class="item" effect="dark" content="删除bug" placement="top">
								<el-button icon="el-icon-delete" @click="delBug(scope.row.id)" size="mini" type="danger" plain>删除</el-button>
							</el-tooltip>
						</div>
					</template>
				</el-table-column>
			</el-table>
		</el-card>
	</div>

	<!-- 查看bug信息 -->
	<el-drawer v-model="showBug" title="I am the title" :with-header="false" size='50%'>
		<el-scrollbar height="calc(100vh - 20px)">
			<el-card>
				<b>bug信息</b>
				<div style="margin-top: 10px;">
					<el-descriptions :column="4" direction="vertical" border>
						<el-descriptions-item label="提交者">admin</el-descriptions-item>
						<el-descriptions-item label="bug状态">{{ bugInfo.status }}</el-descriptions-item>
						<el-descriptions-item label="所属接口">{{ bugInfo.interface_url }}</el-descriptions-item>
						<el-descriptions-item label="提交时间">{{ $tools.rTime(bugInfo.create_time) }}</el-descriptions-item>
					</el-descriptions>
				</div>
			</el-card>
			<el-card style="margin: 5px;min-height: 400px;">
				<b>用例执行信息</b>
				<div style="margin-top: 10px;"><Result :result="bugInfo.info" :showbtn="false"></Result></div>
			</el-card>
			<el-card style="min-height: 400px;" v-if="bugLogs">
				<b>bug处理记录</b>
				<div style="margin-top: 10px;">
					<el-timeline>
						<el-timeline-item v-for="(activity, index) in bugLogs"
                              :key="index"
                              :timestamp="$tools.rDate(activity.create_time)"
                              placement="top"
                              color="#0bbd87">
							<el-card>
								<h4>{{ activity.handle }}</h4>
                <p v-if="activity.remark">评论：{{ activity.remark }}</p>
                <span style="color: #409eff;margin-right: 8px">{{ activity.update_user }}</span>
                <span>操作于 {{ $tools.rTime(activity.create_time) }}</span>
							</el-card>
						</el-timeline-item>
					</el-timeline>
				</div>
			</el-card>
			<el-empty v-else description="无" :image-size="400"></el-empty>
		</el-scrollbar>
	</el-drawer>

	<!-- 修改状态 -->
    <el-dialog title="更新bug信息" v-model="updateBugDlg" width="30%" :before-close="closeDialogBug">
      <el-form :model="updateBugForm">
        <el-form-item label="bug状态">
          <el-select style="width: 100%;" v-model="updateBugForm.status" placeholder="请选择bug状态">
            <el-option label="待处理" value="待处理"></el-option>
            <el-option label="处理中" value="处理中"></el-option>
            <el-option label="处理完成" value="处理完成"></el-option>
            <el-option label="无需处理" value="无需处理"></el-option>
            <el-option label="已关闭" value="已关闭"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="问题评论">
          <el-input type="textarea" :autosize="{ minRows: 2, maxRows: 6 }" v-model="updateBugForm.remark"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button size="mini" @click="closeDialogBug">取 消</el-button>
          <el-button size="mini" type="success" @click="updateBug">确 定</el-button>
        </div>
      </template>
    </el-dialog>
  </el-scrollbar>
  </div>
</template>

<script>
import Result from '../components/common/caseResult.vue';
import { mapState, mapActions } from 'vuex';

export default {
	data() {
		return {
			// 所有的bug
      showBug: false,
			bugInfo: null,
			bugLogs: null,
			updateBugDlg: false,
			updateBugForm: {},
			showBugs: [],
			bugs: []
		};
	},
	computed: {
		...mapState(['pro']),
		bugs1() {
			return this.bugs.filter((item, index, array) => {
				return item.status === '待处理';
			});
		},
		bugs2() {
			return this.bugs.filter((item, index, array) => {
				return item.status === '处理中';
			});
		},
		bugs3() {
			return this.bugs.filter((item, index, array) => {
				return item.status === '处理完成';
			});
		},
		bugs4() {
			return this.bugs.filter((item, index, array) => {
				return item.status === '无需处理';
			});
		},
    bugs5() {
			return this.bugs.filter((item, index, array) => {
				return item.status === '已关闭';
			});
		}
	},
	components: {
		Result
	},
	methods: {
		//获取所有的bug
		async getAllBug() {
			const response = await this.$api.getBugs({
				project: this.pro.id
			});
			if (response.status === 200) {
				this.bugs = response.data;
			}
		},
    //编辑bug取消弹窗重置
    closeDialogBug() {
        this.updateBugForm = '';
				this.updateBugDlg = false;
		    this.getAllBug();
        this.showBugs = this.bugs;
      },

		// 显示bug详情
		showBugInfo(bug) {
			this.bugInfo = bug;
			this.getBugAllLogs(bug.id);
      this.showBug = true
		},
		// 获取bug历史处理记录
		async getBugAllLogs(id) {
			const response = await this.$api.getBugLogs({ bug: id });
			if (response.status === 200 && response.data.length > 0) {
				this.bugLogs = response.data;
			}
		},
		// 修改bug
		async updateBug() {
			const reposne = await this.$api.updateBug(this.updateBugForm.id, this.updateBugForm);
			this.updateBugForm.remark = '';
			if (reposne.status === 200) {
				this.$message({
					type: 'success',
					message: '修改成功',
					duration: 1000
				});
        this.updateBugForm ='';
				await this.getBugAllLogs(this.updateBugForm.id);
				this.updateBugDlg = false;
        await this.getAllBug();
        this.showTable()
        this.showBugs = this.bugs;

			}
		},
		showTable() {
			// 渲染图表
			const ele = this.$refs.chart1Box;
			const data = [this.bugs.length, this.bugs3.length, this.bugs2.length, this.bugs1.length, this.bugs4.length, this.bugs5.length];
			const dataLabel = ['bug总数', '处理完成', '处理中', '待处理', '无需处理', '已关闭'];
			this.$chart.chart1(ele, data, dataLabel);
			const ele2 = this.$refs.chart2Box;
			this.$chart.chart2(ele2, [
				{ value: this.bugs3.length, name: '处理完成' },
				{ value: this.bugs2.length, name: '处理中' },
				{ value: this.bugs1.length, name: '待处理' },
				{ value: this.bugs4.length, name: '无需处理' },
        { value: this.bugs5.length, name: '已关闭' }
			]);
		},
		// 删除bug
		delBug(id) {
			this.$confirm('此操作将永久删除该bug, 是否继续?', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning'
			})
				.then(async () => {
					const reposne = await this.$api.deleteBug(id);
					if (reposne.status === 204) {
						this.$message({
							type: 'success',
							message: '删除成功',
							duration: 1000
						});
						await this.getAllBug();
						this.showTable()
						this.showBugs = this.bugs;
					}
				})
				.catch(() => {
					this.$message({
						type: 'info',
						message: '已取消删除'
					});
				});
		},

    clickUpdate(row){
      this.updateBugDlg = true;
      this.updateBugForm = {...row};
      this.updateBugForm.remark = '';
    },
	},
	updated() {
		this.showTable();
	},

	async created() {
		await this.getAllBug();
		this.showBugs = this.bugs;
		this.showTable();
	},
};
</script>

<style scoped>
.bug_list {
	height: calc(100vh - 290px);
	overflow-y: auto;
	margin-top: 12px;
}

.chartBox {
	height: 220px;
	background: rgba(198, 198, 202, 0.1);
}
.el-tag {
  color: #ffffff;
  width:80px;
}

</style>
