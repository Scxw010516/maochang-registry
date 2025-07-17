<template>
  <a-layout class="full-height-row">
    <!-- 侧边导航 -->
    <a-layout-sider width="230px">
      <!-- admin -->
      <div
        style="
          margin: 25px 40px 44px 25px;
          width: 165px;
          display: inline-flex;
          justify-content: space-between;
        "
      >
        <div
          style="
            width: 44px;
            height: 44px;
            background: #ffffff;
            border-radius: 9.42857px;
            display: flex;
            align-items: center;
            justify-content: center;
          "
        >
          <svg
            width="30"
            height="30"
            viewBox="0 0 30 30"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M14.8374 15.9658C10.8249 15.9658 7.56055 12.7017 7.56055 8.68945C7.56055 4.67697 10.8249 1.4126 14.8374 1.4126C18.8499 1.4126 22.1143 4.67672 22.1143 8.68945C22.1143 12.7014 18.8499 15.9658 14.8374 15.9658ZM14.8374 2.98367C11.6913 2.98367 9.13161 5.54333 9.13161 8.68945C9.13161 11.8356 11.6913 14.3947 14.8374 14.3947C17.9838 14.3947 20.5432 11.8356 20.5432 8.68945C20.5432 5.54333 17.9838 2.98367 14.8374 2.98367Z"
              fill="#666666"
            />
            fill="#666666" />
            <path
              d="M15.0769 18.0161C8.14625 18.0161 2.50781 22.8468 2.50781 28.7846H3.29335C3.29335 23.2709 8.56907 18.8014 15.0769 18.8014C21.5846 18.8014 26.8604 23.2709 26.8604 28.7846H27.4172H27.6459C27.6462 22.8468 22.0072 18.0161 15.0769 18.0161Z"
              fill="#666666"
            />
            fill="#666666" />
            <path
              d="M15.0765 19.5866C21.141 19.5866 26.0745 23.7123 26.0745 28.784H26.86C26.86 23.2703 21.5843 18.8008 15.0765 18.8008C8.5687 18.8008 3.29297 23.2705 3.29297 28.7842H4.0785C4.0785 23.7126 9.01198 19.5866 15.0765 19.5866Z"
              fill="#666666"
            />
            fill="#666666" />
          </svg>
        </div>

        <span
          style="
            height: 44px;
            font-weight: 700;
            font-size: 36px;
            color: #ffffff;
            align-content: center;
          "
          >admin</span
        >
      </div>
      <!-- 目录 -->
      <a-menu
        mode="inline"
        theme="dark"
        v-model:selectedKeys="selectedMenuItem"
        :selectable="state.allowMenuSwitch === 'allow'"
      >
        <a-menu-item v-for="item in menuItems" :key="item.key" height="60px">
          <template #icon>
            <svg
              v-if="selectedMenuItem.includes(item.key)"
              width="20"
              height="20"
              viewBox="0 0 20 20"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M0.238281 5.88965V3.46582C0.238281 2.40332 0.50944 1.60645 1.05176 1.0752C1.59408 0.538411 2.39925 0.27002 3.46729 0.27002H5.83301V1.73926H3.50049C2.91943 1.73926 2.47396 1.89144 2.16406 2.1958C1.8597 2.50016 1.70752 2.9484 1.70752 3.54053V5.88965H0.238281ZM7.15283 1.73926V0.27002H12.8306V1.73926H7.15283ZM18.2842 5.88965V3.54053C18.2842 2.9484 18.1265 2.50016 17.811 2.1958C17.5011 1.89144 17.0612 1.73926 16.4912 1.73926H14.1587V0.27002H16.5161C17.5897 0.27002 18.3976 0.538411 18.9399 1.0752C19.4823 1.61198 19.7534 2.40885 19.7534 3.46582V5.88965H18.2842ZM18.2842 12.8291V7.21777H19.7534V12.8291H18.2842ZM14.1587 19.7769V18.3076H16.4912C17.0612 18.3076 17.5011 18.1554 17.811 17.8511C18.1265 17.5467 18.2842 17.0985 18.2842 16.5063V14.1572H19.7534V16.5811C19.7534 17.638 19.4823 18.4349 18.9399 18.9717C18.3976 19.5085 17.5897 19.7769 16.5161 19.7769H14.1587ZM7.15283 19.7769V18.3076H12.8306V19.7769H7.15283ZM3.46729 19.7769C2.39925 19.7769 1.59408 19.5085 1.05176 18.9717C0.50944 18.4404 0.238281 17.6436 0.238281 16.5811V14.1572H1.70752V16.5063C1.70752 17.0985 1.8597 17.5467 2.16406 17.8511C2.47396 18.1554 2.91943 18.3076 3.50049 18.3076H5.83301V19.7769H3.46729ZM0.238281 12.8291V7.21777H1.70752V12.8291H0.238281Z"
                fill="black"
              />
              fill="black" />
            </svg>
            <svg
              v-else
              width="20"
              height="20"
              viewBox="0 0 20 20"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M0.238281 5.88965H1.70752V3.54053C1.70752 2.9484 1.8597 2.50016 2.16406 2.1958C2.47396 1.89144 2.91943 1.73926 3.50049 1.73926H5.83301V0.27002H3.46729C2.39925 0.27002 1.59408 0.538411 1.05176 1.0752C0.50944 1.60645 0.238281 2.40332 0.238281 3.46582V5.88965ZM7.15283 1.73926H12.8306V0.27002H7.15283V1.73926ZM18.2842 5.88965H19.7534V3.46582C19.7534 2.40885 19.4823 1.61198 18.9399 1.0752C18.3976 0.538411 17.5897 0.27002 16.5161 0.27002H14.1587V1.73926H16.4912C17.0612 1.73926 17.5011 1.89144 17.811 2.1958C18.1265 2.50016 18.2842 2.9484 18.2842 3.54053V5.88965ZM18.2842 12.8291H19.7534V7.21777H18.2842V12.8291ZM14.1587 19.7769H16.5161C17.5897 19.7769 18.3976 19.5085 18.9399 18.9717C19.4823 18.4349 19.7534 17.638 19.7534 16.5811V14.1572H18.2842V16.5063C18.2842 17.0985 18.1265 17.5467 17.811 17.8511C17.5011 18.1554 17.0612 18.3076 16.4912 18.3076H14.1587V19.7769ZM7.15283 19.7769H12.8306V18.3076H7.15283V19.7769ZM3.46729 19.7769H5.83301V18.3076H3.50049C2.91943 18.3076 2.47396 18.1554 2.16406 17.8511C1.8597 17.5467 1.70752 17.0985 1.70752 16.5063V14.1572H0.238281V16.5811C0.238281 17.6436 0.50944 18.4404 1.05176 18.9717C1.59408 19.5085 2.39925 19.7769 3.46729 19.7769ZM0.238281 12.8291H1.70752V7.21777H0.238281V12.8291Z"
                fill="white"
              />
              fill="white" />
            </svg>
          </template>
          <span>
            <div
              v-show="selectedMenuItem.includes(item.key)"
              style="color: #000"
            >
              {{ item.label }}
            </div>
            <div v-show="!selectedMenuItem.includes(item.key)">
              {{ item.label }}
            </div>
          </span>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <!-- 镜架录入 -->
    <a-layout
      class="full-height-row"
      v-if="Array.isArray(selectedMenuItem) && selectedMenuItem.includes('1')"
    >
      <a-layout-content>
        <scanPage
          :goToManage="
            () => {
              selectedMenuItem = ['3'];
            }
          "
        />
      </a-layout-content>
    </a-layout>
    <!-- 镜框验证 -->
    <a-layout
      class="full-height-row"
      v-if="Array.isArray(selectedMenuItem) && selectedMenuItem.includes('2')"
    >
      <a-layout-content>
        <validatePage
          :goToScan="
            () => {
              selectedMenuItem = ['1'];
            }
          "
        />
      </a-layout-content>
    </a-layout>
    <!-- 镜框落库 -->
    <a-layout
      class="full-height-row"
      v-if="Array.isArray(selectedMenuItem) && selectedMenuItem.includes('3')"
    >
      <a-layout-content>
        <ManagePage
          :goToScan="
            () => {
              selectedMenuItem = ['1'];
            }
          "
        />
      </a-layout-content>
    </a-layout>
    <!-- 账号中心 -->
    <a-layout
      class="full-height-row"
      v-if="Array.isArray(selectedMenuItem) && selectedMenuItem.includes('4')"
    >
      <a-layout-content>
        <a-button @click="onClickLogout">退出登录</a-button>
        <acount />
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script lang="ts" setup>
//#####################################第三方库及定义类初始化#####################################
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useStateStore } from "@/stores/store";
import validatePage from "./validate.vue";
import ManagePage from "./manage.vue";
import ScanPage from "./scan.vue";
import acount from "./acount.vue";

