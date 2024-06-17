<template>
  <div class="ele-body ele-body-card">
    <a-row :gutter="16">
      <a-col :lg="6" :md="8" :sm="24" :xs="24">
        <a-card :bordered="false">
          <div class="ele-text-center">
            <div class="user-info-avatar-group">
              <!-- 头像上传 -->
              <uploadImage :limit="1" v-model:value="form.avatar" />
            </div>

            <h1>@一米阳光</h1>
            <div>
              打造一款基于Python语言的敏捷开发框架，用先进的技术思维和软件框架产品赋能开发者、助力企业发展，为企业提供全方位的解决方案！
            </div>
          </div>
          <div class="user-info-list">
            <div class="ele-cell">
              <user-outlined />
              <div class="ele-cell-content">资深架构师</div>
            </div>
            <div class="ele-cell">
              <home-outlined />
              <div class="ele-cell-content">北京DjangoAdmin研发中心</div>
            </div>
            <div class="ele-cell">
              <environment-outlined />
              <div class="ele-cell-content">中国 • 北京市 • 朝阳区</div>
            </div>
            <div class="ele-cell">
              <tag-outlined />
              <div class="ele-cell-content">
                Python、Django、Vue3.x、AntDesign
              </div>
            </div>
          </div>
          <a-divider dashed />
          <h6>标签</h6>
          <div class="user-info-tags">
            <a-tag>一米阳光</a-tag>
            <a-tag>一米阳光</a-tag>
            <a-tag>一米阳光</a-tag>
            <a-tag>一米阳光</a-tag>
            <a-tag>一米阳光</a-tag>
            <a-tag>一米阳光</a-tag>
            <a-tag>一米阳光</a-tag>
            <a-tag>一米阳光</a-tag>
            <a-tag>一米阳光</a-tag>
            <a-tag>一米阳光</a-tag>
            <a-tag>一米阳光</a-tag>
            <a-tag>一米阳光</a-tag>
          </div>
        </a-card>
      </a-col>
      <a-col :lg="18" :md="16" :sm="24" :xs="24">
        <a-card :bordered="false" class="user-info-tabs">
          <a-tabs v-model:active-key="active" size="large">
            <a-tab-pane tab="基本信息" key="info">
              <a-form
                ref="form"
                :model="form"
                :rules="rules"
                :label-col="{ md: { span: 6 }, sm: { span: 24 } }"
                :wrapper-col="{ md: { span: 18 }, sm: { span: 24 } }"
              >
                <a-form-item label="姓名:" name="realname">
                  <a-input
                    v-model:value="form.realname"
                    placeholder="请输入姓名"
                    allow-clear
                  />
                </a-form-item>
                <a-form-item label="昵称:" name="nickname">
                  <a-input
                    v-model:value="form.nickname"
                    placeholder="请输入昵称"
                    allow-clear
                  />
                </a-form-item>
                <a-form-item label="性别:" name="gender">
                  <a-select
                    allow-clear
                    placeholder="请选择性别"
                    v-model:value="form.gender"
                  >
                    <a-select-option :value="1">男</a-select-option>
                    <a-select-option :value="2">女</a-select-option>
                    <a-select-option :value="3">保密</a-select-option>
                  </a-select>
                </a-form-item>
                <a-form-item label="联系方式:" name="mobile">
                  <a-input
                    v-model:value="form.mobile"
                    placeholder="请输入联系方式"
                    allow-clear
                  />
                </a-form-item>
                <a-form-item label="邮箱:" name="email">
                  <a-input
                    v-model:value="form.email"
                    placeholder="请输入邮箱"
                    allow-clear
                  />
                </a-form-item>
                <a-form-item label="详细地址:" name="address">
                  <a-input
                    v-model:value="form.address"
                    placeholder="请输入详细地址"
                    allow-clear
                  />
                </a-form-item>
                <a-form-item label="个人简介:">
                  <a-textarea
                    v-model:value="form.intro"
                    placeholder="请输入个人简介"
                    :rows="4"
                  />
                </a-form-item>
                <a-form-item :wrapper-col="{ md: { offset: 6 } }">
                  <a-button type="primary" @click="save" :loading="loading">
                    {{ loading ? "保存中.." : "保存更改" }}
                  </a-button>
                </a-form-item>
              </a-form>
            </a-tab-pane>
          </a-tabs>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script>
import {
  EnvironmentOutlined,
  HomeOutlined,
  TagOutlined,
  UserOutlined,
} from "@ant-design/icons-vue";
import uploadImage from "@/components/uploadImage";
import setting from "@/config/setting";

