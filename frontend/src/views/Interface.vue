<template>
	<div class="title">
		<el-tabs type="card" class="demo-tabs" @tab-click="handleTabClick" v-model="activeName" style="height: calc(100vh - 65px);">
      <div class="query_model">
          <span>接口名称
            <el-input v-model="QueryCondition.name" placeholder="请输入接口名称" autocomplete="off" maxlength="30" :clearable="true" :style="{ width: '200px' }"/>
          </span>
          <span>请求类型
            <el-input v-model="QueryCondition.method" placeholder="请输入请求类型" autocomplete="off" maxlength="30" :clearable="true" :style="{ width: '200px' }"/>
          </span>
          <span>接口地址
            <el-input v-model="QueryCondition.url" placeholder="请输入接口地址" autocomplete="off" maxlength="30" :clearable="true" :style="{ width: '200px' }"/>
          </span>

            <span class="buttons">
              <el-button @click="resetForm"  icon="el-icon-refresh">重置</el-button>
              <el-button type="success" @click="submitForm"  icon="el-icon-refresh"> 查询</el-button>
            </span>
      </div>
      <!--  // 项目接口页签-->
      <el-tab-pane label="项目接口" name="first">
				<el-button @click="clickAdd"  plain type="success" icon="el-icon-plus" style="margin-bottom: 5px;">添加接口</el-button>
				<el-table :data="interfaceData.result"  empty-text="暂无数据" v-loading="isLoading" >
          <el-table-column label="序号" align="center" width="60">
            <template #default="scope">
              <span>{{ scope.$index + 1 }}</span>
            </template>
          </el-table-column>
					<el-table-column label="接口名称" prop="name" align="center"/>
					<el-table-column label="请求类型"  align="center" width="100" >
            <template #default="scope">
              <div style="font-weight: bold">
              <span v-if="scope.row.method === 'POST'">
                  <el-tag  color="#49cc90" size="large">{{ scope.row.method }}</el-tag>
              </span>
              <span v-if="scope.row.method === 'GET'">
                <el-tag  color="#61affe" size="large">{{ scope.row.method}}</el-tag>
              </span>
              <span v-if="scope.row.method === 'PUT'">
                <el-tag  color="#fca130" size="large">{{ scope.row.method}}</el-tag>
              </span>
              <span v-if="scope.row.method === 'PATCH'">
                <el-tag   color="#50e3c2" size="large">{{ scope.row.method}}</el-tag>
              </span>
              <span v-if="scope.row.method === 'DELETE'">
                <el-tag  color="#f56c6c" size="large">{{ scope.row.method}}</el-tag>
              </span>
              <span v-if="scope.row.method === 'DEAD'">
                <el-tag   color="rgb(201, 233, 104)" size="large">{{ scope.row.method}}</el-tag>
              </span></div>

				  </template>
          </el-table-column>
					<el-table-column label="接口地址" prop="url" show-overflow-tooltip align="center"/>
            <el-table-column label="创建时间" align="center">
            <template #default="scope">
              {{ $tools.rTime(scope.row.create_time) }}
            </template>
            </el-table-column>
					<el-table-column label="操作"  align="center">
						<template #default="scope">
							<el-button @click="clickEdit(scope.row)" size="mini" plain type="success" icon="el-icon-edit-outline">编辑</el-button>
							<el-button @click="clickDel(scope.row.id)()" size="mini" type="danger" plain icon="el-icon-delete">删除</el-button>
						</template>
					</el-table-column>
				</el-table>
			</el-tab-pane>

      <!--  // 外部接口页签-->
			<el-tab-pane label="外部接口"  name="second">
				<el-button @click="clickAdd"  plain type="success" icon="el-icon-plus" style="margin-bottom: 5px;">添加接口</el-button>
				<el-table :data="interfaceData.result"  empty-text="暂无数据" v-loading="isLoading" >
          <el-table-column label="序号" align="center" width="60">
            <template #default="scope">
              <span>{{ scope.$index + 1 }}</span>
            </template>
          </el-table-column>
					<el-table-column label="接口名称" prop="name" align="center"/>
          <el-table-column label="请求类型"  align="center" width="100" >
            <template #default="scope">
              <div style="font-weight: bold">
              <span v-if="scope.row.method === 'POST'">
                  <el-tag  color="#49cc90" size="large">{{ scope.row.method }}</el-tag>
              </span>
              <span v-if="scope.row.method === 'GET'">
                <el-tag  color="#61affe" size="large">{{ scope.row.method}}</el-tag>
              </span>
              <span v-if="scope.row.method === 'PUT'">
                <el-tag  color="#fca130" size="large">{{ scope.row.method}}</el-tag>
              </span>
              <span v-if="scope.row.method === 'PATCH'">
                <el-tag   color="#50e3c2" size="large">{{ scope.row.method}}</el-tag>
              </span>
              <span v-if="scope.row.method === 'DELETE'">
                <el-tag  color="#f93e3e" size="large">{{ scope.row.method}}</el-tag>
              </span>
              <span v-if="scope.row.method === 'DEAD'">
                <el-tag color="rgb(201, 233, 104)" size="large">{{ scope.row.method}}</el-tag>
              </span>
              </div>
				  </template>
          </el-table-column>
					<el-table-column label="接口地址" prop="url" show-overflow-tooltip align="center"/>
          <el-table-column label="创建时间" align="center">
            <template #default="scope">
              {{ $tools.rTime(scope.row.create_time) }}
            </template>
          </el-table-column>
					<el-table-column label="操作"  align="center">
						<template #default="scope">
							<el-button @click="clickEdit(scope.row)" size="mini" plain type="success" icon="el-icon-edit-outline">编辑</el-button>
							<el-button @click="clickDel(scope.row.id)()" size="mini" type="danger" plain icon="el-icon-delete">删除</el-button>
						</template>
					</el-table-column>
				</el-table>
			</el-tab-pane>
      <div class="demo-pagination-block">
        <el-pagination background layout="total, sizes, prev, pager, next, jumper"
                    :page-sizes="[10, 30, 50, 100]"
                    @size-change="sizes"
                    @current-change="currentPages"
                    :total="interfaceData.count"
                    :current-page="interfaceData.current"
                   next-text="下一页" prev-text="上一页">
        </el-pagination>
      </div>
		</el-tabs>
	</div>

	<!-- 添加项目的窗口 -->
	<el-dialog v-model="addDlg" title="添加接口" width="40%" :before-close="clickClear">
		<el-form :model="addForm" :rules="rulesinterface" ref="interfaceRef">
			<el-form-item label="接口名称" prop="name"><el-input  v-model="addForm.name" autocomplete="off" placeholder="请输入接口名称" /></el-form-item>
			<el-form-item label="URL地址" prop="url">
        <el-input  v-model="addForm.url" autocomplete="off" placeholder="请输入接口">
        <template #prepend>
          <span v-if='this.envUrl.length<25'>{{this.envUrl}}</span>
          <el-tooltip v-else effect="dark" :content="this.envUrl" placement="top-start"><span>{{this.envUrl.slice(0,12)}}...</span></el-tooltip>
        </template>
        </el-input>
      </el-form-item>
			<el-form-item label="请求类型" prop="method">
				<el-select style="width: 100%;" v-model="addForm.method" class="m-2" placeholder="请选择请求类型" >
					<el-option label="GET" value="GET" />
					<el-option label="POST" value="POST" />
					<el-option label="PUT" value="PUT" />
					<el-option label="PATCH" value="PATCH" />
					<el-option label="DELETE" value="DELETE" />
					<el-option label="DEAD" value="DEAD" />
				</el-select>
			</el-form-item>
			<el-form-item label="接口类型" prop="type">
				<el-select style="width: 100%;" v-model="addForm.type" class="m-2" placeholder="请选择接口" >
					<el-option label="项目接口" value="1" />
					<el-option label="第三方接口" value="2" />
				</el-select>
			</el-form-item>
		</el-form>
		<template #footer>
			<span class="dialog-footer">
				<el-button @click="clickClear" >取消</el-button>
				<el-button type="success" @click="addInter" >确定</el-button>
			</span>
		</template>
	</el-dialog>

	<!-- 修改项目的窗口 -->
	<el-dialog v-model="editDlg" title="修改接口" width="40%" :before-close="clickClear">
		<el-form :model="editForm" :rules="rulesinterface" ref="interfaceRef">
			<el-form-item label="接口名称" prop="name">
        <el-input v-model.trim="editForm.name" autocomplete="off" />
      </el-form-item>
			<el-form-item label="URL地址" prop="url">
        <el-input  v-model="editForm.url" autocomplete="off" placeholder="请输入接口">
          <template #prepend>
            <span v-if='this.envUrl.length<25'>{{this.envUrl}}</span>
            <el-tooltip v-else effect="dark" :content="this.envUrl" placement="top-start"><span>{{this.envUrl.slice(0,12)}}...</span></el-tooltip>
          </template>
        </el-input>
      </el-form-item>
			<el-form-item label="请求类型" prop="method">
				<el-select style="width: 100%;" v-model="editForm.method" class="m-2" placeholder="请求选择请求类型" size="large">
					<el-option label="GET" value="GET" />
					<el-option label="POST" value="POST" />
					<el-option label="PUT" value="PUT" />
					<el-option label="PATCH" value="PATCH" />
					<el-option label="DELETE" value="DELETE" />
					<el-option label="DEAD" value="DEAD" />
				</el-select>
			</el-form-item>
			<el-form-item label="接口类型" prop="type">
				<el-select style="width: 100%;" v-model="editForm.type" class="m-2" placeholder="选择接口" size="large">
					<el-option label="项目接口" value="1" />
					<el-option label="第三方接口" value="2" />
				</el-select>
			</el-form-item>
		</el-form>
		<template #footer>
			<span class="dialog-footer">
				<el-button @click="clickClear" >取消</el-button>
				<el-button type="success" @click="updateInter" >确定</el-button>
			</span>
		</template>
	</el-dialog>


