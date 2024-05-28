<template>
 <el-button @click="clickAdd"  type="success" icon="el-icon-plus" style="margin-bottom: 30px;margin-left:20px;margin-top: 25px;">新增推送信息</el-button>
 <el-scrollbar >
  <div class="table_data">
    <el-table :data="hookList" v-loading="isLoading" stripe style="width: 100%" empty-text="暂无数据"  >
            <el-table-column label="序号" align="center" width="60">
              <template #default="scope">
                <span>{{ scope.$index + 1 }}</span>
              </template>
            </el-table-column>
            <el-table-column label="推送名称" prop="name" align="center" />
            <el-table-column label="hook地址" prop="webhook" align="center" >
              <template #default="scope">
                <el-tooltip placement="top-start" effect="dark" :content="scope.row.webhook">
                  <div >{{ scope.row.webhook.length > 30 ? scope.row.webhook.slice(0, 30) + '...' : scope.row.webhook }}</div>
                </el-tooltip>
              </template>
            </el-table-column>
            <el-table-column label="接收人" prop="user_ids" align="center"/>
            <el-table-column label="测试计划" prop="testPlan.name" align="center"/>
            <el-table-column label="创建时间" align="center">
            <template #default="scope">
              {{ $tools.rTime(scope.row.create_time) }}
            </template>
            </el-table-column>
            <el-table-column label="操作" width="180" align="center">
              <template #default="scope">
                <el-button @click="clickEdit(scope.row)" size="mini" plain type="success" icon="el-icon-edit-outline">编辑</el-button>
                <el-button @click="delHook(scope.row.id)" size="mini" type="danger" plain icon="el-icon-delete">删除</el-button>
              </template>
            </el-table-column>
    </el-table>
  </div>

  <div class="pagination-container">
    <el-pagination  background layout="total, prev, pager, next, jumper"
                    @current-change="currentPages"
                    default-page-size="100"
                    :total="pages.count"
                    :current-page="pages.current"
                   next-text="下一页" prev-text="上一页">
      </el-pagination>
  </div>
  </el-scrollbar>

<!--  新增弹窗-->
  <el-dialog v-model="addDlg" title="新增推送信息"  width="37%" custom-class="class_dialog" :required="true" style="text-align:left" :before-close="clearValidation">
		<el-form :model="addForm"  :rules="rulesHook" ref="HookRef" label-width="120px" style="max-width: 600px">
      <el-form-item prop="name" label="推送名称">
        <el-input v-model="addForm.name"  maxlength="50" minlength="1" placeholder="请输入推送名称"/>
      </el-form-item>
      <el-form-item prop="webhook" label="webhook地址" >
        <el-input v-model="addForm.webhook"   minlength="3" placeholder="请输入webhook地址" show-word-limit/>
      </el-form-item>
      <el-form-item prop="testPlan_id" label="测试计划">
				<el-select v-model="addForm.testPlan_id" placeholder="请选择测试计划" style="width: 100%;">
					<el-option :label="iter.name" :value="iter.id" v-for="iter in testPlans" :key="iter.id"></el-option>
				</el-select>
			</el-form-item>
      <el-form-item label="接收人">
				<el-select  multiple v-model="addForm.user_ids" placeholder="请选择接收人" style="width: 100%;">
					<el-option  :label="'@all'" :value="'@all'"  :key="'@all'" ></el-option>
          <el-option  :label="iter.weChat_name" :value="iter.weChat_name" v-for="iter in filteredUsers" :key="iter.id"  :disabled="editForm.user_ids.includes('@all')"></el-option>
				</el-select>
			</el-form-item>

		</el-form>
		<template #footer>
			<span class="dialog-footer">
				<el-button @click="clearValidation" size="medium">取消</el-button>
				<el-button type="success" @click="AddInter" size="medium">确定</el-button>
			</span>
		</template>
	</el-dialog>

<!--  修改弹窗-->
  <el-dialog v-model="editDlg" title="修改推送信息"  width="37%" custom-class="class_dialog" :required="true" style="text-align:left" :before-close="clearValidation">
		<el-form :model="editForm"  :rules="rulesHook" ref="HookRef" label-width="120px" style="max-width: 600px">
      <el-form-item prop="name" label="推送名称">
        <el-input v-model="editForm.name"  maxlength="50" minlength="1" placeholder="请输入推送名称"/>
      </el-form-item>
      <el-form-item prop="webhook" label="webhook地址" >
        <el-input v-model="editForm.webhook"   minlength="3" placeholder="请输入webhook地址" show-word-limit/>
      </el-form-item>
      <el-form-item prop="testPlan_id" label="测试计划">
				<el-select v-model="editForm.testPlan_id" placeholder="请选择测试计划" style="width: 100%;">
					<el-option :label="iter.name" :value="iter.id" v-for="iter in testPlans" :key="iter.id"></el-option>
				</el-select>
			</el-form-item>
      <el-form-item label="接收人">
				<el-select  multiple v-model="editForm.user_ids" placeholder="请选择接收人" style="width: 100%;">
					<el-option  :label="'@all'" :value="'@all'"  :key="'@all'" ></el-option>
          <el-option  :label="iter.weChat_name" :value="iter.weChat_name" v-for="iter in filteredUsers" :key="iter.id" :disabled="editForm.user_ids.includes('@all')"></el-option>
				</el-select>
			</el-form-item>
		</el-form>
		<template #footer>
			<span class="dialog-footer">
				<el-button @click="clearValidation" size="medium">取消</el-button>
				<el-button type="success" @click="EditInter" size="medium">确定</el-button>
			</span>
		</template>
	</el-dialog>


