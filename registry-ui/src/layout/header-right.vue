<!-- 顶栏右侧区域按钮 -->
<template>
  <div class="ele-admin-header-tool">
    <div
      class="ele-admin-header-tool-item hidden-sm-and-down"
      @click="changeFullscreen"
    >
      <fullscreen-exit-outlined v-if="fullscreen" />
      <fullscreen-outlined v-else />
    </div>
    <!-- 语言切换 -->
    <!-- <div class="ele-admin-header-tool-item">
      <a-dropdown placement="bottomCenter" :overlay-style="{minWidth: '120px', paddingTop: '17px'}">
        <global-outlined style="transform: scale(1.08);"/>
        <template #overlay>
          <a-menu :selected-keys="language" @click="changeLanguage">
            <a-menu-item key="en">English</a-menu-item>
            <a-menu-item key="zh_CN">简体中文</a-menu-item>
            <a-menu-item key="zh_TW">繁體中文</a-menu-item>
          </a-menu>
        </template>
      </a-dropdown>
    </div> -->
    <!-- 消息通知 -->
    <!-- <div class="ele-admin-header-tool-item">
      <ele-notice/>
    </div> -->
    <!-- 用户信息 -->
    <div class="ele-admin-header-tool-item">
      <a-dropdown
        placement="bottomCenter"
        :overlay-style="{ minWidth: '120px' }"
      >
        <div class="ele-admin-header-avatar">
          <a-avatar :src="loginUser.avatar" />
          <span>{{ loginUser.nickname }}&nbsp;</span>
          <down-outlined />
        </div>
        <template #overlay>
          <a-menu @click="onUserDropClick">
            <a-menu-item key="profile">
              <div class="ele-cell">
                <user-outlined />
                <div class="ele-cell-content">
                  {{ $t("layout.header.profile") }}
                </div>
              </div>
            </a-menu-item>
            <a-menu-item key="password">
              <div class="ele-cell">
                <key-outlined />
                <div class="ele-cell-content">
                  {{ $t("layout.header.password") }}
                </div>
              </div>
            </a-menu-item>
            <a-menu-divider />
            <a-menu-item key="logout">
              <div class="ele-cell">
                <logout-outlined />
                <div class="ele-cell-content">
                  {{ $t("layout.header.logout") }}
                </div>
              </div>
            </a-menu-item>
          </a-menu>
        </template>
      </a-dropdown>
    </div>
  </div>
</template>

<script>
import { createVNode } from "vue";
import {
  DownOutlined,
  UserOutlined,
  KeyOutlined,
  LogoutOutlined,
  ExclamationCircleOutlined,
  FullscreenOutlined,
  FullscreenExitOutlined,
  // GlobalOutlined
} from "@ant-design/icons-vue";
import { toggleFullscreen, isFullscreen } from "ele-admin-pro/packages/util.js";
// import EleNotice from './notice';

export default {
  name: "EleHeaderRight",
  components: {
    DownOutlined,
    UserOutlined,
    KeyOutlined,
    LogoutOutlined,
    FullscreenOutlined,
    FullscreenExitOutlined,
    // GlobalOutlined,
    // EleNotice
  },
  emits: ["item-click", "change-language"],
  props: {
    // 是否显示打开设置抽屉按钮
    showSetting: {
      type: Boolean,
      default: true,
    },
  },
  computed: {
    // 当前登录用户信息
    loginUser() {
      return this.$store.state.user.user;
    },
    // 当前语言
    language() {
      return [this.$i18n.locale];
    },
  },
  data() {
    return {
      // 是否全屏状态
      fullscreen: false,
    };
  },
  methods: {
    /* 个人信息下拉菜单点击 */
    onUserDropClick({ key }) {
      if (key === "logout") {
        // 退出登录
        this.$confirm({
          title: this.$t("layout.logout.title"),
          content: this.$t("layout.logout.message"),
          icon: createVNode(ExclamationCircleOutlined),
          maskClosable: true,
          onOk: () => {
            // 调用接口退出登录
            this.$http
              .get("/index/logout")
              .then((res) => {
                if (res.data.code === 0) {
                  // 清除缓存的token
                  this.$store.dispatch("user/removeToken").then(() => {
                    location.replace("/login"); // 这样跳转避免再次登录重复注册动态路由
                  });
                } else {
                  this.$message.error(res.data.msg);
                }
              })
              .catch((e) => {
                this.$message.error(e.message);
              });
          },
        });
      } else if (key === "profile") {
        this.$router.push("/user/profile");
      } else if (key === "password") {
        this.$emit("item-click", "password");
      }
    },
    /* 打开设置抽屉 */
    openSetting() {
      this.$emit("item-click", "setting");
    },
    /* 全屏切换 */
    changeFullscreen() {
      try {
        this.fullscreen = toggleFullscreen();
      } catch (e) {
        this.$message.error("您的浏览器不支持全屏模式");
      }
    },
    /* 检查全屏状态 */
    checkFullscreen() {
      this.fullscreen = isFullscreen();
    },
    /* 切换语言 */
    changeLanguage({ key }) {
      this.$emit("change-language", key);
    },
  },
};
</script>