</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex';
import { ElMessage, ElMessageBox } from 'element-plus';
export default {
	data() {
		return {
      rulesinterface: {
				// 验证名称是否合法
				name: [
					{
						required: true,
						message: '请输入接口名称',
						trigger: 'blur'
					}
				],
				// 验证环境是否合法
				url: [
					{
						required: true,
						message: '请输入接口信息',
						trigger: 'blur'
					}
				],
       method: [
					{
						required: true,
						message: '请选择请求类型',
						trigger: 'blur'
					}
				],
       type: [
					{
						required: true,
						message: '请选择接口类型',
						trigger: 'blur'
					}
				]
			},
      activeName: 'first',
      QueryCondition:{
       name:"",
       method:"",
       url:""
      },
      isLoading:'',
      interfaceData:'',
      tabIndex:'',
      envUrl:'',
			addDlg: false,
			addForm: {
				name: '',
				url: '',
				method: '',
				type: null,
				project: ''
			},
			editDlg: false,
			editForm: {
				name: '',
				url: '',
				method: '',
				type: null,
				project: ''
			}
		};
	},
	computed: {
		...mapState(['pro',"envId",'interfaces']),
		...mapGetters(['interfaces1', 'interfaces2']),
	},
	methods: {
		...mapActions(['getAllInter']),

    handleTabClick(tab) {
		   if (tab.index === '0') {
        this.allInterface(1,1,this.interfaceData.size)
         this.tabIndex=1;
      } else {
        this.allInterface(2,1,this.interfaceData.size)
         this.tabIndex=2;
      }
      },
		// 点击添加
		clickAdd() {
		  this.checkEnvDetail()
			this.addDlg = true;
			this.addForm = {
				name: '',
				url: '',
				method: '',
				type: null,
				project: this.pro.id
			};
		},
		// 点击修改
		clickEdit(info) {
		  this.checkEnvDetail()
			this.editDlg = true;
			this.editForm = { ...info };
		},
    // 点击取消
    clickClear(){
		  this.editDlg = false;
		  this.addDlg = false;
		  this.$refs.interfaceRef.clearValidate(); // 清除验证信息
    },

    // 点击重置
    resetForm() {
      this.QueryCondition.name='';
      this.QueryCondition.method='';
      this.QueryCondition.url='';
    },

    // 点击查询
    submitForm(){
		  this.allInterface()
    },
		// 点击删除
		clickDel(id) {
			ElMessageBox.confirm('确定要删除该接口吗?', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning'
			})
				.then(() => {
					this.delInter(id);
				})
				.catch(() => {
					ElMessage({
						type: 'info',
						message: '取消删除',
						duration: 1000
					});
				});
		},
    // 列表接口
    async allInterface(type=1,page,size){
      this.isLoading=true;
      const name = this.QueryCondition.name.trim();
      const method = this.QueryCondition.method.trim();
      const url = this.QueryCondition.url.trim();
        // 检查查询条件是否为空
      let params = {};
      if (name !== "") {
        params.name = name;
      }
      if (method !== "") {
        params.method = method;
      }
      if (url !== "") {
        params.url = url;
      }
		  const response =await  this.$api.getInterfaces(this.pro.id,type,page,size,params.name,params.method,params.url)
			if (response.status ===200){
        this.interfaceData = response.data
			}
      this.isLoading=false;
    },

		// 添加接口
		async addInter() {
		  this.$refs.interfaceRef.validate(async vaild => {
        // 判断是否验证通过，不通过则直接retrue
        if (!vaild) return;
        const response = await this.$api.createInterface(this.addForm);
        if (response.status === 201) {
          ElMessage({
            type: 'success',
            message: '添加成功',
            duration: 1000
          });
          this.addDlg = false;
          this.allInterface(this.tabIndex);
        }
      })
		},
		// 修改接口信息
		async updateInter() {
		  this.$refs.interfaceRef.validate(async vaild => {
        // 判断是否验证通过，不通过则直接retrue
        if (!vaild) return;
        const response = await this.$api.updateInterface(this.editForm.id, this.editForm);
        if (response.status === 200) {
          ElMessage({
            type: 'success',
            message: '修改成功',
            duration: 1000
          });
          this.editDlg = false;
          this.allInterface(this.tabIndex);
        }
      })
		},
		// 删除接口
		async delInter(id) {
			const response = await this.$api.delInterface(id);
			if (response.status === 204) {
				ElMessage({
					type: 'success',
					message: '删除成功',
					duration: 1000
				});
				this.allInterface(this.tabIndex);
			}
		},
    // 获取环境url信息
    async checkEnvDetail() {
			const response = await this.$api.getEnvInfo(this.envId,this.pro.id);
			if (response.status === 200) {
				this.envUrl = response.data.debug_global_variable.host;
			}
		},
        // 当前页码变化时触发的回调函数
  currentPages(currentPage) {
      this.allInterface(this.tabIndex,currentPage,this.interfaceData.size)
      this.interfaceData.page = currentPage;
  },

  sizes(size) {
    setTimeout(() => {
      this.allInterface(this.tabIndex,1, size);
    }, 500); // 设置延迟时间为 1000 毫秒（1秒）
    }
	},

created() {
    this.allInterface();
    this.tabIndex = 1;
	}
};
</script>

<style scoped>

.query_model{
  height: 40px;
  padding: 20px;
  margin: 1px 3px 10px 3px;
  border-radius: 10px;
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.2);
}
.query_model span {
  margin-right: 20px;
}
.buttons {
  float:right;
  /*float:right;*/
}
.title {
  margin:10px;
}
.demo-pagination-block{
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
.el-tag {
  color: #ffffff;
  width:60px;
  text-align: center;

}
</style>
