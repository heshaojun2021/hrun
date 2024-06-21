<template>
  <div class="box">
  <el-scrollbar height="calc(100vh - 80px)">
  <div class="query_model">
    <span>用户名
      <el-input v-model="QueryCondition.username" placeholder="请输入用户名" autocomplete="off" maxlength="30" :clearable="true" :style="{ width: '200px' }"/>
    </span>
    <span>手机号
      <el-input v-model="QueryCondition.mobile" placeholder="请输入手机号码" autocomplete="off" maxlength="30" :clearable="true" :style="{ width: '200px' }"/>
    </span>
    <span>邮箱
      <el-input v-model="QueryCondition.email" placeholder="请输入邮箱" autocomplete="off" maxlength="30" :clearable="true" :style="{ width: '200px' }"/>
    </span>
    <span>所属项目
      <el-input v-model="QueryCondition.project_name" placeholder="请输入项目名称" autocomplete="off" maxlength="30" :clearable="true" :style="{ width: '200px' }"/>
    </span>
			<span class="buttons">
				<el-button @click="resetForm"  icon="el-icon-refresh">重置</el-button>
				<el-button type="primary" @click="submitForm"  icon="el-icon-refresh"> 查询</el-button>
			</span>
  </div>
  <el-button @click="clickAdd"  plain type="success" icon="el-icon-plus" style="margin-bottom: 5px;margin-left:10px">新增</el-button>
  <el-button @click="clickAddPro"  plain type="primary" icon="el-icon-plus" style="margin-bottom: 5px;margin-left:10px">添加其他项目成员</el-button>

  <el-dialog v-model="addProDlg" title="添加其他项目成员"  width="30%" custom-class="class_dialog" :required="true" style="text-align:left" :before-close="clearValidation">
		<el-form :model="addProForm" :rules="rulesUser" ref="UserRef" label-width="80px" style="max-width: 500px">
      <el-form-item label="所属项目" :required="true" style="text-align:left" >
        <el-input v-model="addProForm.project_name" autocomplete="off" disabled/>
      </el-form-item>

      <el-form-item label="选择用户">
				<el-select  multiple v-model="addProForm.users" filterable placeholder="请选择用户" style="width: 100%;">
          <el-option
              :value="iter.id" v-for="iter in usersExclude"
              :label="iter.username"
              :key="iter.id">
          </el-option>
				</el-select>
			</el-form-item>
		</el-form>
		<template #footer>
			<span class="dialog-footer">
        <el-button @click="clearValidation" size="medium">取消</el-button>
				<el-button type="primary" @click="clickExcludeUser" size="medium">确定</el-button>
			</span>
		</template>
	</el-dialog>
  <!--  新增用户弹窗-->
	<el-dialog v-model="addDlg" title="新增用户"  width="30%" custom-class="class_dialog" :required="true" style="text-align:left" :before-close="clearValidation">
		<el-form :model="addForm"  :rules="rulesUser" ref="UserRef" label-width="80px" style="max-width: 500px">
      <el-form-item prop="username" label="用户名">
        <el-input v-model="addForm.username"  maxlength="18" minlength="3" placeholder="请输入用户名" show-word-limit/>
      </el-form-item>
      <el-form-item label="标签">
        <el-input v-model="addForm.weChat_name"  maxlength="50" minlength="1" placeholder="请输入名称"/>
      </el-form-item>
			<el-form-item label="手机号码" prop="mobile">
        <el-input v-model="addForm.mobile"  maxlength="11" minlength="11" placeholder="请输入手机号"/>
      </el-form-item>
      <el-form-item label="邮箱地址"><el-input v-model="addForm.email"  placeholder="请输入邮箱地址" readonly onfocus="this.removeAttribute('readonly');"/></el-form-item>
      <el-form-item label="所属项目" :required="true" style="text-align:left" >
        <el-input v-model="addForm.project_name" autocomplete="off" disabled/>
      </el-form-item>
      <el-form-item clearable :readonly="readonlyInput" label="密码" prop="password" >
        <el-input v-model="addForm.password"  type="password" show-password maxlength="18" minlength="3" placeholder="请输入密码"/>
      </el-form-item>

		</el-form>
		<template #footer>
			<span class="dialog-footer">
				<el-button @click="clearValidation" size="medium">取消</el-button>
				<el-button type="primary" @click="AddInter" size="medium">确定</el-button>
			</span>
		</template>
	</el-dialog>
  <!-- 修改项目的窗口 -->
	<el-dialog v-model="editDlg" title="修改用户" width="30%" custom-class="class_dialog" :required="true" style="text-align:left" :before-close="clearValidation">
		<el-form :model="editForm"  :rules="rulesUser" ref="UserRef" label-width="80px" style="max-width: 500px">
      <el-form-item prop="username" label="用户名">
        <el-input v-model="editForm.username"  maxlength="18" minlength="3" placeholder="请输入用户名" disabled />
      </el-form-item>
      <el-form-item label="标签" >
        <el-input v-model="editForm.weChat_name"  maxlength="50" minlength="1" placeholder="请输入名称"/>
      </el-form-item>
			<el-form-item label="手机号码" prop="mobile">
        <el-input v-model="editForm.mobile"  maxlength="11" minlength="11" placeholder="请输入手机号"/>
      </el-form-item>
      <el-form-item label="邮箱地址"><el-input v-model="editForm.email"  placeholder="请输入邮箱地址" maxlength="30"
       readonly onfocus="this.removeAttribute('readonly');"/></el-form-item>
      <el-form-item label="所属项目" :required="true" style="text-align:left" >
        <el-input v-model="editForm.project_name" autocomplete="off" disabled/>
      </el-form-item>
      <el-form-item v-if="showResetPassword" label="新密码" prop="password" >
        <el-input v-model="editForm.password"  type="password" show-password maxlength="18" minlength="3" placeholder="请输入密码" readonly onfocus="this.removeAttribute('readonly');"/>
      </el-form-item>

		</el-form>
		<template #footer>
			<span class="dialog-footer">
        <el-button  type="primary" @click="resetPassword" >重置密码</el-button>
        <el-button type="primary" @click="UpdateInter" >确定</el-button>
				<el-button @click="clearValidation" >取消</el-button>
			</span>
		</template>
	</el-dialog>
  <div class="table_data">
    <el-table :data="UserLsit"  stripe empty-text="暂无数据"  >
            <el-table-column label="序号" align="center" width="60">
              <template #default="scope">
                <span>{{ scope.$index + 1 }}</span>
              </template>
            </el-table-column>
            <el-table-column label="用户名" prop="username" align="center" />
            <el-table-column label="标签" prop="weChat_name" align="center" />
            <el-table-column label="手机号码" prop="mobile" align="center"/>
            <el-table-column label="邮箱" prop="email" align="center"/>
            <el-table-column label="所属项目"  show-overflow-tooltip align="center">
            <template #default="scope">
              <span v-for="(project, index) in scope.row.project" :key="index">
                {{ project.name }}
                <span v-if="index !== scope.row.project.length - 1">, </span>
              </span>
            </template>
            </el-table-column>
