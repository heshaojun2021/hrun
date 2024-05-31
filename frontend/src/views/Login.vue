<template>
	<LoginBack>
		<div class="login_box">
			<!-- log -->
			<div class="logo_box" ><img src="../assets/images/login1.png" /></div>
        <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick" >
    <el-tab-pane label="User" name="first">User</el-tab-pane>
    <el-tab-pane label="Config" name="second">Config</el-tab-pane>
  </el-tabs>
      <el-menu
        class="el-menu-demo"
        mode="horizontal"
        background-color="#000000"
        style="display: flex; justify-content: space-between; padding-bottom: 10px;color: #fff;font-size: 20px"
      >
        <el-menu-item index="1">登录</el-menu-item>
        <el-menu-item index="2">注册</el-menu-item>
      </el-menu>
			<!-- label-width是用占位的 -->
			<el-form ref="loginRef" class="login_from" :model="loginForm" :rules="rulesLogin">
				<!-- 账号密码输入框 -->
				<el-form-item prop="username">
					<el-input size="default" v-model="loginForm.username" prefix-icon="el-icon-user" placeholder="请输入账号"></el-input>
				</el-form-item>
				<el-form-item prop="password">
					<el-input type="password" size="default" v-model="loginForm.password" placeholder="请输入密码" prefix-icon="el-icon-lock" show-password></el-input>
				</el-form-item>
				<el-form-item size="mini" label="记住用户" style="margin-top: 10px;"><el-switch v-model="status" size="default" active-color="#1296db"></el-switch></el-form-item>
				<!-- 按钮 -->
				<el-form-item class="btns">
					<el-button size="default" style="color:#fff;width: 100%;background: #1296db;border: 0;" @click="login">登&nbsp;&nbsp; 录</el-button>
				</el-form-item>
			</el-form>
			<div style="color: #fff;">
				没有账号?
				<span  @click="clickRegister" style="color:#1296db;cursor:pointer;">点击注册</span>
			</div>
		</div>
	</LoginBack>
</template>

<script type="text/javascript">
import LoginBack from '../components/common/LoginBack.vue';

export default {
	components: {
		LoginBack
	},
	data() {
    return {
			// 登录的数据对象
			loginForm: {
				username: '',
				password: ''
			},
			status: false,
			rulesLogin: {
				// 验证用户名是否合法
				username: [
					{
						required: true,
						message: '请输入登录账号',
						trigger: 'blur'
					}
				],
				// 验证密码是否合法
				password: [
					{
						required: true,
						message: '请输入登录密码',
						trigger: 'blur'
					}
				]
			},
      userIcon:[
        {id:1,Emojis:"streamline-emojis:amusing-face"},
        {id:2,Emojis:"streamline-emojis:amazed-face"},
        {id:3,Emojis:"streamline-emojis:anxious-face"},
        {id:4,Emojis:"streamline-emojis:rolling-on-the-floor-laughing-1"},
        {id:5,Emojis:"streamline-emojis:beaming-face-with-smiling-eyes"},
        {id:6,Emojis:"streamline-emojis:astonished-face"},
        {id:7,Emojis:"streamline-emojis:face-screaming-in-fear"},
        {id:8,Emojis:"streamline-emojis:face-with-raised-eyebrow"},
        {id:9,Emojis:"streamline-emojis:face-with-rolling-eyes"},
        {id:10,Emojis:"streamline-emojis:face-with-tongue"},
        {id:11,Emojis:"streamline-emojis:face-without-mouth"},
        {id:12,Emojis:"streamline-emojis:drooling-face-1"},
        {id:13,Emojis:"streamline-emojis:grimacing-face"},
        {id:14,Emojis:"streamline-emojis:grinning-face-with-sweat"},
        {id:15,Emojis:"streamline-emojis:face-blowing-a-kiss"},
        {id:16,Emojis:"streamline-emojis:hushed-face-2"},
        {id:17,Emojis:"streamline-emojis:lying-face"},
        {id:18,Emojis:"streamline-emojis:star-struck-1"},
        {id:19,Emojis:"streamline-emojis:winking-face"},
        {id:20,Emojis:"streamline-emojis:upside-down-face"}
      ]
		};
	},
	methods: {
		clickRegister() {
    this.$router.push({name: 'createUser'})
		},
    userAvatar() {
      const randomIndex = Math.floor(Math.random() * this.userIcon.length);
      const selectedEmojis = this.userIcon[randomIndex];
      window.sessionStorage.setItem('avatar', selectedEmojis.Emojis);

    },
		// 登录的方法
		login() {
			// 通过表单的validate方法来验证表单，验证的结果会传递到validate的回调函数中
			this.$refs.loginRef.validate(async vaild => {
				// 判断是否验证通过，不通过则直接retrue
				if (!vaild) return;
				// 发送请求
				const response = await this.$api.login(this.loginForm);
				// 判断是否登录失败
				if (response.status != 200) return;
				const result = response.data;
				// 1、弹出登录成功
				this.$message({
					type: 'success',
					message: '登录成功',
					duration: 1000
				});
				// 2、获取token,保存到客户端的sessionStorage中
        // 保存用户头像到sessionStorage
        this.userAvatar()
				window.sessionStorage.setItem('token', result.token);
				window.sessionStorage.setItem('username', this.loginForm.username);
				if (this.status) {
					window.localStorage.setItem('userinfo', JSON.stringify(this.loginForm));
				} else {
					window.localStorage.removeItem('userinfo');
				}
				// 3、通过编程式导航跳转到登录之后的页面中
				this.$router.push({ name: 'allProject' })
			});
		}
	},
	mounted() {
		const userinfo = window.localStorage.getItem('userinfo');
		if (userinfo) {
			this.loginForm = JSON.parse(userinfo);
			this.status = true;
		}
	}
};
</script>

<style scoped>
	/* 登录框的样式 */
	.login_box {
		color: #fff;
		width: 400px;
		padding-top: 150px;
		margin: 0 auto;

	}

	/* logo居中 */
	.logo_box {
		text-align: center;
    height: 100px;
	}
.el-menu.el-menu--horizontal {
     border-bottom: none;
}
.el-menu--horizontal>.el-menu-item.is-active {
    border-bottom: 2px solid var(--el-color-primary);
     color: var(--el-color-primary);
}
.el-menu--horizontal>.el-menu-item {
    float: left;
    height: 40px;
    line-height: 40px;
    margin: 0;
    border-bottom: 2px solid transparent;
    color: var(--el-text-color-secondary);
    font-size: 16px;
}
</style>
