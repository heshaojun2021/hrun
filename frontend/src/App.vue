<template>
  <el-config-provider :locale="locale">
    <router-view />
  </el-config-provider>
</template>

<script>

import { ElConfigProvider } from 'element-plus'
// 中文包
import zhCn from 'element-plus/lib/locale/lang/zh-cn'
export default {
   components: {
    [ElConfigProvider.name]: ElConfigProvider
  },
  setup() {
    // 切换为中文
    let locale = zhCn
    return {
      locale
    }
  },

	created() {
		//在页面刷新时将vuex里的信息保存到 sessionStorage里
		window.addEventListener('beforeunload', () => {
			sessionStorage.setItem('messageStore', JSON.stringify(this.$store.state));
		});
		//在页面加载时读取sessionStorage里的状态信息
		sessionStorage.getItem('messageStore') && this.$store.replaceState(Object.assign(this.$store.state, JSON.parse(sessionStorage.getItem('messageStore'))));
	}
};
</script>

<style></style>
