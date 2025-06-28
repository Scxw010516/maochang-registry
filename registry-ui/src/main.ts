/** 主入口js */
import { createApp } from "vue";
import App from "./App.vue";
import { createPinia } from "pinia";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import router from "@/router/index";
import axios from "axios";
import VueAxios from "vue-axios";
import "@/config/axios-config";
import AntdVue from "ant-design-vue";
import "ant-design-vue/dist/reset.css";

const app = createApp(App);
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);
app.use(pinia);
app.use(router);
app.use(VueAxios, axios);
app.use(AntdVue);
app.mount("#app");
