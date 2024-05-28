<template>
  <div class="box">
    <el-scrollbar height="100vh">
    <el-backtop :right="100" :bottom="100" />
    <el-card shadow="never" style="margin-bottom: 20px; height: 120px">
      <el-row :gutter="20">
        <el-col :span="12">
          <div style="align-items: center;display: flex;cursor: pointer">
          <icon :icon="avatar" class="avatar"></icon>
            <div>
              <div style="font-size:20px">
                {{username}},{{greeting()}}
              </div>
              <div class="text-gray">
                今天晴，20℃ - 32℃！
              </div>
            </div>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="projectinfo">
            <div style="text-align: right;padding-left: 8px; padding-right: 8px;">
              <div class="projectinfo_cs">参与项目</div>
              <countTo
                  style="font-size:20px; text-align:right;"
                  :start-val="0"
                  :end-val="32"
                  :duration="2600">

              </countTo>
            </div>
            <el-divider direction="vertical" />
            <div style="text-align: right;padding-left: 8px; padding-right: 8px;">
              <div class="projectinfo_cs">用例数量</div>
              <countTo
                  style="font-size:20px; text-align:right;"
                  :start-val="0"
                  :end-val="99"
                  :duration="2600">

              </countTo>
            </div>
            <el-divider direction="vertical" border-style="dashed" />
            <div style="text-align: right;padding-left: 8px; padding-right: 8px;">
              <div class="projectinfo_cs">项目访问</div>
              <countTo
                  style="font-size:20px; text-align:right;"
                  :start-val="0"
                  :end-val="53233"
                  :duration="2600">

              </countTo>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <el-row  :gutter="20" style="  justify-content: flex-end;">
      <el-col :span="16" style="margin-bottom: 20px">
        <el-card shadow="never" style="margin-bottom: 20px">
          <template #header>
            <div style="justify-content: space-between; display: flex;">
              <span>项目</span>
              <el-dropdown @command="handleCommand">
              <span class="example-showcase" type="primary">
                操作
                <el-icon class="el-icon--right">
                  <arrow-down />
                </el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command='create'>新增项目</el-dropdown-item>
                  <el-dropdown-item command='update'>修改项目</el-dropdown-item>
                  <el-dropdown-item command='delete'>删除项目</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
            </div>
          </template>
          <el-row>
            <el-col :span="8" v-for="item in pro_list" :key="item.id">
               <el-tooltip
                  effect="light"
                  content="点击项目有惊喜噢"
                  placement="top"
                >
              <el-card class="custom-card" shadow="hover" >
              <el-checkbox-group v-model="checkList">
              <el-checkbox
                  @change="statusChange"
                  @click="clickEdit(item)"
                  style="display: flex;
                  float:right;
                  margin-top: -10px"
                  :label="item.id">
                 <span style="display: none;">{{ item.id }}</span>
              </el-checkbox></el-checkbox-group>

               <div @click="clickView(item)" >
                <div style="align-items: center;display: flex">
                  <icon
                    :icon="item.icon"
                    font-size="25"
                    style="margin-right:10px;"></icon>
                  <span class="text-16px">{{ item.name }}</span>
                </div>
                <div class="message">{{ item.desc }}</div>
                <div class="projectinfo_user_time">
                  <span>{{ item.leader }}</span>
                  <span>{{ $tools.rDate(item.create_time) }}</span>
                 </div>
                </div>
              </el-card>
              </el-tooltip>
            </el-col>
          </el-row>
          	<!-- 添加项目的弹框 -->
            <el-dialog v-model="addDlg" title="添加项目" width="35%" :before-close="clearValidation">
              <el-form :model="addForm" :rules="rulesPro" ref="UserRef">
                <el-form-item label="项目名" prop="name">
                  <el-input  v-model="addForm.name" autocomplete="off" maxlength="30" clearable="true"/>
                </el-form-item>
                <el-form-item label="项目描述" prop="desc">
                  <el-input v-model="addForm.desc" show-word-limit type="textarea" maxlength="30"/>
                </el-form-item>
              </el-form>
              <template #footer>
                <span class="dialog-footer">
                  <el-button @click="clearValidation" size="mini">取消</el-button>
                  <el-button type="primary" @click="addPro" size="mini">确定</el-button>
                </span>
              </template>
            </el-dialog>
          	<!-- 修改项目 -->
	          <el-dialog v-model="updateDlg" title="修改项目" width="35%" :before-close="clearValidation">
              <el-form :model="updateForm" :rules="rulesPro" ref="UserRef">
                <el-form-item label="项目名" prop="name"><el-input v-model="updateForm.name" autocomplete="off" maxlength="30" clearable="true"/></el-form-item>
                <el-form-item label="项目描述" prop="desc"><el-input v-model="updateForm.desc" show-word-limit type="textarea" maxlength="30"/></el-form-item>
              </el-form>
              <template #footer>
                <span class="dialog-footer">
                  <el-button  @click="clearValidation" size="mini">取消</el-button>
                  <el-button type="primary" @click="updatePro" size="mini">确定</el-button>
                </span>
              </template>
            </el-dialog>
        </el-card>

        <el-card shadow="never" style="margin-bottom: 20px" >
          <template #header>
            <div style="justify-content: space-between;display: flex;">
              <span>最新动态</span>
              <el-link type="primary" :underline="false">更多</el-link>
            </div>
          </template>
          <div v-for="item in dynamics" :key="item.id">
            <div style=" align-items: center; display: flex">
              <img
                src="@/assets/images/user/user.png"
                alt=""
                class="avatarpro"
              />
              <div>
                <span style="font-size: 14px;margin-left: 20px;color: #409eff">{{ item.name }}</span>
                <span style="font-size: 14px;margin-left: 3px">{{ item.content }}</span>
                <div class="dynamicinfo">
                  {{ item.time }}
                </div>
              </div>
            </div>
            <el-divider />
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card shadow="never" style="margin-bottom: 20px">
          <template #header>
            <span>快捷导航</span>
          </template>
          <el-row>
            <el-col
              v-for="item in shortcut"
              :key="item.id"
              :span="8"
            >
            <el-card shadow="hover">
            <span style="align-items: center;flex-direction: column;box-sizing: border-box;display: flex;outline: none;">
              <Icon :icon="item.icon"  style="font-size: 25px" />
              <span style="overflow: hidden;text-overflow: ellipsis;white-space: nowrap;
                  margin-top: 0.5rem;box-sizing: border-box;outline: none"><el-link  :underline="false" @click="item.click">
                {{ item.name }}</el-link></span>
              </span>
            </el-card>
            </el-col>
          </el-row>
        </el-card>

        <el-card shadow="never" style="margin-bottom: 20px">
          <template #header>
            <span>最近7天编写用例数量</span>
          </template>
          <RadarChart></RadarChart>
        </el-card >

        <el-card shadow="never" style="margin-bottom: 90px">
          <template #header>
            <span>团队</span>
          </template>
          <el-row>
            <el-col v-for="item in team" :key="item.name" :span="12" style="margin-bottom: 20px">
              <div style=" align-items: center; display: flex">
                <icon :icon="item.icon"  style="margin: 10px;" />
                <el-link type="default" :underline="false">
                  {{ item.name }}
                </el-link>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
  </el-scrollbar>
  </div>
