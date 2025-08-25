import { defineStore } from "pinia";
import {
  Camera, //摄像头参数和对象字典
} from "@/interfaces/camera";

// 摄像头管理store
export const useCameraStore = defineStore("camera", {
  state: () => {
    return {
      // 摄像头列表
      cameraState: {
        cameraInitState: false as boolean, // 摄像头初始化状态
        cameraList: [] as Camera[], // 摄像头列表
      },
    };
  },
  getters: {
    // 获取摄像头数量
    cameraNum: (state) => {
      return state.cameraState.cameraList.length;
    },
  },
  actions: {
    /**
     * 初始化摄像头设备的初始化状态
     **/
    initCameraDeviceState() {
      // 重置摄像头设备初始化状态
      this.cameraState.cameraInitState = false;
      // 清空摄像头设备列表
      this.cameraState.cameraList = [];
    },
  },
});
