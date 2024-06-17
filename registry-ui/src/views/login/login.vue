<template>
  <div
    :class="[
      'login-wrapper',
      ['', 'login-form-right', 'login-form-left'][direction],
    ]"
  >
    <a-form
      ref="form"
      :model="form"
      :rules="rules"
      layout="vertical"
      class="login-form ele-bg-white"
    >
      <h4>{{ $t("login.title") }}</h4>
      <a-form-item name="username">
        <a-input
          allow-clear
          size="large"
          v-model:value="form.username"
          :placeholder="$t('login.username')"
        >
          <template #prefix>
            <user-outlined />
          </template>
        </a-input>
      </a-form-item>
      <a-form-item name="password">
        <a-input-password
          size="large"
          v-model:value="form.password"
          :placeholder="$t('login.password')"
        >
          <template #prefix>
            <lock-outlined />
          </template>
        </a-input-password>
      </a-form-item>
      <a-form-item name="captcha">
        <div class="login-input-group">
          <a-input
            allow-clear
            size="large"
            v-model:value="form.captcha"
            :placeholder="$t('login.captcha')"
          >
            <template #prefix>
              <safety-certificate-outlined />
            </template>
          </a-input>
          <a-button class="login-captcha" @click="changeCode">
            <img v-if="captcha" :src="captcha" alt="" />
          </a-button>
        </div>
      </a-form-item>
      <a-form-item>
        <a-checkbox v-model:checked="form.remember">
          {{ $t("login.remember") }}
        </a-checkbox>
      </a-form-item>
      <a-form-item>
        <a-button
          block
          size="large"
          type="primary"
          :loading="loading"
          @click="doSubmit"
        >
          {{ loading ? $t("login.loading") : $t("login.login") }}
        </a-button>
      </a-form-item>
    </a-form>
    <div class="login-copyright">
      copyright © 2021~2024 djangoadmin.cn all rights reserved.
    </div>
  </div>
</template>

<script>
import {
  LockOutlined,
  SafetyCertificateOutlined,
  UserOutlined,
} from "@ant-design/icons-vue";
import setting from "@/config/setting";

export default {
  name: "Login",
  components: {
    UserOutlined,
    LockOutlined,
    SafetyCertificateOutlined,
  },
  data() {
    return {
      // 登录框方向, 0居中, 1居右, 2居左
      direction: 0,
      // 加载状态
      loading: false,
      // 表单数据
      form: {
        username: "admin",
        password: "123456",
        idKey: "",
        remember: true,
      },
      // 验证码base64数据
      captcha: "",
      // 验证码内容, 实际项目去掉
      text: "",
    };
  },
  computed: {
    // 表单验证规则
    rules() {
      return {
        username: [
          {
            required: true,
            message: this.$t("login.username"),
            type: "string",
            trigger: "blur",
          },
        ],
        password: [
          {
            required: true,
            message: this.$t("login.password"),
            type: "string",
            trigger: "blur",
          },
        ],
        captcha: [
          {
            required: true,
            message: this.$t("login.captcha"),
            type: "string",
            trigger: "blur",
          },
        ],
      };
    },
    // 当前语言
    languages() {
      return [this.$i18n.locale];
    },
  },
  mounted() {
    if (setting.takeToken()) {
      return this.goHome();
    }
    this.changeCode();
  },
  methods: {
    /* 提交 */
    doSubmit() {
      this.$refs.form
        .validate()
        .then(() => {
          this.loading = true;
          this.$http.post("/login", this.form).then((res) => {
            this.loading = false;
            if (res.data.code === 0) {
              this.$message.success("登录成功");
              this.$store
                .dispatch("user/setToken", {
                  token: "Bearer " + res.data.data.access_token,
                  remember: this.form.remember,
                })
                .then(() => {
                  this.goHome();
                });
            } else {
              this.$message.error(res.data.msg);
              this.changeCode();
            }
          });
        })
        .catch(() => {});
    },
    /* 跳转到首页 */
    goHome() {
      const query = this.$route.query;
      const path = query && query.from ? query.from : "/";
      this.$router.push(path).catch(() => {});
    },
    /* 更换图形验证码 */
    changeCode() {
      // 这里演示的验证码是后端返回base64格式的形式, 如果后端地址直接是图片请参考忘记密码页面
      this.$http
        .get("/captcha")
        .then((res) => {
          if (res.data.code === 0) {
            this.captcha = res.data.data;
            this.form.idKey = res.data.idkey;
          } else {
            this.$message.error(res.data.msg);
          }
        })
        .catch((e) => {
          this.$message.error(e.message);
        });
    },
    /* 切换语言 */
    changeLanguage({ key }) {
      this.$i18n.locale = key;
      localStorage.setItem("i18n-lang", key);
      this.$refs.form.clearValidate();
    },
  },
};
</script>

<style scoped>
/* 背景 */
.login-wrapper {
  padding: 48px 16px 0 16px;
  position: relative;
  box-sizing: border-box;
  background-image: url("~@/assets/bg-login.png");
  background-repeat: no-repeat;
  background-size: cover;
  min-height: 100vh;
}

.login-wrapper:before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.2);
}

/* 卡片 */
.login-form {
  width: 360px;
  margin: 0 auto;
  max-width: 100%;
  padding: 0 28px;
  box-sizing: border-box;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15);
  border-radius: 2px;
  position: relative;
  z-index: 2;
}

.login-form-right .login-form {
  margin: 0 15% 0 auto;
}

.login-form-left .login-form {
  margin: 0 auto 0 15%;
}

.login-form h4 {
  padding: 22px 0;
  text-align: center;
}

/* 验证码 */
.login-input-group {
  display: flex;
  align-items: center;
}

.login-input-group :deep(.ant-input-affix-wrapper) {
  flex: 1;
}

.login-input-group .login-captcha {
  width: 102px;
  height: 40px;
  margin-left: 10px;
  padding: 0;
}

.login-input-group .login-captcha > img {
  width: 100%;
  height: 100%;
}

/* 第三方登录图标 */
.login-oauth-icon {
  color: #fff;
  padding: 5px;
  margin: 0 12px;
  font-size: 18px;
  border-radius: 50%;
  cursor: pointer;
}

/* 底部版权 */
.login-copyright {
  color: #eee;
  text-align: center;
  padding: 48px 0 22px 0;
  position: relative;
  z-index: 1;
}

/* 响应式 */
@media screen and (min-height: 640px) {
  .login-wrapper {
    padding-top: 0;
  }

  .login-form {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translateX(-50%);
    margin-top: -230px;
  }

  .login-form-right .login-form,
  .login-form-left .login-form {
    left: auto;
    right: 15%;
    transform: translateX(0);
    margin: -230px auto auto auto;
  }

  .login-form-left .login-form {
    right: auto;
    left: 15%;
  }

  .login-copyright {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
  }
}

@media screen and (max-width: 768px) {
  .login-form-right .login-form,
  .login-form-left .login-form {
    left: 50%;
    right: auto;
    margin-left: 0;
    margin-right: auto;
    transform: translateX(-50%);
  }
}
</style>
