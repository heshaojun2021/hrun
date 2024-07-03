import {
    createRouter, createWebHashHistory
} from 'vue-router'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
import store from '../store/index.js'

const routes = [{
    path: '/',
    name: 'home',
    component: () => import( /* webpackChunkName: "about" */ '../views/Home.vue'),
    redirect: "/project",
    children: [
        {
            path: '/project', name: 'project', component: () => import('../views/Workbench/Project.vue'), meta: {
                name: "项目首页"
            }
        },
        {
            path: '/testscent', name: 'testscent', component: () => import('../views/TestScent.vue'), meta: {
                name: "测试场景"
            }
        }, {
            path: '/interface', name: 'interface', component: () => import('../views/Interface.vue'), meta: {
                name: "接口管理"
            }
        }, {
            path: '/teststep', name: 'teststep', component: () => import('../views/TestStep.vue'), meta: {
                name: "接口测试"
            }
        }, {
            path: '/testplan', name: 'testplan', component: () => import('../views/TestPlan.vue'), meta: {
                name: "测试计划"
            }
        },

        {
            path: '/testenv', name: 'testenv', component: () => import('../views/TestEnv.vue'), meta: {
                name: "测试环境"
            }
        }, {
            path: '/crontab', name: 'crontab', component: () => import('../views/CronTab.vue'), meta: {
                name: "定时任务"
            }
        },

        {
            path: '/report/:id', name: 'report', component: () => import('../views/Reports/Report.vue'), meta: {
                name: "测试报告"
            }
        }, {
            path: '/bugs', name: 'bug', component: () => import('../views/BugManage.vue'), meta: {
                name: "bug管理"
            }
        }, {
            path: '/records', name: 'records', component: () => import('../views/Reports/Records.vue'), meta: {
                name: "测试报表"
            }
        },{
            path: '/users', name: 'user', component: () => import('../views/User.vue'), meta: {
                name: "用户管理"
            }
        }, {
            path: '/excel', name: 'excel', component: () => import('../views/excel.vue'), meta: {
                name: "需求问题记录表"
            }
        },{
            path: '/reportPush', name: 'push', component: () => import('../views/Reports/ReportPush.vue'), meta: {
                name: "报告通知"
            }
        },
            {
            path: '/PerformanceTask', name: 'Performance', component: () => import('../views/PerformanceTest/PerformanceTask.vue'), meta: {
                name: "性能任务"
            }
        }, {
            path: '/performanceMonitor', name: 'performanceMonitor', component: () => import('../views/PerformanceTest/Workplace.vue'), meta: {
                name: "性能监控"
            }
        }, {
            path: '/new-interface', name: 'interfaceNew', component: () => import('../views/Interface/InterfaceNew.vue'), meta: {
                name: "接口管理"
            }
        }, {
            path: '/TestCase', name: 'TestCase', component: () => import('../views/TestCase/TestCase.vue'), meta: {
                name: "用例管理"
            }
        },
        {
            path: '/TestCaseDetail', name: 'TestCaseDetail', component: () => import('../views/TestCase/TestCaseDetail.vue'), meta: {
                name: "用例详情"
            }
        },
        {
            path: '/new-testplan', name: 'new-testplan', component: () => import('../views/TestPlan/TestPlanNew.vue'), meta: {
                name: "测试计划"
            }
        },
    ]
},
    {
    path: '/createUser', name: 'createUser', component: () => import('../views/CreateUser')},
    {
    path: '/login', name: 'login', component: () => import( /* webpackChunkName: "about" */ '../views/Login.vue'),

    },
    {
    path: '/allProject',
    name: 'allProject',
    component: () => import('../views/Workbench/AllProject.vue')
    },
    {
    path: '/404',
    name: '404',
    component: () => import('../views/404.vue')
    },
    // 输入不存在的链接重定向到404页面
    {
    path: '/:catchAll(.*)',
    redirect: '/404'
    },
    {
    path: '/PushEport/:id', name: 'PushrEport', component: () => import('../views/Reports/Report.vue'), meta: {
        name: "推送的测试报告查看"
        }
    },
]

const router = createRouter({
    history: createWebHashHistory(), routes
})

// 设置路由导航守卫
router.beforeEach((to, from, next) => {
　   NProgress.start();
    // 添加到路由到标签列表中
    if (to.meta.name) {
        // 添加标签
        store.commit('addTags', {
            name: to.meta.name, path: to.path
        })
    }

    // 获取登录之后的token值
    const isAuthenticated = window.sessionStorage.getItem('token')
    // 如果用户正在访问注册页面，允许未登录用户继续访问
    if (to.name === 'createUser' ) {
        next()
    } else {
        // 其他情况下进行登录状态的检查
        if (to.name !== 'login' && to.name !== 'PushrEport' && !isAuthenticated) {
            next({
                name: 'login'
            })
        } else {
            next()
        }
    }
})
router.afterEach(() => {
  NProgress.done()
})

export default router
