import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import installElementPlus from './plugins/element'
import api from './api/index.js'
import './assets/css/main.css'
import tools from './assets/js/tools.js'
const app = createApp(App)

//将请求对象绑定为应用的全局属性$api
app.config.globalProperties.$api = api

//将工具函数绑定为全局的属性
app.config.globalProperties.$tools = tools

//  将定义echarts图表对象绑定为全局属性
import chart from './chart/index.js'
app.config.globalProperties.$chart = chart
installElementPlus(app)
app.use(store).use(router).mount('#app')