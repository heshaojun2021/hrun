<template>
	<div class="home">
		<div class="left_box"><LeftMenu></LeftMenu></div>
		<div class="right_box">
			<!-- 顶部标签项 -->
			<Tags></Tags>
			<!-- 主体内容展示 -->
			<el-card class="main" body-style="padding:0"><router-view></router-view></el-card>
		</div>
	</div>
</template>

<script>
import LeftMenu from '../components/common/LeftMenu.vue';
import Tags from '../components/common/Tags.vue';
import {mapActions, mapState, mapMutations, mapGetters} from 'vuex';
export default {
	name: 'Home',
	components: {
		LeftMenu,
		Tags
	},
	methods: {
		...mapActions(['getAllInter', 'getAllScent', 'getAllEnvs', 'getAllPlan'])
	},
	created() {
		// this.getAllInter();
		// this.getAllScent();
		this.getAllEnvs();
		this.getAllPlan();
	}
};
</script>

<style type="text/css" scoped>
/* 背景颜色设置 */
.home {
	 background-image: linear-gradient(#001529, #001529) !important;
	/*background-image: linear-gradient(#001529, #00aa7f) !important;*/
	/* background: #00AA7F; */
}
/* 左侧盒子样式 */
.left_box {
	width: 202px;
	height: 100vh;
	border-right: solid 1px #fff;
}

/* 右侧盒子样式 */
.right_box {
	position: absolute;
	left: 200px;
	top: 0px;
	width: calc(100vw - 200px);
	height: 100vh;
  background:#f5f7f9
}
.main {
	background: #fff;
	height: calc(100vh - 53px);
	margin: 12px 12px 0 12px;
}
</style>
