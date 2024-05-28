<template>
	<el-button @click='addDialog=true'  style="margin-bottom: 30px;margin-left:20px;margin-top: 25px;" type="primary" icon="el-icon-plus">添加定时任务</el-button>
	
	<el-table :data="cronList" style="width: 100%" size="mini" empty-text="暂无数据">
    <el-table-column label="序号" align="center" width="60">
      <template #default="scope">
        <span>{{ scope.$index + 1 }}</span>
      </template>
    </el-table-column>
		<el-table-column prop="name" label="名称"  align="center"></el-table-column>
		<el-table-column prop="plan_name" label="执行任务"  align="center"></el-table-column>
		<el-table-column prop="env_name" label="执行环境" align="center"></el-table-column>
		<el-table-column prop="rule" label="时间配置"  align="center"></el-table-column>
     <el-table-column label="创建时间"  align="center">
			<template #default="scope">
				{{ $tools.rTime(scope.row.create_time) }}
			</template>
		</el-table-column>
    <el-table-column label="是否开启"  align="center">
			<template #default="scope">
				<el-switch @change='switchCronStatus(scope.row)' v-model="scope.row.status" active-color="#13ce66" inactive-color="#b1b1b1"></el-switch>
			</template>
		</el-table-column>
		<el-table-column label="操作"  align="center">
			<template #default="scope">
				<el-tooltip class="item" effect="dark" content="编辑" placement="top" >
					<el-button @click='showUpdateCronDlg(scope.row)' type="primary" size="mini" plain  icon="el-icon-edit-outline">编辑</el-button>
				</el-tooltip>
				<el-tooltip class="item" effect="dark" content="删除" placement="top">
					<el-button @click="delCron(scope.row.id)" type="danger" size="mini" plain icon="el-icon-delete" >删除</el-button>
				</el-tooltip>
			</template>
		</el-table-column>
	</el-table>
	
	<!-- 创建定时任务的窗口 -->
	<el-dialog v-model="addDialog" width="50%"  title="新增定时执行任务" :before-close="closeDialogCron" custom-class="class_dialog">
    <el-tabs type="card" v-model="currentTab">
      <el-tab-pane label="测试计划自动运行" name="first">
      <el-form :model="cronTabData" :rules="rulescronTab" ref="cronTabRef" label-width="80px">
        <el-form-item label="任务名称" prop="name">
            <el-input v-model="cronTabData.name" placeholder="请输入任务名称"></el-input>
        </el-form-item>
        <el-form-item label="测试环境" prop="env">
            <el-select v-model="cronTabData.env" placeholder="请选择环境" style="width: 100%;" no-data-text="暂无数据">
                <el-option v-for="item in testEnvs" :key="item.id" :label="item.name" :value="item.id">
                </el-option>
            </el-select>
        </el-form-item>
        <el-form-item label="时间配置" prop="rule">
            <el-popover
              v-model:visible="cronVisible"
              placement="bottom-start"
              width="30">
              <template #reference>
                <el-input
                  v-model="cronTabData.rule"
                  clearable
                  readonly
                  placeholder="请选择时间配置"
                  @click="cronFun(currentTab)"
                />
              </template>
              <timerTaskCron
                :runTimeStr="cronTabData.rule"
                @closeTime="closeRunTimeCron"
                @runTime="runTimeCron"
              >
                </timerTaskCron>
            </el-popover>
          </el-form-item>
        <el-form-item label="执行计划" prop="plan">
           <el-select style="width: 100%;" v-model="cronTabData.plan" placeholder="请选择" no-data-text="暂无数据">
              <el-option
                v-for="item in testPlans"
                :key="item.id"
                :label="item.name"
                :value="item.id">
              </el-option>
            </el-select>
        </el-form-item>
        <el-form-item label="是否开启">
          <el-switch
            v-model="cronTabData.status"
            active-color="#13ce66"
            inactive-color="#c3c3c3">
          </el-switch>
            </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer" style="text-align: center;">
            <el-button @click="closeDialogCron" >取 消</el-button>
            <el-button type="primary" @click="createCron(currentTab)" >确 定</el-button>
        </div>
      </el-tab-pane>
      <el-tab-pane label="YApi自动导入" name="second">
        <el-form :model="cronTabData" :rules="rulescronTab" ref="cronTabRef" label-width="100px">
          <el-form-item label="任务名称" prop="name" >
            <el-input v-model="cronTabData.name" placeholder="请输入任务名称"></el-input>
        </el-form-item>
          <el-form-item label="时间配置" prop="rule">
            <el-popover
              v-model:visible="cronVisibleYApi"
              placement="bottom-start"
              width="30">
              <template #reference>
                <el-input
                  v-model="cronTabData.rule"
                  clearable
                  readonly
                  placeholder="请选择时间配置"
                  @click="cronFun(currentTab)"
                />
              </template>
              <timerTaskCron
                :runTimeStr="cronTabData.rule"
                @closeTime="closeRunTimeCron"
                @runTime="runTimeCron"
              >
                </timerTaskCron>
            </el-popover>
          </el-form-item>
          <el-form-item label="平台地址" prop='url'>
                <el-input v-model="cronTabData.yapi.url" placeholder="请输入YApi平台项目地址" clearable />
          </el-form-item>
          <el-form-item label="平台TOKEN" prop='token'>
                <el-input v-model="cronTabData.yapi.token" placeholder="请输入YApi平台项目token" clearable />
              </el-form-item>
          <el-form-item label="平台项目ID" prop='YApiId'>
                <el-input v-model="cronTabData.yapi.YApiId" placeholder="请输入YApi平台项目id" clearable />
          </el-form-item>
          <el-form-item label="节点/模块" prop='treenode'>
               <el-cascader
                    v-model="cronTabData.yapi.treenode"
                    :options="treeOptions"
                    :props="{label:'name', value:'id',checkStrictly: true}"
                    @change="removeCascaderAriaOwns"
                    @visible-change="removeCascaderAriaOwns"
                    @expand-change="removeCascaderAriaOwns"
                    clearable
                    change-on-select
                    filterable
                    placeholder="请选择节点/模块"
                    />
          </el-form-item>
          <el-form-item label="是否开启">
            <el-switch
            v-model="cronTabData.status"
            active-color="#13ce66"
            inactive-color="#c3c3c3">
          </el-switch>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer" style="text-align: center;">
            <el-button @click="closeDialogCron" >取 消</el-button>
            <el-button type="primary" @click="createCron(currentTab)" >确 定</el-button>
        </div>
      </el-tab-pane>
    </el-tabs>
	</el-dialog>
	<!-- 修改定时任务的窗口 -->
	<el-dialog v-model="editDialog" width="50%"  title="修改定时执行任务" :before-close="closeDialogCron" custom-class="class_dialog">
    <el-form v-if="cronTabData.type===10" :model="cronTabData" :rules="rulescronTab" ref="cronTabRef" label-width="80px">
			<el-form-item label="名称" prop="name" >
			    <el-input v-model="cronTabData.name"></el-input>
			</el-form-item>
      <el-form-item label="测试环境" prop="env">
          <el-select v-model="cronTabData.env" placeholder="请选择环境" style="width: 100%;" no-data-text="暂无数据">
              <el-option v-for="item in testEnvs" :key="item.id" :label="item.name" :value="item.id">
              </el-option>
          </el-select>
      </el-form-item>
      <el-form-item label="时间配置">
          <el-popover
            v-model:visible="cronVisibleEdit"
            placement="bottom-start"
            width="30">
            <template #reference>
              <el-input
                v-model="cronTabData.rule"
                clearable
                readonly
                placeholder="请选择时间"
                @click="cronFun(cronTabData.type)"
              />
            </template>
            <timerTaskCron
              :runTimeStr="cronTabData.rule"
              @closeTime="closeRunTimeCron"
              @runTime="runTimeCron"
            >
              </timerTaskCron>
          </el-popover>
        </el-form-item>
			<el-form-item label="执行计划" prop="plan">
				 <el-select style="width: 100%;" v-model="cronTabData.plan" placeholder="请选择" no-data-text="暂无数据">
				    <el-option
				      v-for="item in testPlans"
				      :key="item.id"
				      :label="item.name"
				      :value="item.id">
				    </el-option>
				  </el-select>
			</el-form-item>
      <el-form-item label="是否开启">
          <el-switch
            v-model="cronTabData.status"
            active-color="#13ce66"
            inactive-color="#c3c3c3">
          </el-switch>
        </el-form-item>
    </el-form>
    <el-form v-else :model="cronTabData" :rules="rulescronTab" ref="cronTabRef" label-width="100px">
      <el-form-item label="任务名称" prop="name" >
        <el-input v-model="cronTabData.name" placeholder="请输入任务名称"></el-input>
    </el-form-item>
      <el-form-item label="时间配置" prop="rule">
        <el-popover
          v-model:visible="cronVisibleYApiEdit"
          placement="bottom-start"
          width="30">
          <template #reference>
            <el-input
              v-model="cronTabData.rule"
              clearable
              readonly
              placeholder="请选择时间配置"
              @click="cronFun(cronTabData.type)"
            />
          </template>
          <timerTaskCron
            :runTimeStr="cronTabData.rule"
            @closeTime="closeRunTimeCron"
            @runTime="runTimeCron"
          >
            </timerTaskCron>
        </el-popover>
      </el-form-item>
      <el-form-item label="平台地址" prop='url'>
            <el-input v-model="cronTabData.yapi.url" placeholder="请输入YApi平台项目地址" clearable />
      </el-form-item>
      <el-form-item label="平台TOKEN" prop='token'>
            <el-input v-model="cronTabData.yapi.token" placeholder="请输入YApi平台项目token" clearable />
          </el-form-item>
      <el-form-item label="平台项目ID" prop='YApiId'>
            <el-input v-model="cronTabData.yapi.YApiId" placeholder="请输入YApi平台项目id" clearable />
      </el-form-item>
      <el-form-item label="节点/模块" prop='treenode'>
           <el-cascader
                v-model="cronTabData.yapi.treenode"
                :options="treeOptions"
                :props="{label:'name', value:'id',checkStrictly: true}"
                @change="removeCascaderAriaOwns"
                @visible-change="removeCascaderAriaOwns"
                @expand-change="removeCascaderAriaOwns"
                clearable
                change-on-select
                filterable
                placeholder="请选择节点/模块"
                />
      </el-form-item>
      <el-form-item label="是否开启">
        <el-switch
        v-model="cronTabData.status"
        active-color="#13ce66"
        inactive-color="#c3c3c3">
      </el-switch>
      </el-form-item>
    </el-form>
	    <div slot="footer" class="dialog-footer" style="text-align: center;">
	        <el-button @click="closeDialogCron" >取 消</el-button>
			    <el-button type="primary" @click="UpdateCron" >提交修改</el-button>
	    </div>
	</el-dialog>
