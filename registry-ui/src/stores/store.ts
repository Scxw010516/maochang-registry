import { defineStore } from "pinia";
import type { SelectProps } from "ant-design-vue"; // 引入下拉框SelectProps组件
import {
  Camera, //摄像头参数和对象字典
} from "@/interfaces/camera";

// 选项接口
interface Option {
  value: string;
}
// 选项状态管理
export const useOptionStore = defineStore("option", {
  state: () => {
    return {
      brand_options: [{ value: "" }] as Option[],
      model_type_options: [
        {
          value: "",
        },
      ] as Option[],
      material_options: [
        {
          value: null,
          label: "",
        },
      ] as SelectProps["options"],
      skuormodeltype_options: [
        {
          value: 1,
          label: "型号",
        },
        {
          value: 2,
          label: "SKU",
        },
      ] as SelectProps["options"],
      warehouse_options: [
        {
          value: null,
          label: "",
        },
      ] as SelectProps["options"],
      color_options: [
        {
          value: null,
          label: "",
        },
      ] as SelectProps["options"],
      shape_options: [
        {
          value: null,
          label: "",
        },
      ] as SelectProps["options"],
      style_options: [
        {
          value: null,
          label: "",
        },
      ] as SelectProps["options"],
    };
  },
});
// 用户状态管理
export const useUserStore = defineStore("user", {
  state: () => {
    return {
      // 用户名
      username: "" as string,
      hasLoggedIn: false as boolean,
      warehouse: 1 as number,
    };
  },
});

export const useCameraStore = defineStore("camera", {
  state: () => {
    return {
      cameraState: {
        cameraInitState: false, // 摄像头初始化状态
        cameraList: [] as Camera[], // 摄像头列表
      },
    };
  },
});

// 应用状态管理
export const useStateStore = defineStore("state", {
  state: () => {
    return {
      // 是否允许切换菜单
      allowMenuSwitch: "allow" as "allow" | "scaning",
      //输入sku时，sku已存在
      searchSku: "" as string,
    };
  },
});