</template>

<script >
import { ElCard, ElRow, ElCol, ElDivider, ElLink, ElMessage, ElMessageBox } from 'element-plus';
import { Icon } from '@iconify/vue'
import RadarChart from '../../components/echart/RadarChart.vue'
import { mapMutations } from 'vuex';
import countTo from '../../components/to'
export default {
  components: {
    ElCard, ElRow, ElCol,
    ElDivider, ElLink, Icon,
    RadarChart, ElMessage, ElMessageBox,
    countTo
  },
  data() {
    return {
      icons: [
        {
          id: 1,
          icon: 'logos:github-icon',
        },
        {
          id: 2,
          icon: 'logos:baker-street',

        },
        {
          id: 3,
          icon: 'cryptocurrency-color:xpr',
        },
        {
          id: 4,
          icon: 'cryptocurrency-color:ethos',
        },
        {
          id: 5,
          icon: 'cryptocurrency-color:sc',
        },
        {
          id: 6,
          icon: 'logos:nocodb',
        },
        {
          id: 7,
          icon: 'logos:web-dev-icon',
        },
        {
          id: 8,
          icon: 'cryptocurrency-color:gxs',
        },
        {
          id: 9,
          icon: 'cryptocurrency-color:one',

        },
        {
          id: 10,
          icon: 'cryptocurrency-color:powr',
        },
        {
          id: 11,
          icon: 'cryptocurrency-color:uni',
        },
        {
          id: 12,
          icon: 'cryptocurrency-color:waves',
        },
        {
          id: 13,
          icon: 'cryptocurrency-color:atom',
        },
        {
          id: 14,
          icon: 'cryptocurrency-color:sky',
        },
      ],
      dynamics: [
        {
          id: 1,
          name:'admin',
          content: '查看了测试报告',
          time: '2小时前',
        },
        {
          id: 2,
          name:'小明',
          content: '提交了bug',
          time: '一天前',
        },
        {
          id: 3,
          name:'小泊',
          content: '修改了登录接口',
          time: '三天前',
        },
        {
          id: 4,
          name:'小泊',
          content: '新增了接口',
          time: '七天前',
        },
        {
          id: 5,
          name:'小文',
          content: '执行了测试计划',
          time: '七天前',
        },
        {
          id: 6,
          name:'猴哥',
          content: '新增了定时任务',
          time: '七天前',
        },
      ],
      radarOptionData: {}, // echart数据
      team:[
        { name: '团队A', icon: 'logos:web-dev-icon' },
        { name: '团队B', icon: 'logos:github-icon' },
        { name: '团队C', icon: 'cryptocurrency-color:sc' },
        { name: '团队D', icon: 'cryptocurrency-color:sc' }
        // 其他团队...
      ],
      shortcut:[
        { id:1,name: '退出登录', icon: 'logos:google-360suite', click:this.logout },
        { id:2,name: '接口测试', icon: 'logos:github-icon' },
        { id:3,name: '性能测试', icon: 'logos:web-dev-icon' },
        { id:4,name: '测试计划', icon: 'logos:async-api-icon' },
        { id:5,name: '测试报告', icon: 'cryptocurrency-color:sc' },
      ],
      pro_list: [],
      checkList:[],
			// 添加项目
			addDlg: false,
			addForm: {
				name: '',
				desc: ''
			},
			// 修改项目
			updateDlg: false,
			updateForm: {
				name: '',
				desc: ''
			},
      rulesPro: {
				// 验证用户名是否合法
				name: [
					{
						required: true,
						message: '请输入项目名称',
						trigger: 'blur'
					}
				],
				// 验证密码是否合法
				desc: [
					{
						required: true,
						message: '请输入项目描述',
						trigger: 'blur'
					}
				],}

    };
  },
 	methods: {
		...mapMutations(['selectPro']),

    statusChange(value){
            if(this.checkList.length > 1){
                this.checkList.splice(0,1)
            }},

		async getAllPro() {
			const response = await this.$api.getProjects();
			  if (response.status === 200) {
          const dataWithIcon = response.data.map((item, index) => ({...item,
          icon: this.icons[index % this.icons.length].icon // 取 icons 列表中的 icon，循环使用
          }));
          this.pro_list = dataWithIcon;
        }
		},
		// 点击进入项目
		clickView(pro) {
			// 将选中的项目信息保存的vuex
			this.selectPro(pro);
			// 路由跳转
			this.$router.push({ name: 'home' });
		},
    handleCommand(types){
    if (types === 'create'){
      this.addForm = {
				name: '',
				desc: ''
			};
      this.addDlg = true;
    }
    else if (types === 'update'){
      if (!this.updateForm.id || this.checkList.length === 0) {
          this.$message({
            message: '请勾选项目后再操作！',
            type: 'warning',
            duration: 1000
          });
          return;
        }
			this.updateDlg = true;
    }
    else {
      if (!this.updateForm.id || this.checkList.length === 0) {
          this.$message({
            message: '请勾选项目后再操作！',
            type: 'warning',
            duration: 1000
          });
          return;
        }
      if (types === 'delete'){
      ElMessageBox.confirm('确定要删除该项目吗?', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning'
			})
				.then(() => {
					this.deletePro(this.updateForm.id);
					this.updateForm = false
          this.checkList=[];
				})
				.catch(() => {
					ElMessage({
						type: 'info',
						message: '取消删除'
					});
					this.checkList=[];
				})}


    }
    },
		// 点击添加项目按钮
		clickAdd() {
			// 将添加表单置空
			this.addForm = {
				name: '',
				desc: ''
			};
			// 显示模态框
			this.addDlg = true;
		},
		// 点击编辑项目按钮
		clickEdit(info) {
			this.updateForm = { ...info };
		},
		// 添加项目
		async addPro() {
      this.$refs.UserRef.validate(async vaild => {
				// 判断是否验证通过，不通过则直接retrun
				if (!vaild) return;
			const response = await this.$api.createProjects(this.addForm);
			if (response.status === 201) {
				this.$message({
					message: '添加成功!',
					type: 'success',
					duration: 1000
				});
				// 刷新页面数据
				this.getAllPro();
				this.addDlg = false;
				this.checkList = [];
			}})
		},
		// 修改项目
		async updatePro() {
      this.$refs.UserRef.validate(async vaild => {
				// 判断是否验证通过，不通过则直接retrue
				if (!vaild) return;
			const response = await this.$api.updateProjects(this.updateForm.id, this.updateForm);
			if (response.status === 200) {
				this.$message({
					message: '修改成功!',
					type: 'success',
					duration: 1000
				});
				// 刷新页面数据
				this.getAllPro();
				this.updateDlg = false;
				this.checkList = [];
			}})
		},
		// 删除项目
		async deletePro(id) {
			const response = await this.$api.delProject(id);
			if (response.status === 204) {
				this.$message({
					message: '删除成功',
					type: 'success',
					duration: 1000
				});
				this.getAllPro();
			}
		},
		// 退出登录
		logout() {
			this.$message({
				message: '已注销登录状态',
				type: 'warning',
				duration: 1000
			});
			window.sessionStorage.removeItem('token');
			window.sessionStorage.removeItem('username');
      window.sessionStorage.removeItem('avatar');
			this.$router.push({ name: 'login' })
		},
    clearValidation() {
      this.addDlg = false;
      this.updateDlg = false;
      this.showResetPassword = false;
      this.checkList = [];
      this.$refs.UserRef.clearValidate(); // 清除验证信息
    },
    greeting(){
		  // 获取当前时间的小时数
      const currentHour = new Date().getHours();
      // 定义问候语
      let greeting = '';

      if (currentHour >= 0 && currentHour < 8) {
        greeting = '早上好！今天是全新的一天，让我们充满活力地开始吧！';
      } else if (currentHour >= 8 && currentHour < 12) {
        greeting = '上午好！加油！有计划地完成任务，让每一分钟都值得！';
      } else if (currentHour >= 12 && currentHour < 18) {
        greeting = '下午好！继续保持精神和积极的态度，目标就在前方！';
      } else {
        greeting = ' 晚上好！给自己一份轻松，给家人一份关爱，明天即将到来，期待更美好的一天！';
      }
      return greeting
    }
	},
  computed: {
		username() {
			return window.sessionStorage.getItem('username');
		},
    avatar() {
		  return window.sessionStorage.getItem('avatar');
    }
	},
	created() {
		this.getAllPro();
	}
};
</script>

