<template>
	<LoginBack>
		<div class="login_box">
			<div class="logo_box" ><img src="../assets/images/logo.png" /></div>
        <el-tabs v-model="activeName" class="demo-tabs">
          <el-tab-pane label="登 录" name="first">
            <el-form ref="loginRef" class="login_from" :model="loginForm" :rules="rulesLogin">
              <el-form-item prop="username">
                <el-input size="default" v-model="loginForm.username" prefix-icon="el-icon-user" placeholder="请输入账号"></el-input>
              </el-form-item>
              <el-form-item prop="password">
                <el-input type="password" size="default" v-model="loginForm.password" placeholder="请输入密码" prefix-icon="el-icon-lock" show-password></el-input>
              </el-form-item>
              <div style="display: flex; justify-content: space-between;">
                  <div>
                      <el-form-item size="mini" label="记住用户" style="margin-top: 6px;">
                          <el-switch v-model="status" size="default" active-color="#1296db"></el-switch>
                      </el-form-item>
                  </div>
                  <div style="color: #fff;margin-top: 10px;">
                      没有账号?
                      <span @click="clickRegister(activeName)" style="color:#1296db;cursor:pointer;">去注册</span>
                  </div>
              </div>
              <!-- 按钮 -->
              <el-form-item>
                <el-button size="default" type="primary" style="width: 100%" @click="login">登&nbsp;&nbsp; 录</el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          <el-tab-pane label="注 册" name="second">
            <el-form class="login_from" :model="createForm">
              <el-form-item>
                <el-input clearable :readonly="readonlyInput" @focus="cancelReadOnly" size="default" v-model="createForm.username" prefix-icon="el-icon-user" placeholder="请输入账号"></el-input>
              </el-form-item>
              <el-form-item>
                <el-input clearable :readonly="readonlyInput" @focus="cancelReadOnly"  type="password" size="default" v-model="createForm.password" placeholder="请输入密码" prefix-icon="el-icon-lock" show-password></el-input>
              </el-form-item>
              <div style="display: flex; justify-content: space-between;">
                  <div>
                      <el-form-item size="mini" label="记住用户" style="margin-top: 6px;">
                          <el-switch v-model="status" size="default" active-color="#1296db"></el-switch>
                      </el-form-item>
                  </div>
                  <div style="color: #fff;margin-top: 10px;">
                      已有账号?
                      <span @click="clickRegister(activeName)" style="color:#1296db;cursor:pointer;">去登录</span>
                  </div>
              </div>
              <el-form-item >
                <el-button size="default" type="primary" style="width: 100%" @click="createClick">注&nbsp;&nbsp; 册</el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
        </el-tabs>
		</div>
	</LoginBack>
</template>

<script type="text/javascript">
import LoginBack from '../components/common/LoginBack.vue';
import {ElNotification} from "element-plus";
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
      createForm: {
        username: '',
				password: '',
        project_id: 1
      },
			status: false,
      readonlyInput: true,
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
      ],
      activeName: 'first'
		};
	},
	methods: {
		clickRegister(activeName) {
		  if (activeName ==='first') {
        this.activeName = 'second'
      }else {
		    this.activeName = 'first'
      }
		},
    cancelReadOnly() {
      this.readonlyInput = false;
    },
    async createClick() {
        const params = {...this.createForm}
        const response = await this.$api.createUser(params)
        if (response.status===201) {
          ElNotification({
              duration: 1000,
              title: '创建成功，可以登录咯',
              type: 'success',
            })
          this.activeName = 'first'
          this.createForm = {
              username: '',
              password: '',
              project_id: 1
            };
        }
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
				if (!vaild) return;
				// 发送请求
				const response = await this.$api.login(this.loginForm);
				// 判断是否登录失败
				if (response.status != 200) return;
				const result = response.data;
        ElNotification({
              duration: 1000,
              title: '登录成功',
              type: 'success',
            })
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
		width: 500px;
		padding-top: 100px;
		margin: 0 auto;

	}

	/* logo居中 */
	.logo_box {
    margin-top: 70px;
		text-align: center;
    height: 130px;
	}

/deep/ .el-tabs__item {
    text-align: center;
    padding: 0 0;
    height: 40px;
    -webkit-box-sizing: border-box;
    box-sizing: border-box;
    line-height: 40px;
    display: inline-block;
    list-style: none;
    font-size: 18px;
    font-weight: 500;
    position: relative;
    width: 250px;
    color: aliceblue;
}
/deep/ .el-form-item__label {
    color: aliceblue;

}
</style>
