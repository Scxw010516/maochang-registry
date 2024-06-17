<template>
  <a-config-provider
    :locale="locale"
    :theme="{ token: { colorPrimary: '#8675ff' } }"
  >
    <router-view />
  </a-config-provider>
</template>

<script>
// import zh_CN from "ele-admin-pro/packages/lang/zh_CN";
// import zh_TW from "ele-admin-pro/packages/lang/zh_TW";
// import en from "ele-admin-pro/packages/lang/en_US";
import zhCN from "ant-design-vue/es/locale/zh_CN";

// const languages = { zh_CN, zh_TW, en };
// const languages = { zhCN };
export default {
  data() {
    return {
      // locale: languages[this.$i18n.locale],
      locale: zhCN,
    };
  },
  computed: {
    // language() {
    //   return this.$i18n.locale;
    // },
  },
  watch: {
    // language() {
    //   this.locale = languages[this.language];
    // },
  },
};
</script>
