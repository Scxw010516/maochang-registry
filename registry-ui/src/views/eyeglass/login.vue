<template>
  <a-row
    v-if="!store.state.hasLoggedIn"
    class="full-height-row"
    type="flex"
    align="middle"
    justify="center"
  >
    <!-- 登录 输入仓库地址 -->
    <a-form v-if="inputAddress" class="login-form-card">
      <LeftOutlined @click="inputAddress = false" />
      <a-select
        v-model:value="store.state.warehouse"
        placeholder="选择仓库地址"
        style="width: 100%"
        show-search
        defaultOpen
        :options="store.state.options.warehouse_options"
        :filter-option="filterOptionbyLabel"
        @select="inputAddress = false"
      ></a-select>
    </a-form>
    <!-- 登录 输入员工号 -->
    <a-form v-else class="login-form-card">
      <img src="@/assets/logo.png" alt="logo" />
      <a-form-item
        name="username"
        style="margin-bottom: 24px; margin-top: 48px"
      >
        <a-input
          class="login-input"
          allow-clear
          size="large"
          v-model:value="store.state.username"
          :placeholder="'请输入员工号'"
        >
        </a-input>
      </a-form-item>
      <a-form-item>
        <a-button
          class="login-button"
          block
          size="large"
          type="primary"
          @click="onClickLogin"
        >
          登录
        </a-button>
      </a-form-item>
      <!-- 展示仓库地址 -->
      <a-form-item name="colllection-address" style="margin-bottom: 24px">
        <a-button
          class="login-address"
          type="link"
          @click="inputAddress = true"
        >
          <svg
            width="27"
            height="27"
            viewBox="0 0 27 27"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M14.4824 5.03652C16.5213 5.03652 18.2428 6.78086 18.2428 8.84766C18.2428 10.2898 17.377 12.3186 15.8129 14.5504C15.3432 15.2131 14.8861 15.8123 14.49 16.2998C14.0812 15.8072 13.609 15.2055 13.152 14.5504C11.5854 12.3465 10.7221 10.3229 10.7221 8.84766C10.7221 6.74531 12.408 5.03652 14.4824 5.03652ZM14.4824 3.38867C11.4711 3.38867 9.07422 5.85664 9.07422 8.84766C9.07422 11.1404 10.5494 13.7328 11.8088 15.5025C12.7711 16.8838 13.7943 18.0314 14.2564 18.5443C14.3174 18.6053 14.3682 18.6561 14.4824 18.6561C14.5434 18.6561 14.6576 18.5951 14.7084 18.5443C15.2213 18.0314 16.1836 16.8762 17.1561 15.5025C18.4053 13.7201 19.8906 11.1404 19.8906 8.84766C19.8881 5.85664 17.4404 3.38867 14.4824 3.38867Z"
              fill="#8675FF"
            />
            <path
              d="M14.4822 7.52256C15.1652 7.52256 15.7213 8.08877 15.7213 8.78447C15.7213 9.48018 15.1652 10.0464 14.4822 10.0464C13.7992 10.0464 13.2432 9.48018 13.2432 8.78447C13.2432 8.08877 13.7967 7.52256 14.4822 7.52256ZM14.4822 6.28857C13.1137 6.28857 12.0066 7.41084 12.0066 8.78701C12.0066 10.1632 13.1137 11.2854 14.4822 11.2854C15.8508 11.2854 16.9578 10.1632 16.9578 8.78701C16.9553 7.41084 15.8482 6.28857 14.4822 6.28857ZM24.8543 22.6274H4.21172C3.91211 22.6274 3.63535 22.4649 3.49062 22.2009C3.3459 21.9394 3.35605 21.6169 3.51601 21.3655L7.49219 15.0661C7.64199 14.8274 7.90605 14.6827 8.18535 14.6827L11.8086 14.6751H11.8111C12.2656 14.6751 12.6338 15.0433 12.6338 15.4952C12.6338 15.9497 12.2682 16.3179 11.8137 16.3204L8.64492 16.3255L5.70215 20.9821H23.4146L20.6648 16.3052L17.1533 16.3128H17.1508C16.6963 16.3128 16.3281 15.9446 16.3281 15.4927C16.3281 15.0382 16.6937 14.67 17.1482 14.6675L21.1295 14.6599H21.132C21.424 14.6599 21.6932 14.8147 21.8404 15.0661L25.5602 21.3909C25.71 21.6448 25.7125 21.9597 25.5652 22.2161C25.418 22.4726 25.1514 22.6274 24.8543 22.6274Z"
              fill="#8675FF"
            />
          </svg>
          <span class="login-address-text">{{
            store.state.options.warehouse_options?.find(
              (option) => option.value === store.state.warehouse,
            )?.label
          }}</span>
        </a-button>
      </a-form-item>
    </a-form>
  </a-row>
</template>

<script setup lang="ts">
//##########################################第三方库及定义类初始化######################################
import { ref, onMounted } from "vue";
import { useStore } from "../../store";
import { useRouter } from "vue-router";
import { LeftOutlined } from "@ant-design/icons-vue";
import { message } from "ant-design-vue";
import { getAllWarehouses } from "./utils";
//#############################################参数初始化##############################################
const store = useStore();
const router = useRouter();
const inputAddress = ref<boolean>(false);

// select和autocompe下拉框选项接口定义
interface Option {
  value: string;
  label: string;
}
// ###########################################生命周期函数#############################################
// 生命周期钩子：组件挂载完成后执行
onMounted(() => {
  // 初始化仓库选项表单
  getAllWarehouses();
});

//###########################################功能函数定义###############################################
// 功能函数：selct和auto-complete的输入框和option不区分大小写
const filterOptionbyLabel = (input: string, option: Option) => {
  // 判断option中是否为空
  if (!option.label) {
    return false;
  } else {
    return option.label.toUpperCase().indexOf(input.toUpperCase()) >= 0;
  }
};

//###########################################点击事件定义###############################################
// 登录按钮点击事件
const onClickLogin = () => {
  // 判断仓库地址是否为空
  if (!store.state.warehouse) {
    message.warning("请选择仓库地址");
    return;
  }
  // 登录成功后，将hasLoggedIn置为true
  store.state.hasLoggedIn = true;
  router.push("/main");
};
</script>

<style scoped>
.full-height-row {
  height: 100vh;
  background-color: #8675ff;
}

.login-form-card {
  height: 582px;
  width: 520px;
  background-color: #ffffff;
  padding-top: 120px;
  padding-bottom: 120px;
  padding-left: 60px;
  padding-right: 60px;
  border-radius: 20px;
}

.login-input {
  border-radius: 30px;
  height: 60px;
  border-color: #8675ff;
  font-size: 20px;
  padding: 6.5px 28px;
}

.login-button {
  border-radius: 30px;
  height: 60px;
  color: white;
  background-color: #8675ff;
  border: none;
  font-size: 20px;
}

.login-address {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-address-text {
  height: 24px;
  font-weight: 700;
  font-size: 16px;
  color: #8675ff;
}
</style>
