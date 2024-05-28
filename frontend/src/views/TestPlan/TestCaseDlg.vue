<template>
  <el-dialog v-model="sceneDlg" title="添加场景" width="75%" :before-close="clickClear" top="0">
  <div style="margin-left: 20px">
    <!--    顶部功能-->
    <div >
      <el-input style="width: 330px" v-model="filterText" placeholder="请输入用例名称进行搜索" clearable>
        <template #append>
          <el-button type="primary" @click="searchClick">查询</el-button>
        </template>
      </el-input>
      <span>
      <el-button
              type="warning"
              style="float: right;margin-right: 19px"
              @click="clickClear"
              icon="el-icon-close"
                >关闭窗口
            </el-button>
      <el-button
              type="primary"
              style="float: right;margin-right: 15px"
              @click="addScentToPlan"
              icon="el-icon-check"
                >确认选择
            </el-button>
      </span>
    </div>
    <!--    表格功能-->
    <el-scrollbar height="calc(100vh - 110px)">
    <div style="margin-top: 15px;margin-right: 20px">
      <el-table :data="caseList"  stripe empty-text="暂无数据" border @selection-change="handleSelectionChange">
            <el-table-column type="selection" align="center" width="50"></el-table-column>
            <el-table-column label="序号" align="center" width="60">
              <template #default="scope">
                <span>{{ scope.$index + 1 }}</span>
              </template>
            </el-table-column>
            <el-table-column label="用例名称" align="center" >
              <template #default="scope">
                <router-link class="no-underline" :to="`/TestCaseDetail/`" style="color: #409eff" @click="clickEdit(scope.row)">{{ scope.row.name }}</router-link>
              </template>
            </el-table-column>
            <el-table-column label="所属项目" prop="project.name"  align="center" />
            <el-table-column label="步骤数" width="70" prop="stepCount" align="center"/>
            <el-table-column label="用例描述" prop="desc" align="center" >
              <template #default="scope">
              <el-tooltip class="item" effect="dark" :content="scope.row.desc" placement="top">
                <div v-if="scope.row.desc.length >16" >{{ scope.row.desc.slice(0, 16) }}...</div>
                <div v-else>{{ scope.row.desc }}</div>
              </el-tooltip>
              </template>
            </el-table-column>
            <el-table-column label="创建人" prop="creator" align="center"  width="120"/>
            <el-table-column label="创建时间" align="center" width="160">
              <template #default="scope">
                {{ $tools.rTime(scope.row.create_time) }}
              </template>
            </el-table-column>
            <el-table-column label="更新人" prop="modifier" align="center" width="120"/>
            <el-table-column label="更新时间" align="center" width="160">
              <template #default="scope">
                <a v-if="scope.row.update_time">{{$tools.rTime(scope.row.update_time)}}</a>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="330" align="center">
              <template #default="scope">
                <el-button @click="runCase(scope.row)" size="mini" type="primary" icon="el-icon-s-promotion">运行</el-button>
                <el-button @click="clickEdit(scope.row)" size="mini" type="warning" icon="el-icon-menu">添加管理步骤</el-button>
                <el-button @click="delCase(scope.row.id)" size="mini" type="danger" plain icon="el-icon-delete">删除</el-button>
              </template>
            </el-table-column>
    </el-table>
    </div>
    <div class="pagination-container">
      <el-pagination  background layout="total, prev, pager, next, jumper"
                    @current-change="currentPages"
                    :default-page-size="100"
                    :total="pages.count"
                    :current-page="pages.current"
                   next-text="下一页" prev-text="上一页">
      </el-pagination>
    </div>
    </el-scrollbar>
  </div>
  </el-dialog>
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
              <span v-else-if="props.row.state == '错误'" style="color: #fca130;">{{ props.row.state }}</span>
							<span v-else style="color:#F56C6C">{{ props.row.state }}</span>
						</template>
					</el-table-column>
				</el-table>
			</el-scrollbar>
		</div>
	</el-drawer>
