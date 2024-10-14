import { InjectionKey } from "vue";
import { createStore, Store, useStore as baseUseStore } from "vuex";
import getters from "./store/getters";
import user from "./store/modules/user";
// import theme from "./store/modules/theme";
import type { SelectProps } from "ant-design-vue"; // 引入下拉框SelectProps组件
import {
  Camera, //摄像头参数和对象字典
} from "@/interfaces/camera";

interface Option {
  value: string;
}
export interface State {
  // 登陆用户名
  username: string;
  // 登录标识
  hasLoggedIn: boolean;
  // 登录仓库
  warehouse: number | null;
  // 检索镜架信息方式
  skuormodeltype: number | null;
  //输入sku时，sku已存在
  searchSku: string;
  //基础参数 下拉列表
  cameraState: {
    cameraInitState: boolean; // 摄像头初始化状态
    cameraList: Camera[]; // 摄像头列表
  };
  options: {
    brand_options: Option[];
    model_type_options: Option[];
    skuormodeltype_options: SelectProps["options"];
    warehouse_options: SelectProps["options"];
    material_options: SelectProps["options"];
    color_options: SelectProps["options"];
    shape_options: SelectProps["options"];
    style_options: SelectProps["options"];
  };
}
export const key: InjectionKey<Store<State>> = Symbol();

// 创建store
export const store = createStore<State>({
  state: {
    username: "",
    hasLoggedIn: false,
    warehouse: 1,
    skuormodeltype: 1,
    searchSku: "",
    cameraState: {
      cameraInitState: false, // 摄像头初始化状态
      cameraList: [], // 摄像头列表
    },
    options: {
      brand_options: [{ value: "" }],
      model_type_options: [
        {
          value: "",
        },
      ],
      material_options: [
        {
          value: null,
          label: "",
        },
      ],
      skuormodeltype_options: [
        {
          value: 1,
          label: "型号",
        },
        {
          value: 2,
          label: "SKU",
        },
      ],
      warehouse_options: [
        {
          value: null,
          label: "",
        },
      ],
      color_options: [
        {
          value: null,
          label: "",
        },
      ],
      shape_options: [
        {
          value: null,
          label: "",
        },
      ],
      style_options: [
        {
          value: null,
          label: "",
        },
      ],
    },
  },
  modules: {
    user,
    // theme,
  },
  getters,
});

export function useStore() {
  return baseUseStore(key);
}
