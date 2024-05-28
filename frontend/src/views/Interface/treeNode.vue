<template>
  <div class="tree-component">
        <el-input v-model="filterText" placeholder="请输入节点名称进行搜索" clearable >
          <template #append>
            <el-button type="primary" @click="handletreeClick">查询</el-button>
          </template>
        </el-input>
        <el-button
          type="primary"
          style="margin-bottom: 5px;margin-top: 10px"
          @click="clickAdd"
        >添加父节点</el-button>
        <el-scrollbar height="calc(100vh - 150px)">
        <el-tree
          class="filter-tree"
          :data="data"
          :props="defaultProps"
          :expand-on-click-node="false"
          @node-click="handleNodeClick"
          :default-expand-all="false"
        >
        <template v-slot="{ node, data }">
          <el-scrollbar>
          <span :class="{ 'bold-node': node.data.parent_id === null }">
            {{ node.label }}
          </span>
          </el-scrollbar>
          <div class="node-content">
            <span>
              <a @click="clickAddPart(node.data.id)"> <el-icon style="color: #0d84ff"><CirclePlus /></el-icon> </a>
              <a @click="clickEdit(node.data)"> <el-icon style="color: #0d84ff"><Edit /></el-icon> </a>
              <a @click="clickDel(node.data.id)"> <el-icon style="color: #0d84ff;margin-right: 20px"><Delete /></el-icon> </a>
            </span>
          </div>
        </template>
        </el-tree>
        </el-scrollbar>
      </div>

  <!--  新增树结构窗口-->
  <el-dialog v-model="addDlg.Dlg" :title="addDlg.sort === '0' ? '添加主节点' : '添加子节点'" width="20%" :before-close="clickClear">
    <el-form :model="addForm" :rules="rulestree" ref="treeRef">
    <el-form-item label="节点名称" prop="name">
      <el-input  v-model="addForm.name" autocomplete="off" placeholder="请输入节点名称" clearable/>
    </el-form-item>
    </el-form>
    <template #footer>
			<span class="dialog-footer">
				<el-button @click="clickClear" >取消</el-button>
				<el-button v-if="addDlg.sort === '0'" type="success" @click="addtree" >确定</el-button>
        <el-button v-else type="success" @click="partaddtree" >确定</el-button>
			</span>
		</template>
  </el-dialog>
  <!--  修改树结构窗口-->
  <el-dialog v-model="editDlg" title="修改节点" width="20%" :before-close="clickClear">
    <el-form :model="upFrom" :rules="rulestree" ref="treeRef">
    <el-form-item label="节点名称" prop="name">
      <el-input v-model="upFrom.name" autocomplete="off" placeholder="请输入节点名称" clearable/>
    </el-form-item>
    </el-form>
    <template #footer>
			<span class="dialog-footer">
				<el-button @click="clickClear" >取消</el-button>
        <el-button  type="success" @click="updatetree" >确定</el-button>
			</span>
		</template>
  </el-dialog>

</template>

<script>
import {ElMessage, ElMessageBox} from "element-plus";
import {mapState} from "vuex";

