/**
 * 路由配置
 */
import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import LoginView from "@/views/eyeglass/login.vue";
import MainView from "@/views/eyeglass/main.vue";
import NotFoundView from "@/views/exception/404.vue";
import NProgress from "nprogress";
import "nprogress/nprogress.css";

// 静态路由
const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    redirect: "/login",
  },
  {
    name: "login",
    path: "/login",
    component: LoginView,
    meta: {
      title: "登录",
    },
  },
  {
    name: "main",
    path: "/main",
    component: MainView,
    meta: {
      title: "镜架扫描",
    },
  },
  {
    path: "/:pathMatch(.*)*",
    component: NotFoundView,
  },
];

const router = createRouter({
  routes,
  history: createWebHistory(),
});

// 路由守卫
router.beforeEach((to, from, next) => {
  // 开启进度条
  NProgress.start();
  // 更新标题
  updateTitle(to);
  // 继续路由
  next();
});

router.afterEach(() => {
  // 关闭进度条
  setTimeout(() => {
    NProgress.done(true);
  }, 300);
});

export default router;

/**
 * 更新浏览器标题
 * @param route 路由
 */
function updateTitle(route: any) {
  if (!route.path.startsWith("/redirect/")) {
    let names: string[] = [];
    if (route && route.meta && route.meta.title) {
      names.push(route.meta.title);
    }
    const appName = import.meta.env.VITE_NAME;
    if (appName) {
      names.push(appName);
    }
    document.title = names.join(" - ");
  }
}
