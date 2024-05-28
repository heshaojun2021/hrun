<template>
	<!-- 用户信息 -->
	<div class="user_box">
		<el-dropdown trigger="click" :hide-on-click="false" @command="handleCommand" style="color: #fff;flex: 1;text-align: center; cursor: pointer; margin-right: 20px"  >
			<span class="el-dropdown-link">
        <i ><icon :icon="avatar" class="u_head"/></i>
			<span class="username">{{ username }}
				<el-icon class="el-icon--right"><CaretBottom /></el-icon>
        </span>
			</span>
			<template #dropdown >
				<el-dropdown-menu >
					<el-dropdown-item command="select">选择项目</el-dropdown-item>
					<el-dropdown-item command="logout">注销登录</el-dropdown-item>
				</el-dropdown-menu>
			</template>
		</el-dropdown>
	</div>
	<!-- 左侧菜单 -->
	<div class="left_menu">
		<el-scrollbar height="calc(100vh - 54px);" >
			<el-menu :default-active="$route.path" router  background-color='#001529' text-color='#fff'
		active-text-color='#fff' class="el-menu-vertical-demo" :default-openeds="['test']" >
        <el-menu-item :index="'/project'">
					<span :class="'el-icon-s-home'"></span>
					<span>项目看板</span>
				</el-menu-item>
				 <el-submenu index="test" v-if="isTestMenuActive=true" >
          <template #title>
            <span class="el-icon-link"></span>
            <span>接口测试</span>
          </template>
        <el-menu-item :index="item.path" v-for="item in menus">
					<span :class="[item.icon, { 'colored-icon': item.icon === 'el-icon-info' }]"></span>
					<span>{{ item.name }}</span>
				</el-menu-item>
       </el-submenu>
         <el-submenu index="test2" v-if="isTestsubMenuActive=true" >
          <template #title>
            <span class="el-icon-discover"></span>
            <span>性能测试</span>
          </template>
         <el-menu-item :index="item.path" v-for="item in menus1">
					<span :class="item.icon"></span>
					<span>{{ item.name }}</span>
				</el-menu-item>
       </el-submenu>
       <el-submenu index="test3" v-if="isTestsubMenuActive=true" >
          <template #title>
            <span class="el-icon-setting"></span>
            <span>其他工具</span>
          </template>
         <el-menu-item :index="item.path" v-for="item in menus2">
					<span :class="item.icon"></span>
					<span>{{ item.name }}</span>
				</el-menu-item>
       </el-submenu>
        <el-menu-item :index="item.path" v-for="item in submenu">
					<span :class="item.icon"></span>
					<span>{{ item.name }}</span>
				</el-menu-item>
			</el-menu>
		</el-scrollbar>
	</div>
</template>

<script>
import { Icon } from '@iconify/vue'
import {mapMutations, mapState} from 'vuex';
const menuList1 = [
  {
		name: '接口管理',
		path: '/new-interface',
		icon: 'el-icon-paperclip'
	},
	{
		name: '接口用例',
		path: '/TestCase',
		icon: 'el-icon-s-help'
	},
  {
		name: '测试计划',
		path: '/new-testplan',
		icon: 'el-icon-collection-tag'
	},
	{
		name: '测试环境',
		path: '/testenv',
		icon: 'el-icon-coin'
	},
	{
		name: '定时任务',
		path: '/crontab',
		icon: 'el-icon-time'
	},
	{
		name: 'bug管理',
		path: '/bugs',
		icon: 'el-icon-lightning'
	},
	{
		name: '测试报表',
		path: '/records',
		icon: 'el-icon-s-data'
	}
];
const submenuList = [
    {
		name: '报告推送',
		path: '/reportPush',
		icon: 'el-icon-s-promotion'
	},
  {
		name: '用户管理',
		path: '/users',
		icon: 'el-icon-user'
	},

];

const menuList2=[
  {
		name: '性能任务',
		path: '/performanceTask',
		icon: 'el-icon-cpu'
	},
  {
		name: '性能监控',
		path: '/performanceMonitor',
		icon: 'el-icon-stopwatch'
	},

]

const menuList3=[
	// {
	// 	name: '接口管理',
	// 	path: '/interface',
	// 	icon: 'el-icon-paperclip'
	// },
	// {
	// 	name: '接口用例',
	// 	path: '/testStep',
	// 	icon: 'el-icon-connection'
	// },
	// {
	// 	name: '测试场景',
	// 	path: '/testscent',
	// 	icon: 'el-icon-s-help'
	// },
  // {
	// 	name: '测试计划',
	// 	path: '/testplan',
	// 	icon: 'el-icon-collection-tag'
	// },
]

export default {
  components: {
   Icon
  },
	data() {
		return {
			menus: menuList1,
      menus1: menuList2,
      menus2: menuList3,
      submenu:submenuList,
      isTestMenuActive:false,
      isTestsubMenuActive:false,
      openeds:[]

		};
	},
	computed: {
    ...mapState({
      tags: state => state.tags,
    }),
		username() {
			return window.sessionStorage.getItem('username');
		},
    avatar() {
		  return window.sessionStorage.getItem('avatar');
    }
	},
	methods: {
     ...mapMutations(['clearEnvId','delTags']),
		handleCommand(cmd) {
			if (cmd === 'select') {
				this.$router.push({ name: 'allProject' });
				window.sessionStorage.removeItem('messageStore');
			  this.clearEnvId();
			  this.tags.forEach(item => {
          this.delTags(item.path)});

			}
			else if (cmd === 'logout') {
			  this.clearEnvId();
        this.tags.forEach(item => {
          this.delTags(item.path)});
				window.sessionStorage.removeItem('token');
				window.sessionStorage.removeItem('username');
				window.sessionStorage.removeItem('messageStore');
				window.sessionStorage.removeItem('avatar');
				this.$router.push({ name: 'login' });
			}
		}
	}
};
</script>

<style scoped>
.user_box {
  cursor: pointer;
	height: 53px;
	line-height: 53px;
	display: flex;
	align-items: center;
  background-color: #001529;
}
.u_head {
	height: 53px;
	border-radius: 50%;
  width: 40px;
  align-items: center;
}
.el-menu-item.is-active {
      background-color: #409eff !important;
      color: #fff;
      span {
        color: #fff !important;
      }
}
.username {
  height: 53px;
  position: relative;
  top: -23px;
  margin-left: 6px;
}
.colored-icon {
  color: rgb(245, 108, 108);
}
</style>