export default {
  name: "UserInfo",
  components: {
    UserOutlined,
    HomeOutlined,
    EnvironmentOutlined,
    TagOutlined,
    uploadImage,
  },
  data() {
    return {
      // tab页选中
      active: "info",
      // 表单数据
      form: {},
      // 表单验证规则
      rules: {
        realname: [
          {
            required: true,
            message: "请输入姓名",
            type: "string",
            trigger: "blur",
          },
        ],
        nickname: [
          {
            required: true,
            message: "请输入昵称",
            type: "string",
            trigger: "blur",
          },
        ],
        gender: [
          {
            required: true,
            message: "请选择性别",
            type: "number",
            trigger: "blur",
          },
        ],
        email: [
          {
            required: true,
            message: "请输入邮箱",
            type: "string",
            trigger: "blur",
          },
        ],
      },
      // 保存按钮loading
      loading: false,
      // 是否显示裁剪弹窗
      showCropper: false,
    };
  },
  mounted() {
    // 获取用户信息
    this.getUserInfo();
  },
  methods: {
    /* 获取当前用户信息 */
    getUserInfo() {
      if (setting.userUrl) {
        this.$http
          .get(setting.userUrl)
          .then((res) => {
            const result = setting.parseUser
              ? setting.parseUser(res.data)
              : res.data;
            if (result.code === 0) {
              // 赋予对象值
              var formData = JSON.parse(JSON.stringify(result.data));
              this.form = Object.assign({
                realname: formData.realname,
                nickname: formData.nickname,
                gender: formData.gender,
                mobile: formData.mobile,
                email: formData.email,
                address: formData.address,
                intro: formData.intro,
                avatar: formData.avatar,
              });
            } else if (result.msg) {
              this.$message.error(result.msg);
            }
          })
          .catch((e) => {
            console.error(e);
            this.$message.error(e.message);
          });
      }
    },
    /* 保存更改 */
    save() {
      this.$refs.form
        .validate()
        .then(() => {
          this.loading = true;
          this.$http
            .put("/index/userInfo", this.form)
            .then((res) => {
              this.loading = false;
              if (res.data.code === 0) {
                this.$message.success("保存成功");
              } else {
                this.$message.error(res.data.msg);
              }
            })
            .catch((e) => {
              this.loading = false;
              this.$message.error(e.message);
            });
        })
        .catch(() => {});
    },
  },
};
</script>

<style scoped>
/* 用户资料卡片 */
.user-info-avatar-group {
  margin: 16px 0;
  display: inline-block;
  position: relative;
  cursor: pointer;
}

.user-info-avatar-group .user-info-avatar-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #fff;
  font-size: 30px;
  display: none;
  z-index: 2;
}

/*.user-info-avatar-group:hover .user-info-avatar-icon {*/
/*  display: block;*/
/*}*/

/*.user-info-avatar-group:hover:after {*/
/*  content: "";*/
/*  position: absolute;*/
/*  top: 0;*/
/*  left: 0;*/
/*  width: 100%;*/
/*  height: 100%;*/
/*  border-radius: 50%;*/
/*  background-color: rgba(0, 0, 0, .3);*/
/*}*/

.user-info-avatar-group + h1 {
  margin-bottom: 8px;
}

/* 用户信息列表 */
.user-info-list {
  margin: 52px 0 32px 0;
}

.user-info-list .ele-cell + .ele-cell {
  margin-top: 16px;
}

.user-info-list + .ant-divider {
  margin-bottom: 16px;
}

/* 用户标签 */
.user-info-tags {
  margin: 16px 0 4px 0;
}

.user-info-tags .ant-tag {
  margin: 0 12px 8px 0;
}

/* 右侧卡片 */
.user-info-tabs :deep(.ant-card-body) {
  padding: 0;
}

.user-info-tabs :deep(.ant-tabs-tab) {
  padding-left: 4px;
  padding-right: 4px;
  margin: 0 12px 0 28px !important;
}

.user-info-tabs .ant-form {
  max-width: 580px;
  margin-top: 20px;
  padding: 0 24px;
}

/* 用户账号绑定列表 */
.user-account-list {
  margin-bottom: 27px;
}

.user-account-list > .ele-cell {
  padding: 18px 34px;
}

.user-account-list .user-account-icon {
  color: #fff;
  padding: 8px;
  font-size: 26px;
  border-radius: 50%;
}

.user-account-list .user-account-icon.anticon-qq {
  background: #3492ed;
}

.user-account-list .user-account-icon.anticon-wechat {
  background: #4daf29;
}

.user-account-list .user-account-icon.anticon-alipay {
  background: #1476fe;
}
</style>
