<template>
  <el-row :gutter="10">
    <!-- 左边内容 -->
    <el-col :span="5">
      <div class="tree-component">
        <el-input v-model="filterText" placeholder="请输入计划名称进行搜索" clearable >
          <template #append>
            <el-button type="primary" @click="handletreeClick">查询</el-button>
          </template>
        </el-input>
        <el-button
          type="primary"
          style="margin-bottom: 5px;margin-top: 10px;"
          @click="addPlan"
          icon="el-icon-plus"
        >添加计划</el-button>
        <el-scrollbar height="calc(100vh - 150px)">
        <el-tree
          class="filter-tree"
          :data="planList"
          :props="defaultProps"
          default-expand-all
          :expand-on-click-node="false"
          @node-click="handleNodeClick"
        >
        <template v-slot="{ node, data }">
          <el-scrollbar>
          <span class="bold-node">
            {{ node.label }}
          </span>
          </el-scrollbar>
          <div class="node-content">
            <span>
              <a @click="clickPlan(node.data)"> <el-icon style="color: #0d84ff"><Edit /></el-icon> </a>
              <a @click="delPlan(node.data.id)"> <el-icon style="color: #0d84ff;margin-right: 20px"><Delete /></el-icon> </a>
            </span>
          </div>
        </template>
        </el-tree>
        </el-scrollbar>
      </div>
    </el-col>
    <!-- 中间内容 -->
    <el-col :span="10" style="margin-top: 10px">
      <span style="display: flex; justify-content: space-between;margin-left: 10px;margin-right: 26px">
        <el-button
            type="primary"
            style="margin-bottom: 5px;margin-top: 10px;"
            @click="clickAddScene"
            icon="el-icon-plus"
          >添加场景
        </el-button>
        <el-button
          type="primary"
          style="margin-bottom: 5px;margin-top: 10px;"
          @click="runPlan"
          icon="el-icon-s-promotion"
          >运行
        </el-button>
      </span>
      <el-empty v-if="scene_list.length===0" description="暂无数据请添加测试场景"></el-empty>
    <el-scrollbar height="calc(100vh - 115px)">
     <div style="display: flex; flex-wrap: wrap;margin-top: 30px">
      <el-card v-for="(item, index) in scene_list" :key="item.id"
               class="custom-card"
               style="flex: 0 0 calc(30.5%); margin: 5px;cursor: pointer;"
               shadow="hover"
                >
        <!-- 卡片内容 -->
        <div @click="clickView(item)">
          <i @click.stop class="el-icon-delete" @click="delScene(item.id)" style="display: flex;float:right;margin-top: -10px;margin-right: -10px;color:#7e8bec"></i>
          <div style="display: flex; align-items: center;">
            <icon icon="line-md:star-pulsating-loop" font-size="25" style="margin-right: 5px;color: #7e8bec"></icon>
            <span class="text-16px">{{ item.name }}</span>
          </div>
          <div class="message">{{ item.desc }}</div>
          <div class="projectinfo_user_time">
            <span>步骤数：{{ item.stepCount }}</span>
            <span>场景{{ index + 1 }}</span>
          </div>
        </div>
      </el-card>
    </div>
    </el-scrollbar>
  </el-col>
    <!-- 右边内容 -->
    <el-col :span="9">
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
							<span v-if="scope.row.status !== '执行中'">{{ scope.row.all }}</span>
						</template>
					</el-table-column>

					<el-table-column label="通过数" min-width="50" align="center">
						<template #default="scope">
							<span v-if="scope.row.status !== '执行中'">{{ scope.row.success }}</span>
						</template>
					</el-table-column>
					<el-table-column label="通过率" min-width="80" align="center">
						<template #default="scope">
							<span v-if="scope.row.status !== '执行中'">{{ scope.row.pass_rate + '%' }}</span>
						</template>
					</el-table-column>
					<el-table-column label="测试报告" width="100" align="center">
						<template #default="scope">
							<span v-if="scope.row.status === '执行中'">
								<el-tag>{{ scope.row.status }}</el-tag>
							</span>
							<el-button v-else type="success" icon="el-icon-view" plain size="mini" @click="$router.push({ name: 'report', params: { id: scope.row.id } })">
								查看
							</el-button>
						</template>
					</el-table-column>
				</el-table>
			</el-scrollbar>
		</el-col>

  </el-row>
  <!-- 修改计划窗口-->
  <el-dialog v-model="editDlg" title="修改计划" width="20%" :before-close="clickClear">
    <el-form :model="planForm" ref="treeRef">
    <el-form-item label="计划名称" prop="name">
      <el-input v-model="planForm.name" autocomplete="off" placeholder="请输入计划名称" clearable/>
    </el-form-item>
    </el-form>
    <template #footer>
			<span class="dialog-footer">
				<el-button @click="clickClear" >取消</el-button>
        <el-button  type="primary" @click="savePlan" >确定</el-button>
			</span>
		</template>
  </el-dialog>
  <!--  添加测试场景窗口-->
  <TestCase v-if="sceneDlg" @close-modal="handleCloseModal" :planId="planId"></TestCase>
</template>

