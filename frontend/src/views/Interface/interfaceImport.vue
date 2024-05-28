<template>
  <el-dialog v-model="importDlg"  title="导入接口" width="60%" :before-close="clickClear" custom-class="class_dialog" top="50px">
    <div>
      <el-check-tag v-for="(option, index) in options" :key="index" :class="{ 'selected': selectedOption === option.value }" @click="selectOption(option.value)" class="option">
        <i ><icon :icon="option.icon" class="importIcon"/></i>{{ option.label }}
      </el-check-tag>
    </div>
    <div v-if="selectedOption==='Postman'">
      <div class="help-box">
      支持导入 <el-tag>Postman</el-tag> 集合、环境、全局数据。
      </div>
      <div style="display: flex; justify-content: center; align-items: center;">
        <el-upload
          v-model:file-list="fileList"
          drag
          action="http://127.0.0.1:8001/upload/"
          multiple
          @on-change="handleChange"
        >
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">将文件拖到此处，或 <em>点击上传</em></div>
        </el-upload>
      </div>
    </div>
    <div v-if="selectedOption==='YApi'">
      <div class="help-box">
      支持手动、自动导入 <el-tag>YApi</el-tag> 平台的接口数据。
      </div>
      <div>
      <el-check-tag v-for="(optionYApi, index) in optionYApi"
                    :key="index"
                    :class="{ 'selectedYApi': selectedOptionYApi === optionYApi.value }"
                    @click="selectOptionYApi(optionYApi.value)"
                    class="optionYApi">
        {{ optionYApi.label }}
      </el-check-tag>
      </div>
      <div v-if="selectedOptionYApi===0">
          <el-form :inline="true" :model="formInline" class="demo-form-inline" :rules="rulesYApi" ref="YApiRef">
            <el-form-item label="平台地址" prop='url'>
              <el-input v-model="formInline.url" placeholder="请输入YApi平台项目地址" clearable />
            </el-form-item>
            <el-form-item label="平台TOKEN" prop='token'>
              <el-input v-model="formInline.token" placeholder="请输入YApi平台项目token" clearable />
            </el-form-item>
            <el-form-item label="平台项目ID" prop='YApiId'>
              <el-input v-model="formInline.YApiId" placeholder="请输入YApi平台项目id" clearable />
            </el-form-item>
            <el-form-item label="节点/模块" prop='treenode'>
              <el-cascader
                  v-model="formInline.treenode"
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
          </el-form>
      </div>
      <div v-else >
        <div class="help-warning">
          因与定时任务功能入口重复，请移至定时任务功能入口进行自动同步
        </div>
      </div>
    </div>
    <template #footer>
        <span slot="footer" class="dialog-footer">
          <el-button @click="clickClear">取消</el-button>
          <el-button type="primary" :loading="isLoading" @click="importClick(selectedOption)">导入</el-button>
        </span>
    </template>
  </el-dialog>
</template>

