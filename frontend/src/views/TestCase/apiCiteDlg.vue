<template>
  <el-dialog v-model="addApiDlg" title="引用接口" width="88%" :before-close="clickClear" top="0">
  <el-row :gutter="10">
    <!-- 左边内容 -->
    <el-col :span="6">
      <treeNode @treeClick="handleTreeClick" :handleTreeClick="handleTreeClick"></treeNode>
    </el-col>
    <!-- 右边内容 -->
    <el-col :span="18">
      <el-row :gutter="1" style="margin-bottom: 20px;">
        <div style="margin-top: 20px">
          <el-input style="width: 400px" v-model="filterText" placeholder="请输入接口名称进行搜索" clearable>
            <template #append>
              <el-button type="primary" @click="handlenewInterfacesClick">查询</el-button>
            </template>
          </el-input>
          <div>
            <el-button
              type="primary"
              style="margin-bottom: 20px;margin-top: 40px;margin-right: 10px"
              @click="userInterface"
              icon="el-icon-view"
                >{{buttonText}}
            </el-button>
            <el-button
              type="primary"
              style="margin-bottom: 20px;margin-top: 40px;margin-right: 10px"
              icon="el-icon-star-off"
              @click="dialogVisible = true"
                >选择环境
            </el-button>
            <el-dialog v-model="dialogVisible" width="30%" title="选择环境">
              <el-form :rules="rulesinterface" ref="interfaceRef" >
                <el-form-item label="测试环境" prop="env">
                  <el-select v-model.lazy="selectedEnvironment" placeholder="请选择环境" style="width: 70%;" no-data-text="暂无数据">
                    <el-option v-for="item in testEnvs" :key="item.id" :label="item.name" :value="item.id">
                    </el-option>
                  </el-select>
                </el-form-item>
              </el-form>
              <template #footer>
              <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取消</el-button>
                <el-button type="primary" @click="confirmSelection">确定</el-button>
              </span>
              </template>
            </el-dialog>

            <span style="margin-bottom: 20px;margin-top: 40px;margin-right: 30px;font-size: 14px;color: #909399">当前环境：
              <el-button
                  type="info"
                  disabled
                  plain
                  >{{selectedEnvironmentName}}</el-button>
            </span>
            <el-button
              type="warning"
              style="margin-bottom: 20px;margin-top: 40px;float: right;"
              @click="clickClear"
              icon="el-icon-close"
                >关闭窗口
            </el-button>
            <el-button
              type="primary"
              style="margin-bottom: 20px;margin-top: 40px;float: right;margin-right: 15px"
              @click="handleApiClick"
              icon="el-icon-check"
                >确认选择
            </el-button>
          </div>
          <div class="interface-title">全部接口共 ({{interfaceCount}}) 个</div>
          <el-scrollbar height="calc(100vh)">
            <el-card :body-style="{ width: 'calc(100vh + 210px)'}">
           <el-row>
            <el-col :span="24">
              <el-table
                ref="multipleTable"
                :data="tableData"
                row-key="ID"
                :cell-style="{ paddingTop: '4px', paddingBottom: '4px' }"
                :selectable="selectionConfig"
                @selection-change="handleSelectionChange"
              >
              <el-table-column  type="selection"></el-table-column>
              <el-table-column align="center" >
              <template #default="scope">
                <el-card :style='getRowClassName(scope.row.method)'>
                  <el-col :span="20">
                    <div class="style">
                  <span slot="header" class="card-title">
                  <div style="font-weight: bold;margin-top: -9px">
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
                    <b class="card-url">{{ scope.row.url }}</b>
                    <span class="card-name">{{ scope.row.name }}</span>
                    </span>
                    </div>
                    </el-col>
                    <el-col :span="4">
                    <span class="card-content" >
                    <el-button
                      type="text"
                      size="small"
                      class="card-button"
                      @click="clickEditStep(scope.row.id)"
                    >
                      调试
                    </el-button>
                    <el-button
                      type="text"
                      size="small"
                      class="card-button"
                      @click="clickCopy(scope.row.id)"
                    >
                      复制
                    </el-button>
                    <el-button
                      type="text"
                      size="mini"
                      @click="clickDel(scope.row.id)"
                    >
                      删除
                    </el-button>
                    <el-button
                      type="text"
                      size="small"
                      class="card-button"
                      @click="clickLog"
                    >
                      操作记录
                    </el-button>
                    </span>
                    </el-col>
                </el-card>
              </template>
            </el-table-column>
          </el-table>
        </el-col>
      </el-row>
    </el-card>
          </el-scrollbar>
    </div>
    </el-row>
    </el-col>
  </el-row>
  </el-dialog>
	<!-- 编辑测试步骤窗口 -->
  <el-drawer v-model="editCaseDlg"   :with-header="false" size="50%"><newEditCase ref="childRef" @closeDrawer="handleClose"  :Interface_id="Interface_id" :copyDlg="copyDlg"  style="padding: 0 10px;"></newEditCase></el-drawer>
  <!--  接口操作记录窗口-->
  <el-drawer v-model="logDlg"   :with-header="false" size="50%">
    <el-card>
				<b>接口操作记录</b>
				<div style="margin-top: 10px;">
					<el-timeline>
						<el-timeline-item v-for="(activity, index) in bugLogs"
                              :key="index"
                              :timestamp="$tools.rDate(activity.create_time)"
                              placement="top"
                              color="#0bbd87">
							<el-card>
								<h4>{{ activity.handle }}</h4>
                <p v-if="activity.remark">变更记录：{{ activity.remark }}</p>
                <span style="color: #409eff;margin-right: 8px">{{ activity.update_user }}</span>
                <span>操作于 {{ $tools.rTime(activity.create_time) }}</span>
							</el-card>
						</el-timeline-item>
					</el-timeline>
				</div>
			</el-card>
  </el-drawer>
  <!--  导入接口窗口-->
  <el-dialog v-model="importDlg" width="30%" title="导入接口">
      <el-form :rules="rulesinterface" ref="interfaceRef" >
      </el-form>
      <template #footer>
      <span slot="footer" class="dialog-footer">
        <el-button @click="importDlg = false">取消</el-button>
        <el-button type="primary" @click="confirmSelection1">导入</el-button>
      </span>
      </template>
  </el-dialog>