</template>

<script>
import {mapMutations, mapState} from "vuex";
import caseResult from '../../components/common/caseResult.vue';
import {ElNotification} from "element-plus";
export default {
  props: {
    planId: String
  },
  computed: {
    ...mapState(['pro','envId']),
  },
  components:{
    caseResult
  },
  data(){
    return {
      filterText:'',
      pages: [],
      caseList: [],
      ResultDlg:false,
      runScentResult:'',
      sceneDlg:true,
      selectedRows: []

    }
  },
 methods: {
    ...mapMutations(['CaseInfo']),
    // 查询
   searchClick() {
     this.allTestCase(this.pro.id,this.pages.current,this.filterText)
   },

   // 点击编辑用例
   clickEdit(id) {
   this.$router.push({ name: 'TestCaseDetail' });
   this.CaseInfo(id)
   },

   // 用例列表
   async allTestCase(project,page,name) {
     const response =await this.$api.getTestCase(project,page,name)
     if (response.status ===200){
        // 将获取到的测试用例数据存储在 caseList 中
				const allCase = response.data.result;
				this.pages = response.data
        // 调用接口获取已存在于计划中的场景列表
        const existingScenesResponse  = await this.$api.getTestCase_({
				testplan: this.planId
			});
        if (existingScenesResponse.status === 200) {
              const existingScenes = existingScenesResponse.data.result;
              // 过滤掉已存在于计划中的场景
              this.caseList = allCase.filter(item => !existingScenes.map(scene => scene.id).includes(item.id));
              // 过滤掉 stepCount 为 0 的数据
              this.caseList = this.caseList.filter(item => item.stepCount !== 0);
              this.pages.count =  this.caseList.length
        }
			}
   },

   currentPages(currentPage) {
      this.allTestCase(this.pro.id,currentPage)
      this.pages.current = currentPage

  },

   // 点击删除
   delCase(id) {
    this.$confirm('此操作将永久删除该用例, 是否继续?', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
      .then(async () => {
        const response = await this.$api.delTestCase(id)
        if(response.status ===204){
          this.$message({
            type: 'success',
            message: '删除成功!'
          });
          // 刷新页面
          this.allTestCase(this.pro.id);
          this.filterText = ''
        }
      })
      .catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        });
      });
  },

  // 运行测试用例
  async runCase(data) {
      const stepCount = parseInt(data.stepCount);
      console.log(stepCount)
      if(stepCount > 0){
			if (this.envId) {
				const params = {
					env: this.envId,
					scene: data.id
				};
          ElNotification({
            title: '开始运行',
            message: '运行过程中请稍等片刻噢',
            type: 'success',
            duration:1000
          });
				const response = await this.$api.runCases(data.id, params);
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
		}else this.$message({
					type: 'warning',
					message: '请添加步骤后再运行',
					duration: 1000
				});
		  },

  closeModal() {
    this.$emit('close-modal');
  },
  // 点击取消
  clickClear(){
    this.closeModal()
  },
  // 添加选中的测试场景到测试计划中
  async addScentToPlan(){
      if (this.selectedRows.length === 0) {
        this.$message({
          type: 'warning',
          message: '请勾选要添加的测试场景',
          duration: 1000
        });
      return; // 如果没有勾选场景，则不执行后续操作
      }
			let params = {}
      params.scene_ids = [...this.selectedRows]
			const response = await this.$api.createTestPlan_scene(this.planId,params)
			if(response.status===200){
				this.$message({
					type: 'success',
					message: '添加成功',
					duration: 1000
				});
			}
      this.closeModal()
		},


  handleSelectionChange(val) {
      this.selectedRows = val.map(row => row.id);
      console.log(this.selectedRows)
    },

 },
 created() {
  this.allTestCase(this.pro.id);
},

}


</script>

<style scoped>
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
.no-underline {
  text-decoration: none;
}
</style>