</template>


<script>
import {mapActions, mapState} from "vuex";
export default {
  data() {
    return {
      hookList:'',
      pages:'',
      addDlg:false,
      isLoading: false,
      editDlg: false,
      addForm:{
        name: '',
        webhook: '',
        user_ids: [],
        project_id: '',
        testPlan_id: '',
      },
      editForm:{
        name: '',
        webhook: '',
        user_ids: [],
        project_id: '',
        testPlan_id: '',
      },
      rulesHook: {
				// 验证用户名是否合法
				name: [
					{
						required: true,
						message: '请输入名称',
						trigger: 'blur'
					}
				],
				// 验证密码是否合法
				webhook: [
					{
						required: true,
						message: '请输入webhook地址',
						trigger: 'blur'
					}
				],
       testPlan_id: [
					{
						required: true,
						message: '请选择测试计划',
						trigger: 'blur'
					}
				]
			},

    }},
  computed: {
		...mapState(['pro','testPlans','Users']),
    filteredUsers() {
      const filtered = this.Users.filter( iter=> iter.weChat_name !== null);
      return filtered
    }
	},

  methods: {
    ...mapActions(['getAllUser']),

    // 点击添加
    clickAdd() {
      this.addDlg = true;
      this.addForm = {
        name: '',
        webhook: '',
        user_ids: [],
        project_id: this.pro.id,
        testPlan_id: '',
          }
        },
    // 点击修改
		clickEdit(info) {
			this.editDlg = true;
			this.editForm = { ...info };
			this.editForm.project_id = this.pro.id
      console.log(this.editForm)
		},

    // 点击删除
    delHook(id) {
			this.$confirm('此操作将永久删除该推送信息, 是否继续?', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning'
			})
				.then(async () => {
					const response = await this.$api.delHook(id)
					if(response.status ===204){
						this.$message({
							type: 'success',
							message: '删除成功!'
						});
						// 刷新页面
						this.getAllHook(this.pro)
					}
				})
				.catch(() => {
					this.$message({
						type: 'info',
						message: '已取消删除'
					});
				});
		},

    // 点击关闭弹窗
    clearValidation() {
      this.addDlg = false;
      this.editDlg = false;
      this.$refs.HookRef.clearValidate(); // 清除验证信息
    },
     // 列表数据展示
    async getAllHook(){
      this.isLoading=true;
      const response =await this.$api.getHook(this.pro.id)
			if (response.status ===200){
				this.hookList = response.data.result;
				this.pages = response.data
        // 遍历每条记录并处理user_ids字段
       this.hookList.forEach(record => {
          const userIDs = eval(record.user_ids);
          record.user_ids = userIDs;
        });
				console.log(this.hookList)

			}
      this.isLoading=false;

    },
    // 新增接口
    async AddInter(){
      this.$refs.HookRef.validate(async vaild => {
				// 判断是否验证通过，不通过则直接retrue
				if (!vaild) return;
      // 调用接口等逻辑
        const params = {...this.addForm}
        const formattedIds = params.user_ids.map(id => `'${id}'`); // 在每个元素周围添加单引号
        params.user_ids = `[${formattedIds.join(',')}]`; // 将数组转换为字符串，并使用方括号括起来

        const response = await this.$api.createHook(params)
        if (response.status===201) {
          this.$message({
            type: 'success',
            message: '添加成功',
            duration: 1000})

          this.addForm = {
            name: '',
            webhook: '',
            user_ids: [],
            project_id: '',
            testPlan_id: '',

            };
          this.addDlg = false;
          this.getAllHook()
        }
      })
    },
    // 修改接口
    async EditInter(){
      this.$refs.HookRef.validate(async valid => {
        if (!valid) return
        const  params = {...this.editForm}
        const formattedIds = params.user_ids.map(id => `'${id}'`); // 在每个元素周围添加单引号
        params.user_ids = `[${formattedIds.join(',')}]`; // 将数组转换为字符串，并使用方括号括起来
        const response = await  this.$api.updateHook(params.id,params)
        if (response.status===200) {
          this.$message({
            type: 'success',
            message: '修改成功',
            duration: 1000});

          this.editForm = {
            name: '',
            webhook: '',
            user_ids: [],
            project_id: '',
            testPlan_id: '',
            };
          this.editDlg = false;
          this.getAllHook()
        }
      })
    },
    currentPages(currentPage) {
      this.getAllHook(currentPage)
      this.hookList.page = currentPage;

  },

  },

  created() {
  this.getAllHook()
  this.getAllUser()
	}
}


</script>

<style scoped>

.table_data{
  margin:10px;
}
.dialog-footer {
  display: flex;
  justify-content: center;
}
.dialog-footer .el-button:first-child {
  margin-right: 10px;
}
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}


</style>