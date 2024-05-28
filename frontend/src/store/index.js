import {
	createStore
} from 'vuex'
import api from '../api/index.js'
export default createStore({
	state: {
		tags: [],
		envId:null,// 选中的环境ID
		interfaces: [], 
		testScents: [],
		testPlans: [],
		testEnvs: [],
		cronTabs: [],
		Users: [],

	},
	getters: {
		// 内部接口
		interfaces1(state) {
			return state.interfaces.result.filter(item => {
				return item.type === '1';
			});
		},
		// 外部接口
		interfaces2(state) {
			return  state.interfaces.result.filter(item => {
				return item.type === '2';
			});
		}
	},
	mutations: {
		// 添加标签：
		addTags(state, tag) {
			const res = state.tags.find((item) => {
				return item.path === tag.path
			})
			if (!res) {
				state.tags.push(tag)
			}
		},
		// 删除标签标签：
		delTags(state, path) {
			// 删除标签页
			state.tags = state.tags.filter((item) => {
				return item.path !== path
			})
		},
		// 选中项目pro
		selectPro(state, value) {
			state.pro = value
		},
		// 选中的用例
		CaseInfo(state, value) {
			state.case = value
		},
		// 清除选中的用例
		clearCaseInfo(state) {
			  state.case = null;
			},

		// 选中的环境
		selectEnv(state, value) {
			state.envId = value
		},
		// 清空 envId 的值
		clearEnvId(state) {
			  state.envId = null;
			},
		updateInterfaces(state,value){
			state.interfaces = value
		},
		updateTestScents(state,value){
			state.testScents = value
		},
		updateTestPlans(state,value){
			state.testPlans = value
		},
		updateTestEnvs(state,value){
			state.testEnvs = value
		},
		updatecronTabs(state,value){
			state.cronTabs = value
		},
		updateUser(state,value){
			state.Users = value
		},
	},
	actions: {
		// 获取项目下所有接口
		// async  getAllInter(context){
		// 	const response = await api.getInterfaces(context.state.pro.id)
		// 	if(response.status===200){
		// 		context.commit('updateInterfaces',response.data)
		// 	}
		// },
		// 获取所有测试场景
		// async getAllScent(context) {
		// 	const response = await api.getTestScent({project:context.state.pro.id});
		// 	if (response.status === 200) {
		// 		context.commit('updateTestScents',response.data)
		//
		// 	}
		// },

		// 获取所有测试环境
		async getAllEnvs(context) {
			const response = await api.getTestEnvs(context.state.pro.id);
			if (response.status === 200) {
				context.commit('updateTestEnvs',response.data)
			
			}
		},
		// 获取所有测试计划
		async getAllPlan(context) {
			const response = await api.getTestPlan(context.state.pro.id);
			if (response.status === 200) {
				context.commit('updateTestPlans',response.data)
			
			}
		},
		// 获取所有用户
		async getAllUser(context) {
			const response = await api.getAlluser('/users/user/',context.state.pro.id);
			if (response.status === 200) {
				context.commit('updateUser',response.data.result)

			}
		},
	},
	modules: {}
})
