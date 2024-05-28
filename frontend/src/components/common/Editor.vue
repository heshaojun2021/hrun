<template>
  <el-scrollbar @wheel.stop>
    <VAceEditor :options="editOption" v-model:value="dataEdit" :lang="lang" :theme="theme" :style="{ height: height}" />
    <el-button style="margin-top:10px" plain type="success" size="small" @click="formatJson" v-if="lang === 'json'">格式化JSON</el-button>
  </el-scrollbar>
</template>

<script>
import { VAceEditor } from 'vue3-ace-editor';
import 'ace-builds/src-noconflict/snippets/json';
import 'ace-builds/src-noconflict/mode-json';
import 'ace-builds/src-noconflict/snippets/python';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/mode-html';
import 'ace-builds/src-noconflict/snippets/html';
import 'ace-builds/src-noconflict/theme-chrome';
import 'ace-builds/src-noconflict/theme-monokai';
import 'ace-builds/src-noconflict/ext-language_tools';
// import ace from 'ace-builds';
// ace.config.set('basePath', 'https://cdn.jsdelivr.net/npm/ace-builds@' + require('ace-builds').version + '/src-noconflict/');

export default {
	components: {
		VAceEditor
	},
	methods: {
  formatJson() {
    const jsObj = JSON.parse(this.dataEdit);
    const formattedJson = JSON.stringify(jsObj, null, 4);

    // 更新数据并等待DOM更新完成后再执行其他操作
    this.$nextTick(() => {
      this.dataEdit = formattedJson;
    });
  }
	},
	props: {
		lang: {
			default: 'json'
		},
		modelValue: {
			type: String
		},
		theme: {
			default: 'chrome'
		},
		height: {
			default: '400px'
		},
		readOnly: {
			default: false
		},
	},
	emits: ['update:modelValue'],
	computed: {
		editOption() {
			return {
				enableBasicAutocompletion: true, // 启用基本自动补全
				enableSnippets: true, // 启用代码段
				enableLiveAutocompletion: true, // 启用实时自动提示
				tabSize: 4, // 	tab键占用的空格的位置
				fontSize: 14, // 设置字号
				// useWorker: true, // 使用校验语法是否正确
				showPrintMargin: false, //去除编辑器里的竖线
				enableMultiselect: true, // 支持鼠标选中多处
				readOnly: this.readOnly, // 是否只读
				showFoldWidgets: true, // 显示折叠部件
				fadeFoldWidgets: true, // 淡入折叠部件
				wrap: true, //换行
			};
		},
		dataEdit: {
			get() {
				return this.modelValue;
			},
			set(value) {
				this.$emit('update:modelValue', value);
			}
		}
	}
};
</script>

<style>
.ace_scrollbar {
    display: none !important;
}

</style>