</template>

<script>
import treeNode from '../Interface/treeNode.vue';
import {ElMessage, ElMessageBox} from "element-plus";
import newEditCase from '../../components/common/InterfaceNew/neweditCase.vue';
import {mapMutations, mapState} from "vuex";
export default {
components: {
    treeNode,
    newEditCase
  },
computed: {
    buttonText() {
      return this.showOnlySelf ? '取消只看自己创建' : '只看自己创建';
    },
    ...mapState(['pro','testEnvs','envId']),
    username() {
			return window.sessionStorage.getItem('username');
		},
    env: {
			get() {
				return this.envId;
			},
			set(val) {
				this.selectEnv(val);
			}
		}
    },
data() {
    return {
      addApiDlg:true,
      treeId: '',
      filterText:'',
      tableData: [],
      editCaseDlg: false,
      logDlg:false,
      importDlg:false,
      Interface_id: '',
      copyDlg: false,
      showOnlySelf: false,
      selectedOption:'',
      dialogVisible: false,
      selectedEnvironment: '',
      selectedEnvironmentName: '暂未选择',
      selectionConfig: {
      selectedRowKeys: [], // 已选中行的 key
      selectionChange: this.handleSelectionChange // 选择变化时的回调函数
    },
      bugLogs: [
        {
          create_time: "2024-02-18T10:30:00",
          handle: "修复了一个bug",
          remark: "这是修复bug的备注",
          update_user: "张三"
        },
        {
          create_time: "2024-02-17T14:20:00",
          handle: "重新测试了bug",
          remark: "接口名称登录变更为tms登录接口",
          update_user: "李四"
        },
        {
          create_time: "2024-02-16T09:45:00",
          handle: "提交了一个新的bug",
          update_user: "王五"
        }
        ],
      interfaceCount:0,
    };
  },
  methods: {
  ...mapMutations(['selectEnv']),
    closeModal() {
      this.$emit('close-modal');
    },
    // 点击取消
    clickClear(){
      this.closeModal()
    },

    // 把批量选择完成的数据取出id重新生成数组
    handleSelectionChange(selected) {
      this.selectionConfig.selectedRowKeys = selected.map(item => item.id);
    },
    // 根据接口类型展示不同的样式
    getRowClassName(row) {
      switch (row) {
        case 'GET':
          return '--el-card-border-color:#61affe;background-color:rgba(97,175,254,.1)'
        case 'POST':
          return '--el-card-border-color:#49cc90;background-color:rgba(73,204,144,.1)'
        case 'PUT':
          return '--el-card-border-color:#fca130;background-color:rgba(252,161,48,.1)'
        case 'DELETE':
          return '--el-card-border-color:#f93e3e;background-color:rgba(249,62,62,.1)'
        case 'PATCH':
          return '--el-card-border-color:#50e3c2;background-color:rgba(80,227,194,.1)'
        default:
          return '';
    }
  },

    // 根据对应节点展示接口信息
    async handleTreeClick(id,name,creator) {
      if(name) {
      const response = await this.$api.getnewInterfaces(id,name);
      if (response.status === 200) {
        this.treeId = id;
        this.tableData = response.data;
        this.interfaceCount = response.data.length;
      }} else if(creator){
        const response = await this.$api.getnewInterfaces(id,name,creator);
        if (response.status === 200) {
          this.treeId = id;
          this.tableData = response.data;
          this.interfaceCount = response.data.length;}
      } else {
        const response = await this.$api.getnewInterfaces(id);
        if (response.status === 200) {
          this.treeId = id;
          this.tableData = response.data;
          this.interfaceCount = response.data.length;}
      }
    },

    // 单个接口信息删除接口
    async delInterface(id){
      const response = await this.$api.delnewInterface(id);
			if (response.status === 204) {
        ElMessage({
          type: 'success',
          message: '删除成功',
          duration: 1000
        });
      this.handleTreeClick(this.treeId);
      this.filterText = '';
      this.$refs.multipleTable.clearSelection();
      }
    },
    // 确定添加
    handleApiClick(){
      if (this.selectionConfig.selectedRowKeys.length === 0) {
          ElMessage({
            type: 'warning',
            message: '请勾选数据后再操作！',
            duration: 2000
          });
          return;
        }
      const apis = [...this.selectionConfig.selectedRowKeys]
      this.$emit('childEvent', apis);
      this.filterText = '';
      this.selectionConfig.selectedRowKeys = [];
      this.$refs.multipleTable.clearSelection();
      this.clickClear()

    },

    // 点击查询
    handlenewInterfacesClick() {
      this.handleTreeClick(this.treeId,this.filterText)
    },


    // 点击删除
    clickDel(id) {
			ElMessageBox.confirm('确定要删除该接口吗?', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning'
			})
				.then(() => {
					this.delInterface(id);
				})
				.catch(() => {
					ElMessage({
						type: 'info',
						message: '取消删除',
						duration: 1000
					});
				});
		},

    handleClose() {
      this.addCaseDlg = false;
      this.editCaseDlg = false;
      this.copyDlg = false;
      this.handleTreeClick(this.treeId);
    },

    clickEditStep(id) {
      this.Interface_id = id
      this.editCaseDlg = true
      this.$nextTick(() => {
        this.$refs.childRef.getInterfaceInfo(this.Interface_id);
      })
    },

    // 复制用例
		clickCopy(id) {
      this.copyDlg = true;
      this.clickEditStep(id)
    },
    // 操作记录
		clickLog() {
      this.logDlg = true;

    },
    // 只看自己创建的接口
    userInterface() {
      this.showOnlySelf = !this.showOnlySelf;
       if (this.showOnlySelf) {
        // 只看自己创建的逻辑
        this.handleTreeClick(this.treeId,'',this.username);
      } else {
        // 取消只看自己创建的逻辑
        this.handleTreeClick(this.treeId);
      }
    },

    confirmSelection() {
      this.env = this.selectedEnvironment; // 在确认选择时更新 env 数据
      this.selectedEnvironmentName = this.testEnvs.find(env => env.id === this.selectedEnvironment).name;
      this.dialogVisible = false;
    }

  }
};
</script>

<style scoped>

.style {
    line-height: 12px;
    height: 28px;
}
.card-title {
  display: flex;
  width: 1200px;
}
.card-content {
  display: flex;
  justify-content: flex-end;
  margin-top: -11px; /* 调整此处的数值来改变距离 */
}
/*.el-card{*/
/*  --el-card-border-color:#49cc90*/
/*}*/

.card-url {
  margin-left: 10px;
  margin-right: 10px;
  font-size: 15px;
}
.card-name {
  font-size: 14px;
}
.el-tag {
  color: #ffffff;
  width:70px;
  height: 30px;
  text-align: center;
  font-size: 14px;
  line-height: 30px;
}
.interface-title {
    clear: both;
    font-weight: 400;
    margin-top: .48rem;
    margin-bottom: 4px;
    border-left: 3px solid #2395f1;
    padding-left: 8px;
    font-size: 14px;
}
</style>