</template>




<script>
import timerTaskCron from '../components/common/timerTaskCron';
import { mapState } from 'vuex';
export default{

	data(){
		return{
     currentTab:'first',
     treeOptions:[],
     cronVisible: false,
     cronVisibleYApi: false,
     cronVisibleEdit: false,
     cronVisibleYApiEdit: false,
     rulescronTab: {
				name: [
					{
						required: true,
						message: '请输入名称',
						trigger: 'blur'
					}
				],
				env: [
					{
						required: true,
						message: '请选择环境',
						trigger: 'blur'
					}
				],
        plan: [
					{
						required: true,
						message: '请选择执行计划',
						trigger: 'blur'
					}
				],
			},
			// 定时任务列表
			cronList:null,
			editDialog:false,
			addDialog:false,
			// 添加定时任务
			cronTabData:{
				name: "",
				status: true,
				plan: null,
				env:null,
        rule: "",
        yapi:{
          token:'',
          YApiId:null,
          treenode:null,
          format:'list',
          project:null,
          url:'http://121.37.2.117:8081'
        },
        type:''
			  },
		}
	},
  components: {
	  timerTaskCron
  },

	computed:{
		...mapState(['pro','testEnvs','testPlans'])
	},
	methods:{
    cronFun(value) {
      if (value==='first') {
        this.cronVisible = true;
      }
      else if(value==='second'){
        this.cronVisibleYApi = true;
      }
      else if (value===10){
        this.cronVisibleEdit = true;
      }
      else if (value===20){
        this.cronVisibleYApiEdit = true;
      }
      else {
       console.error('未知的值:', value);
      }
    },
    closeRunTimeCron(isClose) {
      this.cronVisible = isClose;
      this.cronVisibleYApi= isClose;
      this.cronVisibleEdit= isClose;
      this.cronVisibleYApiEdit= isClose;
    },
    runTimeCron(cron) {
      this.cronTabData.rule= cron;
    },

		async getAllCron(){
			const response =await  this.$api.getCrons(this.pro.id)
			if (response.status ===200){
				this.cronList = response.data
			}
		},
		delCron(id) {
			this.$confirm('此操作将永久删除该定时任务, 是否继续?', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning'
			})
				.then(async () => {
					// 删除定时任务
					const response = await this.$api.delCron(id)
					if(response.status ===204){
						this.$message({
							type: 'success',
							message: '删除成功!'
						});
						// 刷新页面定时任务
						this.getAllCron()
					}
				})
				.catch(() => {
					this.$message({
						type: 'info',
						message: '已取消删除'
					});
				});
		},
		// 任务开启和关闭
		async switchCronStatus(cron){
			const response = await this.$api.updateCron(cron.id, cron)
			if (response.status === 200) {
				if (cron.status == true) {
					this.$message({
						type: 'success',
						message: '定时运行已开启',
						duration: 1000
					})
				} else {
					this.$message({
						type: 'warning',
						message: '定时运行已关闭',
						duration: 1000
					})
				}
			} else {
				this.$message({
					type: 'error',
					message: '修改状态失败',
					duration: 1000
				})
			}
		},
    // 取消按钮时重置输入信息
    closeDialogCron() {
      this.editDialog = false;
      this.addDialog = false;
      this.cronTabData = {
            name: "",
            rule: "",
            status: true,
            plan: null,
            env: null,
            yapi:{
              token:'',
              YApiId:null,
              treenode:null,
              format:'list',
              project:null,
              url:'http://121.37.2.117:8081'
            },
            type:null
          };
      this.$refs.cronTabRef.clearValidate();
      },


		// 添加定时任务
		async createCron(currentTab){
        if (currentTab==='first') {
          delete this.cronTabData.yapi;
          const params = {
            ...this.cronTabData,
            type:10,
            project:this.pro.id
          }
          const response = await this.$api.createCron(params)
            if (response.status ===201){
              this.$message({
                type: 'success',
                message: '定时任务添加成功',
                duration: 1000
              })
              this.closeDialogCron();
              this.getAllCron()
            }

        }
        else if(currentTab==='second'){
          let params = { ...this.cronTabData.yapi};
          params.project = this.pro.id;
          // 获取最后一个节点的id
          if (params.treenode && params.treenode.length > 0) {
            const lastValue = params.treenode[params.treenode.length - 1];  // 获取最后一个值
            params.treenode = lastValue
          }
          const data = {
            ...this.cronTabData,
            project:this.pro.id,
            yapi:params,
            type:20,
          }
          console.log(data)
          const response = await this.$api.createCron(data)
            if (response.status ===201){
              this.$message({
                type: 'success',
                message: '定时任务添加成功',
                duration: 1000
              })
              this.closeDialogCron();
              this.getAllCron()
            }

        }
        else {
          console.log('待完善')
        }
		},
		//显示修改定时任务的窗口
		showUpdateCronDlg(cron){
			this.cronTabData = JSON.parse(JSON.stringify(cron));
			this.editDialog = true
		},
		// 修改定时任务
		async UpdateCron(){
      let params = { ...this.cronTabData.yapi};
      params.project = this.pro.id;
      // 获取最后一个节点的id
      if (params.treenode && params.treenode.length > 0) {
        const lastValue = params.treenode[params.treenode.length - 1];  // 获取最后一个值
        params.treenode = lastValue
      }
      const data = {
            ...this.cronTabData,
            yapi:params
          }
      console.log(data)
			const response = await this.$api.updateCron(this.cronTabData.id,data)
			if (response.status ===200){
				this.$message({
					type: 'success',
					message: '修改成功',
					duration: 1000
				})
        this.closeDialogCron();
				this.getAllCron()
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
    // 树结构列表接口
    async allTree() {
      const response = await this.$api.gettreeNode()
      if (response.status === 200) {
        this.treeOptions = response.data.result}
     },

	},
	created() {
		this.getAllCron();
		this.allTree()
	}
}	
	
</script>

<style>
</style>
