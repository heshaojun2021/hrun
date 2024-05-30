import axios from 'axios'
import router from '../router/index.js'
import {
	ElMessage
} from 'element-plus';
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'


// 设置后台域名
// axios.defaults.baseURL = 'http://172.28.25.61:8002'
// axios.defaults.baseURL = 'http://127.0.0.1:8000'
axios.defaults.baseURL = 'http://139.9.38.166:5001'
axios.defaults.timeout = 80000    //请求超时
axios.defaults.validateStatus = function(status) {
	return true
}
// 自动携带cookies
axios.defaults.withCredentials = true;

axios.interceptors.request.use(config => {
  NProgress.start()
  // 最后必须return config
  return config
})
// 在 response 拦截器中，隐藏进度条 NProgress.done();
axios.interceptors.response.use(config => {
  NProgress.done()
  return config
})




// 通过requests拦截器，获取sessionStirage中的token，添加到请求头中
axios.interceptors.request.use(config => {
  const url = config.url;
  const regex = /^\/records\/\d+(?:\/report)?\/?/; // 匹配 /records/ 下的所有请求
  if (!regex.test(url) && url !== '/users/login/') {
    config.headers.Authorization = 'Bearer ' + window.sessionStorage.getItem('token');
  }
  return config;
});
// 添加响应拦截器
axios.interceptors.response.use(function(response) {

	//响应状态码正常不做处理
	if (response.status === 200) return response
	if (response.status === 201) return response
	if (response.status === 204) return response
	// 异常响应状态码的处理
	// 判断响应状态码是否为401,并且不是登录接口或注册接口
	if (response.status === 401 && (response.config.url !== '/users/login/') && !response.config.url.match(/^\/records\/\d+(?:\/report)?\/?/)) {
		window.localStorage.removeItem('token')
		console.log(response.config.url)
		// 路由跳转到登录页面
		router.push({
			name: 'login'
		})
		ElMessage({
			message: '您未登录,请先进行登录!',
			type: 'warning',
			duration: 1000
		});
	} else if (response.status === 400) {
		ElMessage({
			message: response.data,
			type: 'warning',
			duration: 1000
		});
	} else if (response.status === 500) {
		ElMessage({
			message: '服务异常，请联系开发人员处理！',
			type: 'error',
			duration: 1000
		});
	} else if (response.status === 404) {
	} else {
		// 其他的响应状态码提示
		ElMessage({
			message: response.data.detail,
			type: 'warning',
			duration: 1000
		});
	}
	return response;
});