<!--            <el-table-column label="创建时间" align="center">-->
<!--            <template #default="scope">-->
<!--              {{ $tools.rTime(scope.row.date_joined) }}-->
<!--            </template>-->
<!--            </el-table-column>-->
            <el-table-column label="操作" width="180" align="center">
              <template #default="scope">
                <el-button @click="clickEdit(scope.row)" size="mini" plain type="primary" icon="el-icon-edit-outline">编辑</el-button>
                <el-button @click="delUser(scope.row.id)" size="mini" type="danger" plain icon="el-icon-delete">删除</el-button>
              </template>
            </el-table-column>
    </el-table>
  </div>

  <div class="pagination-container">
    <el-pagination  background layout="total, sizes, prev, pager, next, jumper"
                    :page-sizes="[10, 30, 50, 100]"
                    @size-change="sizes"
                    @current-change="currentPages"
                    :total="Pager.count"
                    :current-page="Pager.current"
                   next-text="下一页" prev-text="上一页">
      </el-pagination>
  </div>
  </el-scrollbar>
  </div>
</template>





<script>
import {mapGetters, mapState} from "vuex";

export default {
  data() {
    return {
      UserLsit:"",
      QueryCondition:{
       username:"",
       mobile:"",
       email:"",
       project_name:"",
      },
      Pager:'',
      addDlg: false,
      addForm: {
        username: '',
        mobile: '',
        email: '',
        project_id:'',
        project_name:'',
        password:'',
        weChat_name:""
      },
      editDlg: false,
      editForm: {
        username: '',
        mobile: '',
        email: '',
        project_id:'',
        project_name:'',
        password:'',
        weChat_name:""
      },
      showResetPassword: false,
      addProDlg: false,
      addProForm:{
        project_id:'',
        users:''

      },
      rulesUser: {
        // 验证用户名是否合法
        username: [
          {
            required: true,
            message: '请输入用户名',
            trigger: 'blur'
          }
        ],
        // 验证密码是否合法
        password: [
          {
            required: true,
            message: '请输入密码',
            trigger: 'blur'
          }
        ],
       mobile: [
          {
            required: true,
            message: '请输入手机号',
            trigger: 'blur'
          }
        ]
      },
      readonlyInput: true,
      usersExclude: []
    }
  },
  computed: {
		...mapState(['pro','interfaces']),
    ...mapGetters(['interfaces1', 'interfaces2']),
	},



  methods: {
    cancelReadOnly() {
      this.readonlyInput = false;
    },
    // 列表数据展示
    async getAllUser(page,size){
      const username = this.QueryCondition.username.trim();
      const mobile = this.QueryCondition.mobile.trim();
      const email = this.QueryCondition.email.trim();
      const project_name = this.QueryCondition.project_name.trim();

      // 构造查询参数
      let params = [];
      if (username) {
        params.push(`&username=${encodeURIComponent(username)}`);
      }
      if (mobile) {
        params.push(`&mobile=${encodeURIComponent(mobile)}`);
      }
      if (email) {
        params.push(`&email=${encodeURIComponent(email)}`);
      }
      if (project_name) {
        params.push(`&project_name=${encodeURIComponent(project_name)}`);
      }
      let url = '/users/user/';
      if (page && size) {
      url += `?page=${page}&size=${size}${params.join('')}`;
    }else if (page){
        url += `?page=${page}&size=${size}${params.join('')}`;
      }else if (size){
        url += `?size=${size}${params.join('')}`;
      }

			const response =await  this.$api.getAlluser(url,this.pro.id)
			if (response.status ===200){
				this.UserLsit = response.data.result
        this.Pager = response.data
			}
		},

    async getExcludeUser() {
        const response = await this.$api.getExcludeUser(this.pro.id);
        if (response.status === 200) {
            const userData = response.data;
            this.usersExclude = userData.map(user => {
                return {
                    id: user.id,
                    username: user.username
                };
            });
            console.log('打印：', this.usersExclude)
        }
    },

    async clickExcludeUser() {
      const params = {...this.addProForm}
      const response = await this.$api.addExcludeUser(params)
        if (response.status===200) {
          this.$message({
            type: 'success',
            message: '用户添加成功',
            duration: 1000})
          this.addProDlg = false;
          this.getAllUser(1,this.Pager.size)
          }
    },
    resetForm() {
      // 重置表单逻辑
      this.QueryCondition.username='';
      this.QueryCondition.mobile='';
      this.QueryCondition.email='';
      this.QueryCondition.project_name='';
      console.log(this.interfaces)

    },

    submitForm() {

    this.getAllUser(1,this.Pager.size)

    },

    clickAdd() {
      this.addDlg = true;
      this.addForm = {
				username: '',
				mobile: '',
				email: '',
        password: '',
        project_id:this.pro.id,
        project_name:this.pro.name,
        weChat_name:''

			};
    },
    clickAddPro() {
      this.addProDlg = true;
      this.addProForm = {
        project_id:this.pro.id,
        project_name:this.pro.name,
        users:[]

			};
      this.getExcludeUser()
    },
    clearValidation() {
      this.addDlg = false;
      this.editDlg = false;
      this.addProDlg = false;
      this.showResetPassword = false;
      this.$refs.UserRef.clearValidate();
    },

    AddInter(){
      this.$refs.UserRef.validate(async vaild => {
				// 判断是否验证通过，不通过则直接retrue
				if (!vaild) return;
      // 调用接口等逻辑
        const params = {...this.addForm}
        const response = await this.$api.createUser(params)
        if (response.status===201) {
          this.$message({
            type: 'success',
            message: '用户添加成功',
            duration: 1000})

          this.addForm = {
              username: '',
              mobile: '',
              email: '',
              password: '',
              project_id: '',
              project_name: '',
              weChat_name:''

            };
          this.addDlg = false;
          this.showResetPassword = false;
          this.getAllUser(1,this.Pager.size)
        }
      })
    },

    //修改用户信息
    UpdateInter() {
      this.$refs.UserRef.validate(async valid => {
        if (!valid) return
        const  params = this.editForm
        console.log(params)
        const response = await  this.$api.updateUser(params.id,params)
        if (response.status===200) {
          this.$message({
            type: 'success',
            message: '用户修改成功',
            duration: 1000});

          this.addForm = {
              username: '',
              mobile: '',
              email: '',
              password: '',
              project_id: '',
              project_name: '',
              weChat_name:''

            };
          this.editDlg = false;
          this.showResetPassword = false;
          this.getAllUser(1,this.Pager.size)
        }
      })
    },
    resetPassword() {
      this.showResetPassword = !this.showResetPassword;
      if (this.showResetPassword === false) {
        this.editForm.password = ''
      }

    },

    // 点击修改
		clickEdit(info) {
			this.editDlg = true;
			this.editForm = { ...info };
			this.editForm.project_id = this.pro.id
      this.editForm.project_name = this.pro.name
		},

    // 点击删除
    delUser(id) {
			this.$confirm('此操作将永久删除该用户, 是否继续?', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning'
			})
				.then(async () => {
					// 删除用户
					const response = await this.$api.deleteUser(id)
					if(response.status ===204){
						this.$message({
							type: 'success',
							message: '删除成功!'
						});
						// 刷新页面
						this.getAllUser(1,this.Pager.size)
					}
				})
				.catch(() => {
					this.$message({
						type: 'info',
						message: '已取消删除'
					});
				});
		},
    // 当前页码变化时触发的回调函数
    currentPages(currentPage) {
      this.getAllUser(currentPage,this.Pager.size)
      this.Pager.page = currentPage;
      console.log(currentPage)
  },

    sizes(size) {
      this.getAllUser(1, size);
    }
  },

created() {
		this.getAllUser(1,10)
	}
}
</script>

<style scoped>

.box{
  padding:5px;
}
.query_model{
  height: 70px;
  padding: 20px;
  margin:10px;
  border-radius: 10px;
  background: #ffffff;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
}
.query_model span {
  margin-right: 10px;
}
.buttons {
  float:right;
}

.table_data{
  margin:10px;
}
.dialog-footer {
  display: flex;
  justify-content: center;
}



.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

</style>