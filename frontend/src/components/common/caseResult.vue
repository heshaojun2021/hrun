<template>
	  <el-tabs model-value="rb" style="min-height: 300px;" type="border-card" value="rb" size="mini">
		<el-tab-pane v-if="result.type == 'api'" label="响应体" name="rb">
			  <div v-if="result.response_header">
				<div v-if="result.response_header['Content-Type'].search('application/json') != -1">
					<Editor :readOnly="true" v-model="result.response_body" lang="json" theme="chrome"></Editor>
				</div>
				<div v-else>
          <Editor :readOnly="true" v-model="result.response_body" lang="html" theme="chrome" height="500px"></Editor>
        </div>
			</div>
		</el-tab-pane>
		<el-tab-pane v-if="result.type == 'api'" label="响应头" name="rh">
      <el-scrollbar height="400px" @wheel.stop>
			  <div class="tab-box-sli" v-if="result.response_header">
				<div v-for="(value, key) in result.response_header">
					<el-tag style="margin-top: 3px;" type="info">
						<b style="color: #747474;">{{ key + ' : ' }}</b>
						<span>{{ value }}</span>
					</el-tag>
				</div>
			</div>
      </el-scrollbar>
		</el-tab-pane>
		<el-tab-pane v-if="result.type == 'api'" label="请求信息" name="rq">
      <el-scrollbar height="400px" @wheel.stop>
			  <div v-if="result.requests_body">
				<el-collapse v-model="activeNames" class="tab-box-sli">
					<el-collapse-item name="1">
						<template #title>
							<b>General</b>
						</template>
						<div>Request Method : {{ result.method }}</div>
						<div>Request URL : {{ result.url }}</div>
					</el-collapse-item>
					<el-collapse-item name="2">
						<template #title>
							<b>Request Headers</b>
						</template>
						<div v-for="(value, key) in result.requests_header">
							<span>{{ key + ' : ' + value }} :</span>
						</div>
					</el-collapse-item>
					<el-collapse-item name="3">
						<template #title>
							<b>Request Payload</b>
						</template>
						<span>{{ result.requests_body }}</span>
					</el-collapse-item>
				</el-collapse>
			</div>
      </el-scrollbar>
		</el-tab-pane>
		<el-tab-pane label="日志">
			<el-scrollbar height="400px" @wheel.stop>
				<div class="tab-box-sli">
					<div v-for="(item, index) in result.log_data">
						<el-tag style="margin-top: 3px;" v-if="item[0] === 'DEBUG'" >{{ item[1] }}</el-tag>
						<el-tag style="margin-top: 3px;" v-else-if="item[0] === 'WARNING'" type="warning">{{ item[1] }}</el-tag>
						<el-tag style="margin-top: 3px;" v-else-if="item[0] === 'ERROR'" type="danger">{{ item[1] }}</el-tag>
						<el-tag style="margin-top: 3px;" v-else-if="item[0] === 'INFO'" type="success">{{ item[1] }}</el-tag>
						<pre v-else-if="item[0] === 'EXCEPT'" style="color: #d60000;">{{ item[1] }}</pre>
					</div>
				</div>
			</el-scrollbar>
		</el-tab-pane>
		<el-tab-pane disabled>
			<template #label>
				<span v-if="result.state === '成功'" style="color: #00AA7F;">{{ 'Assert : ' + result.state }}</span>
				<span v-else-if="result.state === '失败'" style="color: #d18d17;">{{ 'Assert : ' + result.state }}</span>
				<span v-else style="color: #ff0000;">{{ result.state }}</span>
			</template>
		</el-tab-pane>
		<el-tab-pane v-if="result.type == 'api'" disabled>
			<template #label>
				<span v-if="result.status_cede <= 300" style="color: #00AA7F;">{{ 'Status : ' + result.status_cede }}</span>
				<span v-else style="color: #ff5500;">{{ 'Status : ' + result.status_cede }}</span>
			</template>
		</el-tab-pane>
		<el-tab-pane disabled>
			<template #label>
				{{ 'Time : ' + result.run_time }}
			</template>
		</el-tab-pane>
	</el-tabs>
	<div style="margin-top: 10px;width: 100%;text-align: center;" v-if="result.state === '失败' && showbtn">
		<el-button  @click="getInterfaces" type="success" plain size="mini">提交bug</el-button>
	</div>
	<!-- 添加bug的弹框 -->
	<el-dialog title="提交bug" v-model="addBugDlg" width="40%" :before-close="closeDialogResult">
		<el-form :model="bugForm">
			<el-form-item label="所属接口">
				<el-select size="small" v-model="bugForm.interface" placeholder="bug对应的接口" style="width: 100%;">
					<el-option :label="iter.name + ' ' + iter.url" :value="iter.id" v-for="iter in interfaces" :key="iter.id"></el-option>
				</el-select>
			</el-form-item>
			<el-form-item label="bug描述"><el-input :autosize="{ minRows: 3, maxRows: 4 }" v-model="bugForm.desc" type="textarea" autocomplete="off"></el-input></el-form-item>
		</el-form>
		<template #footer>
			<div class="dialog-footer">
				<el-button @click="closeDialogResult">取 消</el-button>
				<el-button type="success" @click="saveBug">确 定</el-button>
			</div>
		</template>
	</el-dialog>
</template>

<script>
import Editor from './Editor.vue';
import { mapState } from 'vuex';
export default {
	props: {
		result: {
			default: {}
		},
		showbtn: {
			default: true
		}
	},
	computed: {
		...mapState(['pro'])
	},
	components: {
		Editor
	},
	data() {
		return {
			activeNames: ['1', '2', '3'],
			// 提交bug的显示窗口
			addBugDlg: false,
			// 添加bug的表单
			bugForm: {
				interface: null,
				desc: '',
				info: '',
				status: '待处理'
			},
      interfaces:[]
		};
	},
	methods: {
		async saveBug() {
			this.bugForm.project = this.pro.id;
			this.bugForm.info = this.result;
			const response = await this.$api.createBugs(this.bugForm);
			if (response.status === 201) {
				this.$message({
					type: 'success',
					message: 'bug提交成功',
					duration: 1000
				});
				this.addBugDlg = false;
				this.bugForm = {
					interface: null,
					desc: '',
					info: '',
					status: '待处理'
				};
			}
		},
    // 取消按钮时重置输入信息
    closeDialogResult() {
      this.addBugDlg = false;
      this.bugForm = {
					interface: null,
					desc: '',
					info: '',
					status: '待处理'
				};
      },

    // 获取接口列表
    async getInterfaces() {
      const response = await this.$api.getnewInterfaces();
      if (response.status === 200) {
        this.interfaces = response.data
        this.addBugDlg = true
      }
    }
	}
};
</script>

<style></style>
