<template>
  <div>
    <div class="mask">
      <div class="global">用户注册</div>
    </div>
    <div class="form-wrapper">
        <el-form  :model="addForm" label-width="100px" :rules="rulesUser" ref="UserRef">
              <el-form-item prop="username" label="账号">
                <el-input size="large" v-model="addForm.username"  maxlength="18" minlength="3" placeholder="请输入账号"  readonly onfocus="this.removeAttribute('readonly');" show-word-limi/>
              </el-form-item>
              <el-form-item label="密码" prop="password" >
                <el-input size="large" v-model="addForm.password"  type="password" show-password maxlength="18" minlength="3" placeholder="请输入密码" readonly onfocus="this.removeAttribute('readonly');"/>
              </el-form-item>
              <el-form-item label="手机号码" prop="mobile">
                <el-input size="large" v-model="addForm.mobile"  maxlength="11" minlength="11" placeholder="请输入手机号" show-word-limit/>
              </el-form-item>
              <el-form-item label="邮箱地址"><el-input size="large" v-model="addForm.email"  placeholder="请输入邮箱地址" readonly onfocus="this.removeAttribute('readonly');"/></el-form-item>
              <span class="dialog-footer">
                <el-button style="margin-left: 50px" type="primary" @click="submitForm" size="large">立即创建</el-button>
              </span>
        </el-form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      addForm: {
				username: '',
				mobile: '',
				email: '',
        password:'',
        project_id:'4',
        project_name:'示例项目',
			},
      rulesUser: {
				// 验证用户名是否合法
				username: [
					{
						required: true,
						message: '请输入用户名',
						trigger: 'blur'
					}
				],
				// 验证密码是否合法
				password: [
					{
						required: true,
						message: '请输入密码',
						trigger: 'blur'
					}
				],
       mobile: [
					{
						required: true,
						message: '请输入手机号',
						trigger: 'blur'
					}
				]
			}

    };
  },
  methods: {
    submitForm() {
      this.$refs.UserRef.validate(async vaild => {
				// 判断是否验证通过，不通过则直接return
				if (!vaild) return;

        const params = {...this.addForm}
        const response = await this.$api.createUser(params)
        if (response.status===201) {
          this.$message({
            type: 'success',
            message: '用户创建成功',
            duration: 1000})

          this.addForm = {
              username: '',
              mobile: '',
              email: '',
              password: '',
              project_id:'',
              project_name:''
            };
          setTimeout(() => {
              this.$router.push({name: 'login'})
            }, 1000); // 设置延迟时间为 1000 毫秒（1秒）

        }
      })
    },
  },
};
</script>


<style scoped>
.mask {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 999;
  width: 100%;
  height: 100%;
  background:#f5f7f9;
}
.global {
  font-size: 30px;
  color: #00aeff;
  display: flex;
  justify-content: center;
  padding-top: 50px;
}
.form-wrapper {
  position: fixed;
  top: 40%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  width: 500px;
}
.el-form {
    margin-left: -50px;
}
.dialog-footer {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}
</style>