export default {
	// 上传文件接口信息
	uploadApi: {
		url: axios.defaults.baseURL + '/upload/',

	},

	//--------------------用户登录----------------------------------
	// 登录接口
	login(params) {
		return axios.post('/users/login/', params)
	},

	// ==========================用户管理接口================
	// 获取所有用户
	getAlluser(url,project_id) {
		return axios.get(url,{
			params: {
				project: project_id
			}
		})
	},
	// 新增用户
	createUser(params) {
		return axios.post('/users/user/',params)
	},
	// 修改用户
	updateUser(id,params) {
		return axios.patch(`/users/user/${id}/`,params)
	},

	// 删除用户
	deleteUser(id) {
		return axios.delete(`/users/user/${id}/`)
	},


	// -------------------项目增删查改-------------------------------
	// 获取所有项目
	getProjects() {
		return axios.get('/projects/')
	},
	// 获取单个项目详情
	getProject(id) {
		return axios.get(`/projects/${id}/`)
	},
	// 删除项目
	delProject(id) {
		return axios.delete(`/projects/${id}/`)
	},
	// 添加项目
	createProjects(params) {
		return axios.post('/projects/', params)
	},
	// 编辑项目项目
	updateProjects(id, params) {
		return axios.patch(`/projects/${id}/`, params)
	},
	// ================接口增删查改===================
	// 获取所有接口
	getInterfaces(project_id, type,page,size,name,method,url) {
		return axios.get(`/interfaces/`, {
			params: {
				project: project_id,
				type: type,
				page: page,
				size: size,
				name: name,
				method: method,
				url:url
			}
		})
	},
	// 删除接口
	delInterface(id) {
		return axios.delete(`/interfaces/${id}/`)
	},
	// 添加接口
	createInterface(params) {
		return axios.post('/interfaces/', params)
	},
	// 修改接口
	updateInterface(id, params) {
		return axios.patch(`/interfaces/${id}/`, params)
	},

	// ================new结构树增删查改===================
	// 获取所有treeNode
	gettreeNode(params) {
		return axios.get(`/treeNode/`,{
			params: params
		})
	},
	// 删除treeNode
	deltreeNode(id) {
		return axios.delete(`/treeNode/${id}/`)
	},
	// 添加treeNode
	createtreeNode(params) {
		return axios.post('/treeNode/', params)
	},
	// 修改treeNode
	updatetreeNode(id, params) {
		return axios.patch(`/treeNode/${id}/`, params)
	},



	// ================new接口增删查改===================

	// 获取所有接口
	getnewInterfaces(treenode_id,name,status,creator) {
		return axios.get(`/newinterfaces/`, {
			params: {
				treenode_id: treenode_id,
				name: name,
				creator:creator,
				status:status
			}
		})
	},

	// 获取单个测试步骤
	getnewInterface(id) {
		return axios.get(`/newinterfaces/${id}/`)
	},

	// 删除单个接口
	delnewInterface(id) {
		return axios.delete(`/newinterfaces/${id}/`)
	},

	// 批量删除接口
	delAllnewInterface(params) {
		return axios.post('/newinterfaces/delete_batch/', params)
	},
	// 添加接口
	createnewInterface(params) {
		return axios.post('/newinterfaces/', params)
	},
	// 修改接口
	updatenewInterface(id, params) {
		return axios.patch(`/newinterfaces/${id}/`, params)
	},


	// 运行单用例的接口
	runNewCase(params) {
		return axios.post('/newinterfaces/run/', params)
	},




	// ================hook推送增删查改===================
	// 获取所有hook
	getHook(project_id,page,size) {
		return axios.get(`/wxPush/`, {
			params: {
				project_id: project_id,
				page: page,
				size: size,

			}
		})
	},
	// 删除hook
	delHook(id) {
		return axios.delete(`/wxPush/${id}/`)
	},
	// 添加hook
	createHook(params) {
		return axios.post('/wxPush/', params)
	},
	// 修改hook
	updateHook(id, params) {
		return axios.patch(`/wxPush/${id}/`, params)
	},

	// ============测试场景相关的接口====================
	// 获取项目所有测试场景
	getTestScent(params) {
		return axios.get(`/test_scenes/`, {
			params: params
		})
	},
	// 获取单个测试场景下的详细数据
	getScentInfo(scren_id) {
		return axios.get(`/test_scenes/${scren_id}/`)
	},
	// 删除测试场景
	delTestScent(id) {
		return axios.delete(`/test_scenes/${id}/`)
	},
	// 添加测试场景
	createTestScent(params) {
		return axios.post('/test_scenes/', params)
	},
	// 修改测试场景
	updateTestScent(id, params) {
		return axios.patch(`/test_scenes/${id}/`, params)
	},
	// ==============测试场景中的数据==================
	// 修改测试场景中的执行步骤顺序
	updateScentDataOrder(params) {
		return axios.put('/test_scene_steps/order/', params)
	},
	// 获取测试场景数据
	getScentDatas(scentId) {
		return axios.get(`/test_scene_steps/`, {
			params: {
				scene: scentId
			}
		})
	},

	// 添加步骤到测试场景中
	addScentData(params) {
		return axios.post('/test_scene_steps/', params)
	},
	// 删除测试场景中的步骤
	delScentData(id) {
		return axios.delete(`/test_scene_steps/${id}/`)
	},

	// ==============测试步骤相关的接口================
	getTeststep(params) {
		return axios.get(`/test_steps/`, {
			params: params
		})
	},
	// 获取单个测试步骤
	getTestStepInfo(id) {
		return axios.get(`/test_steps/${id}/`)
	},
	// 删除测试步骤
	delTeststep(id) {
		return axios.delete(`/test_steps/${id}/`)
	},
	// 创建测试步骤
	createTeststep(params) {
		return axios.post('/test_steps/', params)
	},
	// 修改测试步骤
	updateTeststep(id, params) {
		return axios.patch(`/test_steps/${id}/`, params)
	},


	// ============测试计划相关的接口====================
	// 获取项目所有测试计划
	getTestPlan(project_id,name) {
		return axios.get(`/test_plans/`, {
			params: {
				project: project_id,
				name: name
			}
		})
	},
	// 删除测试计划
	delTestPlan(id) {
		return axios.delete(`/test_plans/${id}/`)
	},
	// 添加测试计划
	createTestPlan(params) {
		return axios.post('/test_plans/', params)
	},
	// 添加测试计划下的场景
	createTestPlan_scene(id,params) {
		return axios.post(`/test_plans/${id}/add_new_scenes/`, params)
	},
	// 删除测试计划下的场景
	delTestPlan_scene(id,params) {
		return axios.post(`/test_plans/${id}/remove_new_scene/`, params)
	},
	// 修改测试计划
	updateTestPlan(id, params) {
		return axios.patch(`/test_plans/${id}/`, params)
	},
	// ============测试环境相关的接口====================
	// 获取项目所有测试环境
	getTestEnvs(project_id) {
		return axios.get(`/test_envs/`, {
			params: {
				project: project_id
			}
		})
	},
	getEnvInfo(id,project_id) {
		return axios.get(`/test_envs/${id}/`,{
			params: {
				project: project_id
			}
		})
	},
	// 删除测试环境
	delTestEnvs(id) {
		return axios.delete(`/test_envs/${id}/`)
	},
	// 添加测试环境
	createTestEnvs(params) {
		return axios.post('/test_envs/', params)
	},
	// 修改测试环境
	updateTestEnvs(id, params) {
		return axios.patch(`/test_envs/${id}/`, params)
	},
	// ==========================定时任务接口================
	// 获取所有定时任务
	getCrons(project_id) {
		return axios.get(`/crontab_tasks/`, {
			params: {
				project: project_id
			}
		})
	},
	// 删除定时任务
	delCron(id) {
		return axios.delete(`/crontab_tasks/${id}/`)
	},
	// 添加定时任务
	createCron(params) {
		return axios.post('/crontab_tasks/', params)
	},
	// 修改定时任务
	updateCron(id, params) {
		return axios.patch(`/crontab_tasks/${id}/`, params)
	},


	// ===================测试记录==========================
	// 获取所有的测试记录
	getTestRecord(params) {
		return axios.get(`/records/`, {
			params: params,
		})
	},
	getRecordInfo(id) {
		return axios.get(`/records/${id}/`)
	},
	// 获取测试报告信息
	getTestReport(id) {
		return axios.get(`/records/${id}/report/`)
	},
	//=====================bug管理======================
	// 获取所有bug
	getBugs(params) {
		return axios.get('/bugs/', {
			params: params
		})
	},
	// 添加bug记录
	createBugs(params) {
		return axios.post('/bugs/', params)
	},
	// 修改bug记录
	updateBug(id, params) {
		return axios.patch(`/bugs/${id}/`, params)
	},
	// 删除bug
	deleteBug(id) {
		return axios.delete(`/bugs/${id}/`)
	},
	//=====================获取bug处理记录列表======================
	getBugLogs(params) {
		return axios.get('/blogs/', {
			params: params
		})
	},


	// =================用例运行===========================
	// 运行测试的接口
	runTest(params) {
		return axios.post('/runTest/', params)
	},
	// 运行单用例的接口
	runCase(params) {
		return axios.post('/test_steps/run/', params)
	},
	// 运行单个场景的接口
	runScene(id, params) {
		return axios.post(`/test_scenes/${id}/run/`, params)
	},
	// 运行单个场景的接口
	runCases(id, params) {
		return axios.post(`/TestCase/${id}/run/`, params)
	},
	// 运行测试计划的接口
	runPlan(id, params) {
		return axios.post(`/test_plans/${id}/run/`, params)
	},

	// ================文件上传操作========================
	// 上传文件
	uploadFile(params) {
		// 功能待完善
		return axios.post('/upload/', params)
	},
	// 获取文件列表
	getFiles() {
		return axios.get('/upload/')
	},
	// 删除文件
	deleteFile(id) {
		return axios.delete(`/upload/${id}/`)
	},

	// ================测试用例增删查改===================
	// 获取用例信息
	getTestCase(project_id,page,name) {
		return axios.get(`/TestCase/`, {
			params: {
				project_id: project_id,
				page: page,
				name: name,

			}
		})
	},
		// 获取单个用例信息
	getTestCase_(params) {
		return axios.get(`/TestCase/`, {
			params: params
		})
	},
	// 删除用例
	delTestCase(id) {
		return axios.delete(`/TestCase/${id}/`)
	},
	// 添加用例
	createTestCase(params) {
		return axios.post('/TestCase/', params)
	},
	// 修改用例
	updateTestCase(id, params) {
		return axios.patch(`/TestCase/${id}/`, params)
	},
	// 进入用例详情
	detailTestCase(id) {
		return axios.patch(`/TestCase/${id}/`)
	},

	// ================测试用例步骤的增删查改===================
	// 获取用例步骤
	getTestCaseStep(cases) {
		return axios.get(`/TestCase_Setp/`, {
			params: {
				case: cases,
			}
		})
	},
	// 批量添加用例步骤
	createsTestCaseStep(params) {
		return axios.post('/TestCase_Setp/batch_create/', params)
	},
	// 修改单个用例步骤
	updateTestCaseStep(id, params) {
		return axios.patch(`/TestCase_Setp/${id}/`, params)
	},
	// 单个添加用例步骤
	createTestCaseStep(params) {
		return axios.post('/TestCase_Setp/', params)
	},
	// 删除用例步骤
	delTestCaseStep(id) {
		return axios.delete(`/TestCase_Setp/${id}/delete_node`)
	},

	// 修改用例步骤的执行步骤顺序
	updateCaseStepOrder(params) {
		return axios.put('/TestCase_Setp/order/', params)
	},

	// ================测试用例控制器步骤的增删查改===================
	// 新增控制器步骤
	createStepControll(params) {
		return axios.post('/StepControll/', params)
	},
	// 删除控制器步骤
	delStepControll(id) {
		return axios.delete(`/StepControll/${id}/`)
	},

	// 修改控制器步骤
	updateStepControll(id, params) {
		return axios.patch(`/StepControll/${id}/`, params)
	},

	// 批量修改控制器步骤
	updatesStepControll(params) {
		return axios.put('/StepControll/batch_updateStep/', params)
	},

	// ================接口导入操作===================
	// YApi接口导入
	getYApiImport(params) {
		return axios.post('/yapi/', params)
	},


	// ================项目看板===================

	getProjectBoard(params) {
		return axios.post('/ProjectBoard/', params)
	},

}