<script>
import { Icon } from '@iconify/vue'
import {mapState} from "vuex";
import {ElMessage} from "element-plus";
export default {
  components: {
   Icon
  },
  props: ['importDlg'],
  data() {
    return {
      isLoading: false,
      importDlg:this.importDlg,
      selectedOption: 'Postman', // 默认选中第一个选项
      selectedOptionYApi: 0, // 默认选中第一个选项
      rulesYApi: {
        url: [
					{
						required: true,
						message: '请输入YApi平台项目地址',
						trigger: 'blur'
					}
				],
				token: [
					{
						required: true,
						message: '请输入YApi平台项目token',
						trigger: 'blur'
					}
				],
				YApiId: [
					{
						required: true,
						message: '请输入YApi平台项目id',
						trigger: 'blur'
					}
				],
        treenode: [
					{
						required: true,
						message: '请选择节点/模块',
						trigger: 'blur'
					}
				]
			},
      options: [
        { value: 'Postman', label: 'Postman', icon: 'devicon:postman' },
        { value: 'Apipost', label: 'Apipost', icon: 'logos:appcircle-icon'},
        { value: 'Curl', label: 'Curl', icon: 'logos:codio'},
        { value: 'Swagger', label: 'Swagger', icon: 'vscode-icons:file-type-swagger' },
        { value: 'Js fetch', label: 'Js fetch', icon: 'logos:nodejs-icon'},
        { value: 'YApi', label: 'YApi', icon: 'logos:yii' }
      ],
      optionYApi: [
        { value: 0, label: '手动同步'},
        { value: 1, label: '自动同步'}
      ],
      fileList: [
        {
          name: 'food.jpeg',
          url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100',
        },
        {
          name: 'food2.jpeg',
          url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100',
        },
      ],
    formInline:{
        token:'069a46f10333f6923285d9d312c0c912f2db0286b99c3a8ae3544fca38eb1f54',
        YApiId:17139,
        treenode:'',
        format:'list',
        project:'',
        url:'http://api.doc.jiyou-tech.com'
    },
    treeOptions:[]
    }
  },
  computed: {
    ...mapState(['pro']),
  },
  methods:{
    closeModal() {
      this.$emit('close-modal');
    },
    // 点击取消
    clickClear(){
      this.closeModal()
    },

    importClick(selectedOption) {
      if (selectedOption==='YApi'){
          this.getYApiImport()
      }else {}
    },

    selectOption(option) {
      this.selectedOption = option; // 更新选中选项
    },
    selectOptionYApi(option) {
      this.selectedOptionYApi = option; // 更新选中选项
    },
    handleChange(uploadFile, uploadFiles) {
      this.fileList = this.fileList.slice(-3);
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

    async getYApiImport(){
      this.$refs.YApiRef.validate(async vaild => {
        if (!vaild) return;
      this.isLoading = true;
      let params = { ...this.formInline};
			params.project = this.pro.id;
			// 获取最后一个节点的id
			if (params.treenode && params.treenode.length > 0) {
        const lastValue = params.treenode[params.treenode.length - 1];  // 获取最后一个值
        params.treenode = lastValue
      }
      const response = await this.$api.getYApiImport(params)
        if (response.status === 201) {
            ElMessage({
              type: 'success',
              message: '导入成功',
              duration: 1000
            });
            this.closeModal()
          }
			  this.isLoading = false;
      })
    },
    // 树结构列表接口
    async allTree() {
      const response = await this.$api.gettreeNode()
      if (response.status === 200) {
        this.treeOptions = response.data.result}
     },



  },
  created() {
    this.allTree()
  }

}
</script>

<style scoped>
.option {
  cursor: pointer;
  color: #000;
  margin:0px 0px 25px 15px;
  width: 150px;
  line-height: 30px;
  font-weight: 400;
}

.selected {
  background-color: #b2d8ff; /* 高亮展示的背景颜色 */
  color: white; /* 高亮展示时的字体颜色 */
}
.importIcon {
  margin-right: 8px;
  margin-left: -5px;
  font-size:25px;
  border-radius: 50%;
  display: inline-block; /* 将元素设置为行内块级元素 */
  vertical-align: middle; /* 垂直居中对齐 */

}

.help-box {
    background-color: #fafafb;
    padding: 20px;
    border-radius: 5px;
    margin:0 10px 20px 14px;
}
.help-warning {
    background-color: #fdf6ec;
    padding: 20px;
    border-radius: 5px;
    margin:0 10px 20px 14px;
}

.dialog-footer {
  margin-top: 30px;
  margin-right: 10px;
}

.optionYApi {
  margin:0px 0px 25px 15px;
  cursor: pointer;
  color: #409eff;
  font-weight: 400;
}

.selectedYApi {
  background-color: #409eff; /* 高亮展示的背景颜色 */
  color: white; /* 高亮展示时的字体颜色 */
}

</style>