export default {
  props: {
    handleTreeClick: Function, // 父组件传递的方法
  },
  data() {
    return {
      filterText: '',
      data: [],
      addDlg: {
        Dlg:false,
        sort:''
      },
      addForm:{
        name: '',
        parent_id: '',
        project:''
      },
      editDlg:false,
      upFrom:{
        name: '',
        parent_id: '',
        create_time:'',
        enable_flag:'',
        id:'',
        project:'',
        type:null
      },
      rulestree: {
				// 验证名称是否合法
				name: [
					{
						required: true,
						message: '请输入节点名称',
						trigger: 'blur'
					}
				],
			},
    }
  },
  computed: {
    ...mapState(['pro']),
    defaultProps() {
      return {
        children: 'children',
        label: 'name',
      }
    },
  },
  methods: {
    // 树结构列表接口
    async allTree(name) {
      if(name) {
      const response = await this.$api.gettreeNode({
        name: name,
        project_id: this.pro.id
		})
      if (response.status === 200) {
        this.data = response.data.result
      }}
      else {
        const response = await this.$api.gettreeNode({
          project_id: this.pro.id
		})
        if (response.status === 200) {
          this.data = response.data.result;
          // 设置默认激活的测试计划,并获取数据
				  if (this.data.length > 0 ) {
               this.handleTreeClick(this.data[0].id);
          }
        }
      }
    },

    handleNodeClick(data) {
      const id = data.id
      this.$emit('treeClick', id)
    },

    // 接口列表接口
    handleInterfaceClick() {
      console.log('查询接口')
    },

    // 主节点新增接口
    async addtree() {
       this.$refs.treeRef.validate(async vaild => {
        // 判断是否验证通过，不通过则直接retrue
        if (!vaild) return;
          const response = await this.$api.createtreeNode(this.addForm);
          if (response.status === 201) {
            ElMessage({
              type: 'success',
              message: '添加成功',
              duration: 1000
            });
            this.addDlg.Dlg = false;
            this.filterText = '';
            this.addDlg.sort = '';
            this.addForm = {
              name: '',
              parent_id: null,
              project: ''
            };
            this.allTree()
              }

       })

    },

    // 子节点新增接口
    async partaddtree() {
       this.$refs.treeRef.validate(async vaild => {
        // 判断是否验证通过，不通过则直接retrue
        if (!vaild) return;
        console.log(this.addForm)
          const response = await this.$api.createtreeNode(this.addForm);
          if (response.status === 201) {
            ElMessage({
              type: 'success',
              message: '添加成功',
              duration: 1000
            });
            this.addDlg.Dlg = false;
            this.addDlg.sort = '';
            this.filterText = '';
            this.addForm = {
              name: '',
              parent_id: null,
              project: ''
            };
            this.allTree()
              }

       })

    },

    // 修改接口
    async updatetree(){
      this.$refs.treeRef.validate(async vaild => {
        // 判断是否验证通过，不通过则直接retrue
        if (!vaild) return;
          const response = await this.$api.updatetreeNode(this.upFrom.id, this.upFrom);
          if (response.status === 200) {
            ElMessage({
              type: 'success',
              message: '修改成功',
              duration: 1000
            });
            this.editDlg = false;
            this.filterText = '';
            this.upFrom = {
                              name: '',
                              parent_id: '',
                              create_time:'',
                              enable_flag:'',
                              id:'',
                              type:null,
                              project: ''
                            }
              }
          this.allTree()

       })

    },

    // 删除接口
    async deltree(id){
      const response = await this.$api.deltreeNode(id);
			if (response.status === 204) {
        ElMessage({
          type: 'success',
          message: '删除成功',
          duration: 1000
        });
      this.allTree()
      this.filterText = '';
      }

    },

    // 点击查询
    handletreeClick() {
      this.allTree(this.filterText)
    },

    // 主节点点击添加
		clickAdd() {
			this.addDlg.Dlg = true;
			this.addDlg.sort = '0';
			this.addForm = {
				name: '',
        project: this.pro.id
			};
		},

    // 子节点点击添加
		clickAddPart(parent_id) {
			this.addDlg.Dlg = true;
			this.addDlg.sort = '1';
			console.log(parent_id)
			this.addForm = {
				name: '',
        parent_id: parent_id,
        project: this.pro.id
			};
		},


		// 点击修改
		clickEdit(info) {
			this.upFrom = { ...info };
			this.editDlg = true;
			console.log(this.upFrom)
		},

    // 点击取消
    clickClear(){
		  this.editDlg = false;
		  this.upFrom = '';
		  this.addDlg.Dlg = false;
		  this.addDlg.sort = '';
		  this.$refs.treeRef.clearValidate(); // 清除验证信息
    },

    // 点击删除
		clickDel(id) {
			ElMessageBox.confirm('确定要删除吗?', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
				type: 'warning'
			})
				.then(() => {
					this.deltree(id);
				})
				.catch(() => {
					ElMessage({
						type: 'info',
						message: '取消删除',
						duration: 1000
					});
				});
		},
  },

  created() {
    this.allTree()
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
</style>