<script>
import {ElMessage, ElMessageBox, ElNotification} from "element-plus";
import {mapMutations, mapState} from "vuex";
import { Icon } from '@iconify/vue'
import TestCase from '../../views/TestPlan/TestCaseDlg.vue';
export default {
  components: {
    Icon,
    TestCase
  },
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
			addScentList: [],
      planForm:{
        name:''
      },
      filterText: '',
      editDlg:false,
      scene_list:'',
      checkList:'',
      sceneDlg: false,
      planId:'',

    }
  },
  computed: {
    ...mapState(['pro','envId']),
    defaultProps() {
      return {
        children: 'children',
        label: 'name',
      }
    },
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
  },
  methods: {
    ...mapMutations(['CaseInfo']),
    // 获取测试计划列表
    async getAllPlan(name) {
      if(name){
        const response = await this.$api.getTestPlan(this.pro.id,name);
        if (response.status === 200) {
          this.planList = response.data;
        }
        // 设置默认激活的测试计划,并获取数据
				if (this.planList.length > 0 ) {
				  this.planId = this.planList[0].id
					this.getScenes(this.planList[0].id);
				}
      }
      else {
        const response = await this.$api.getTestPlan(this.pro.id);
        if (response.status === 200) {
          this.planList = response.data;
        }
        // 设置默认激活的测试计划,并获取数据
				if (this.planList.length > 0 ) {
				  this.planId = this.planList[0].id
					this.getScenes(this.planList[0].id);
				}
      }
		},

		// 获取测试计划所有的执行记录
		async getAllRecord() {
			const response2 = await this.$api.getTestRecord({ plan: this.planId,project: this.pro.id });
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

    handleNodeClick(data) {
      this.planId = data.id
      this.getScenes(this.planId)
    },
    async getScenes(planId) {
      const response = await this.$api.getTestCase_({
				testplan: planId
			});
			if (response.status == 200) {
				this.scene_list = response.data.result;
			}
			this.getAllRecord();
    },
    // 点击查询
    handletreeClick() {
      this.getAllPlan(this.filterText)
    },

    // 点击取消
    clickClear(){
		  this.editDlg = false;
    },
    // 点击编辑测试计划
    clickPlan(data){
      this.editDlg = true;
      this.planForm = {...data}
    },
    // 保存测试计划名
		async savePlan() {
			const response = await this.$api.updateTestPlan(this.planForm.id, this.planForm);
			if (response.status === 200) {
				this.$message({
					type: 'success',
					message: '保存成功',
					duration: 1000
				});
				this.editDlg = false;
				this.getAllPlan();
			}
		},
    // 运行测试计划
		async runPlan() {
			if (this.envId) {
				const params = {
					env: this.envId,
					plan: this.planId,
          types: 2
				};
        ElNotification({
            title: '开始运行',
            message: '运行过程中请稍等片刻噢',
            type: 'success',
            duration:3000
          });
				const response = await this.$api.runPlan(this.planId, params);
				if (response.status === 200) {
					this.getAllRecord();
				}
			} else {
				this.$message({
					type: 'warning',
					message: '当前未选中执行环境!',
					duration: 1000
				});
			}
		},
		// 删除测试计划
		delPlan(id) {
			ElMessageBox.confirm('确定要删除吗?', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning',
			})
				.then(async () => {
					const response = await this.$api.delTestPlan(id);
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

    clickView(item) {
     this.$router.push({ name: 'TestCaseDetail' });
     item.back_type = 'plan'
     this.CaseInfo(item)
   },

    async delScene(id) {
      let params = {scene_id:id}

			const response = await this.$api.delTestPlan_scene(this.planId,params)
			if (response.status === 200) {
				this.$message({
					type: 'success',
					message: '删除成功',
					duration: 1000
				});
				// 更新页面中当前任务的数据
				this.getScenes(this.planId)
			}
		},
    clickAddScene() {
      this.sceneDlg = true;
    },

    handleCloseModal() {
      console.log('我被触发了',this.planId)
      this.sceneDlg = false; // 关闭弹窗
      this.getScenes(this.planId)
    },

  },

  created() {
    this.getAllPlan()
  },
  watch: {
		records() {
			// 渲染通过率趋势图
			this.$chart.chart3(this.$refs.chartTable, this.chartData.value, this.chartData.label);
		}
	}
}


</script>

<style scoped>
.tree-component {
  padding: 20px;
  box-shadow: 5px 0 5px rgba(0, 0, 0, 0.06); /* 添加此样式来设置阴影 */
}
.filter-tree {
  margin-top: 10px;
  padding-right:0px;
}
.tree-component[data-v-1b4274da] {
    width: 300px;
    padding-right: 0px;
    box-shadow: 5px 0 5px rgba(0, 0, 0, 0.06);
}
.node-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  font-size: 16px;

}
.el-icon {
  margin-left: 10px;
  transition: transform 0.3s ease;
}
.el-icon:hover {
  transform: scale(1.2);
}
.bold-node {
  font-weight: bold;
}
.data_box {
	box-shadow: 0 0 5px #dcdfe6;
}
.title {
	text-align: center;
	font: bold 16px/30px 'microsoft yahei';
	height: 30px;
}
.char_box1 {
  margin-top: 8px;
	height: 200px;
}

.message{
    --un-text-opacity: 1;
    color: rgb(156 163 175 / var(--un-text-opacity));
    font-size: 14px;
    margin-top: 15px
}
.projectinfo_user_time{
    --un-text-opacity: 1;
    color: rgb(156 163 175 / var(--un-text-opacity));
    font-size: 12px;
    justify-content: space-between;
    display: flex;
    margin-top: 20px;
}

.custom-card {
  background-color: #ffffff; /* 设置背景色 */
  border-radius: 8px; /* 设置圆角 */
  border: 1px solid #ddd; /* 设置边框 */
  overflow: hidden; /* 隐藏溢出内容 */
}

.custom-card:hover {
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.2); /* 设置鼠标悬停时的阴影效果 */
}
</style>