//#########################################参数初始化###########################################
const router = useRouter();
const state = useStateStore();
// 侧边导航栏菜单
const menuItems = ref([
  { key: "1", label: "镜架采集", title: "镜架采集" },
  { key: "2", label: "镜架验证", title: "镜架验证" },
  { key: "3", label: "镜框落库", title: "镜框落库" },
  { key: "4", label: "账号中心", title: "账号中心" },
]);

const selectedMenuItem = ref<string[]>(["1"]); // 选中的菜单项

// ###########################################点击事件定义##############################################
// 退出登录按钮点击事件
const onClickLogout = () => {
  router.push("/");
};
</script>

<style scoped>
.full-height-row {
  height: 100vh;
  background-color: #8675ff;
}
.full-height-row {
  height: 100vh;
  background-color: #8675ff;
}

:global(.ant-layout-sider-children) {
  background-color: #8675ff;
}

:global(.ant-menu) {
  background-color: #8675ff;
}
:global(.ant-menu-item) {
  height: 60px !important;
  font-weight: 400;
  font-size: 20px;
  margin-left: 25px !important;
  border-radius: 11px 0 0 11px !important;
  width: calc(100% - 25px) !important;
}

:global(.ant-menu-item-selected) {
  background-color: #ffffff !important;
}
</style>