<style scoped>
.box{
  padding:20px;
  background:#f5f7f9
}
.avatar{
  width: 70px;
  height: 70px;
  margin: 20px;
  margin-top: 10px;
  margin-bottom: 10px;
  margin-left: 1px;
  border-radius: 50%;
}
.avatarpro{
  width: 35px;
  height: 35px;
  border-radius: 50%;
}
.text-gray{
  --un-text-opacity: 1;
  color: rgb(107 114 128 / var(--un-text-opacity));
  font-size: 14px;
  margin-top: 10px;

}
.projectinfo{
  justify-content: flex-end;
  align-items: center;
  display: flex;
  height: 85px;
}
.projectinfo_cs{
  --un-text-opacity: 1;
  color: rgb(156 163 175 / var(--un-text-opacity));
  font-size: 14px;
  margin-bottom: 20px;
}
.el-link.el-link--primary {
    color: #66b1ff;
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
.dynamicinfo{
    --un-text-opacity: 1;
    color: rgb(156 163 175 / var(--un-text-opacity));
    font-size: 12px;
    margin-top: 15px;
    margin-left: 20px
}
.el-row {
cursor: pointer;
}
.example-showcase{
  cursor: pointer;
  color: var(--el-color-primary);
  display: flex;
  align-items: center;
}

.custom-card {
  margin: 2px;
  background-color: #ffffff; /* 设置背景色 */
  border-radius: 8px; /* 设置圆角 */
  border: 2px solid #ddd; /* 设置边框 */
  overflow: hidden; /* 隐藏溢出内容 */
}

.custom-card:hover {
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3); /* 设置鼠标悬停时的阴影效果 */
}
</style>
