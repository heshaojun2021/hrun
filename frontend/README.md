#  frontend

## 安装node.js
```
官网地址：https://nodejs.org/en
```

## 项目初始化
```
npm install
```

### 开发或测试环境启动
```
npm run serve
```

### 生产环境发布打包
```
npm run build
```
## 目录结构
```
dist -- 存放生产部署打包配置
node_modules -- 项目所需的各种依赖包和模块
public -- 浏览器展示的启动标签等信息
src：
    api -- 存放所有的接口
    assets -- 存放全局的js、css、图片等信息
    components -- 存放公共组件
    plugins -- element的配置文件
    router -- path配置
    store -- 数据共享等配置
    views -- 各个页面的vue代码存放
```
### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
