/**
 * axios配置
 */
import axios, { AxiosRequestConfig, AxiosResponse } from "axios";
// import { store } from "../store";
import router from "@/router/index";
import setting from "@/config/setting";
import { Modal, message } from "ant-design-vue";

// 设置统一的url
axios.defaults.baseURL = import.meta.env.VITE_API_BASE_URL;

/* 请求拦截器 */
axios.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    // 添加token到header
    const token = setting.takeToken();
    if (token) {
      config.headers[setting.tokenHeaderName] = token;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

/* 响应拦截器 */
axios.interceptors.response.use(
  (res: AxiosResponse) => {
    // 登录过期处理
    // if (res.data.code === 401) {
    //   if (res.config.url === setting.menuUrl) {
    //     goLogin();
    //   } else {
    //     Modal.destroyAll();
    //     Modal.info({
    //       title: "系统提示",
    //       content: "登录状态已过期, 请退出重新登录!",
    //       okText: "重新登录",
    //       onOk: () => {
    //         goLogin(true);
    //       },
    //     });
    //   }
    //   return Promise.reject(new Error(res.data.msg));
    // }
    // token自动续期
    const access_token = res.headers[setting.tokenHeaderName];
    if (access_token) {
      // setting.cacheToken(access_token);
    }
    return res;
  },
  (error) => {
    message.error("无法连接到服务器，请检查网络或稍后重试", 5);
    return Promise.reject(error);
  },
);

/**
 * 跳转到登录页面
 */
function goLogin(reload?: boolean) {
  // store.dispatch("user/removeToken").then(() => {
  //   if (reload) {
  //     location.replace("/login"); // 这样跳转避免再次登录重复注册动态路由
  //   } else {
  //     const path = router.currentRoute.path;
  //     return router.push({
  //       path: "/login",
  //       query: path && path !== "/" ? { form: path } : null,
  //     });
  //   }
  // });
}

export default axios;
