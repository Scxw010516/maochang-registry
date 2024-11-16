/** 主入口js */
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import axios from "axios";
import VueAxios from "vue-axios";
import "./config/axios-config";
import { createPinia } from "pinia";
import AntdVue from "ant-design-vue";
// import "ant-design-vue/dist/antd.css";
import "ant-design-vue/dist/reset.css";
// @ts-ignore
import EleAdminPro from "ele-admin-pro";
// import ModalUtil from "ele-admin-pro/packages/modal-util.vue";
import i18n from "./lang";
import { setGlobalOptions } from "vue-request";

const pinia = createPinia();
const app = createApp(App);
app.use(router);
app.use(VueAxios, axios);
app.use(pinia);
// app.use(permission);
app.use(EleAdminPro);
// app.use(ModalUtil);
app.use(i18n);
app.use(AntdVue);
app.mount("#app");
// 设置全局请求配置vue-request
setGlobalOptions({
  manual: true,
});
