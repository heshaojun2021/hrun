<template>
  <el-row :gutter="40">
    <el-col :span="15">
      <el-row v-for="(item, index) in params" :key="index" :gutter="5" style="margin-top: 5px;">
        <el-col :span="5">
          <el-input size="mini" v-model="item[0]" placeholder="参数名" clearable/>
        </el-col>
        <el-col :span="4">
          <el-select @change="seleType($event, index)" v-model="paramsType[index]" placeholder="参数类型" size="mini"
                     style="width: 100%;">
            <el-option label="Text" value="text"/>
            <el-option label="File" value="file"/>
          </el-select>
        </el-col>
        <el-col :span="11">
          <!-- 文字输入框 -->
          <el-input v-if="paramsType[index] == 'text'" v-model="item[1]" placeholder="参数值" size="mini" clearable/>
          <el-select v-else @change="seleFile($event, index)" v-model="item[1][0]" size="mini" placeholder="选择已有文件"
                     style="width: 100%;">
            <el-option v-for="item in files" :label="item.info[0]" :value="item.info[0]"/>
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-button icon="el-icon-delete" @click="params.splice(index, 1)" size="mini" type="danger" plain></el-button>
        </el-col>
      </el-row>
      <el-button style="margin-top: 10px;" icon="el-icon-plus" @click="params.push(['', ''])" size="mini" type="success"
                 plain></el-button>
    </el-col>
    <el-col :span="9">
      <el-card>
        <el-upload
            class="upload-demo"
            :action="$api.uploadApi.url"
            :headers="updateHead"
            :show-file-list="false"
            :on-success="uploadSuccess"
            :on-error="uploadError"
            name="file"
        >
          <el-button type="success" plain size="mini">上传文件</el-button>
        </el-upload>
        <el-table :data="files" style="width: 100%" size="mini" height="200px" empty-text="暂无数据">
          <el-table-column label="已有文件">
            <template #default="scope">
              <el-tag type="success">{{ scope.row.info[0] }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="文件类型">
            <template #default="scope">
              <el-tag type="info">{{ scope.row.info[2] }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template #default="scope">
              <el-button @click="deleteFile(scope)" type="danger" size="small" icon="el-icon-delete" plain></el-button>

            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>
export default {
  data() {
    return {
      // 编辑的参数
      params: [],
      // 文件列表
      files: [],
      // 参数类型列表
      paramsType: []
    };
  },
  props: {
    modelValue: {
      type: Array,
      default: [['', '']]
    }
  },
  computed: {
    updateHead() {
      return {
        Authorization: 'Bearer ' + window.sessionStorage.getItem('token')
      };
    }
  },
  emits: ['update:modelValue'],
  methods: {
    // 修改参数类型
    seleType(val, index) {
      if (val === 'file') {
        this.params[index][1] = ['', '', ''];
      } else {
        this.params[index][1] = '';
      }
    },
    // 修改参数值
    seleFile(val, index) {
      // 当前选中的文件
      const sFile = this.files.find(item => {
        return item.info[0] === val;
      });
      // 修改文件
      this.params[index][1] = [...sFile.info];
      console.log(this.params);
    },
    // 文件上传成功
    uploadSuccess(response) {
      this.$message({
        type: 'success',
        message: '文件上传成功!',
        duration: 2000
      });
      this.getAllfile();
    },
    // 文件上传失败
    uploadError(error) {
      this.$message({
        type: 'error',
        message: JSON.parse(error.message)[0],
        duration: 2000
      });
    },
    // 获取文件列表
    async getAllfile() {
      // 获取文件列表
      const response = await this.$api.getFiles();
      if (response.status === 200) {
        this.files = response.data;
      }
    },
    // 文件删除
    async deleteFile(scope) {
      // 删除文件
      console.log(scope)
      const response = await this.$api.deleteFile(scope.row.id);
      if (response.status === 204) {
        this.$message({
          type: 'success',
          message: '删除成功！',
          duration: 2000
        });
        this.files.splice(scope.$index, 1)
      }
    },
    // 获取参数的类型
    getParamsType() {
      // 获取参数类型
      this.paramsType = [];
      this.params.forEach(item => {
        if (typeof item[1] === 'string') {
          this.paramsType.push('text');
        } else {
          this.paramsType.push('file');
        }
      });
    }
  },
  created() {
    if (this.modelValue.length > 0) {
      this.params = this.modelValue;
    } else {
      this.params = [['', '']];
    }
    this.getAllfile();
    this.getParamsType();
  },
  watch: {
    'params.length': function (val) {
      this.getParamsType();
    },
    params: {
      deep: true,
      handler: function (value) {
        this.$emit('update:modelValue', value);
      }
    },
    modelValue: {
      deep: true,
      handler: function (value) {
        this.params = value;
      }
    }
  }
};
</script>

<style></style>
