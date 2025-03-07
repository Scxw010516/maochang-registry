import axios from "@/config/axios-config";
import { message } from "ant-design-vue";
import { useOptionStore } from "@/stores/store";

const options = useOptionStore();
// 功能函数：初始化表单填写辅助信息
export const initFormOptions = () => {
  // 获取所有镜架品牌
  getAllBrands();
  // 获取所有镜架型号
  getAllModeltypes();
  // 获取所有镜架材质
  getAllMaterials();
  // 获取所有镜架颜色
  getAllColors();
  // 获取所有镜架形状
  getAllShapes();
  // 获取所有透明度
  getAllIstransparent();
  // 获取所有镜框类型
  getAllFrametypes();
  // 获取所有镜架风格
  // getAllStyles();
};

// 功能函数：获取所有镜架品牌
export const getAllBrands = async () => {
  await axios
    .get("/glassmanagement/api/get-all-brands")
    .then((response) => {
      // 判断返回的code值，若为-1则提示无镜架信息
      if (response.data.code === -1) {
        message.warning("无镜架品牌信息");
        return;
      } else {
        // 将返回的品牌列表赋值给brand_options
        options.brand_options = response.data.data.map((item: string) => ({
          value: item,
        }));
      }
    })
    .catch((error) => {
      console.log(error);
    });
};

// 功能函数：获取所有镜架型号
export const getAllModeltypes = async () => {
  await axios
    .get("/glassmanagement/api/get-all-model-types")
    .then((response) => {
      // 判断返回的code值，若为-1则提示无镜架信息
      if (response.data.code === -1) {
        message.warning("无镜架型号信息");
        return;
      } else {
        // 将返回的型号列表赋值给store中的brand_options
        options.model_type_options = response.data.data.map((item: string) => ({
          value: item,
        }));
      }
    })
    .catch((error) => {
      console.log(error);
    });
};

// 功能函数：获取所有镜架材质
export const getAllMaterials = async () => {
  await axios
    .get("/glassmanagement/api/get-all-materials")
    .then((response) => {
      // 判断返回的code值，若为-1则提示无镜架信息
      if (response.data.code === -1) {
        message.warning("无镜架材质信息");
        return;
      } else {
        // 将返回的材质列表赋值给store中的material_options
        options.material_options = response.data.data.map(
          (item: { id: number; material: string }) => ({
            value: item.id,
            label: item.material,
          }),
        );
      }
    })
    .catch((error) => {
      console.log(error);
    });
};

// 功能函数：获取所有镜架颜色
export const getAllColors = async () => {
  await axios
    .get("/glassmanagement/api/get-all-colors")
    .then((response) => {
      // 判断返回的code值，若为-1则提示无镜架信息
      if (response.data.code === -1) {
        message.warning("无镜架颜色信息");
        return;
      } else {
        // 将返回的颜色列表赋值给store中的color_options
        options.color_options = response.data.data.map(
          (item: { id: number; color: string }) => ({
            value: item.id,
            label: item.color,
          }),
        );
      }
    })
    .catch((error) => {
      console.log(error);
    });
};

// 功能函数：获取所有镜架形状
export const getAllShapes = async () => {
  await axios
    .get("/glassmanagement/api/get-all-shapes")
    .then((response) => {
      // 判断返回的code值，若为-1则提示无镜架信息
      if (response.data.code === -1) {
        message.warning("无镜架形状信息");
        return;
      } else {
        // 将返回的形状列表赋值给store中的shape_options
        options.shape_options = response.data.data.map(
          (item: { id: number; shape: string }) => ({
            value: item.id,
            label: item.shape,
          }),
        );
      }
    })
    .catch((error) => {
      console.log(error);
    });
};

// 功能函数：获取所有镜架透明度
export const getAllIstransparent = async () => {
  await axios
    .get("/glassmanagement/api/get-all-is-transparent")
    .then((response) => {
      // 判断返回的code值，若为-1则提示无镜架信息
      if (response.data.code === -1) {
        message.warning("无镜架透明度信息");
        return;
      } else {
        // 将返回的形状列表赋值给store中的is_transparent_options
        options.is_transparent_options = response.data.data.map(
          (item: { id: number; is_transparent: string }) => ({
            value: item.id,
            label: item.is_transparent,
          }),
        );
      }
    })
    .catch((error) => {
      console.log(error);
    });
};

// 功能函数：获取所有镜框类型
export const getAllFrametypes = async () => {
  await axios
    .get("/glassmanagement/api/get-all-frame-types")
    .then((response) => {
      // 判断返回的code值，若为-1则提示无镜架信息
      if (response.data.code === -1) {
        message.warning("无镜框类型信息");
        return;
      } else {
        // 将返回的形状列表赋值给store中的frame_type_options
        options.frame_type_options = response.data.data.map(
          (item: { id: number; frame_type: string }) => ({
            value: item.id,
            label: item.frame_type,
          }),
        );
      }
    })
    .catch((error) => {
      console.log(error);
    });
};

// 功能函数：获取所有风格
export const getAllStyles = async () => {
  await axios
    .get("/glassmanagement/api/get-all-styles")
    .then((response) => {
      // 判断返回的code值，若为-1则提示无镜架信息
      if (response.data.code === -1) {
        message.warning("无镜架风格信息");
        return;
      } else {
        // 将返回的材质列表赋值给store中的style_options
        options.style_options = response.data.data.map(
          (item: { id: number; style: string }) => ({
            value: item.id,
            label: item.style,
          }),
        );
      }
    })
    .catch((error) => {
      console.log(error);
    });
};

// 功能函数：获取所有仓库
export const getAllWarehouses = async () => {
  await axios
    .get("/warehouse/api/get-all-warehouses")
    .then((response) => {
      // 判断返回的code值，若为-1则提示无镜架信息
      if (response.data.code === -1) {
        message.warning("无仓库信息");
        return;
      } else {
        // 将返回的仓库列表赋值给store中的warehouse_options
        options.warehouse_options = response.data.data.map(
          (item: { id: number; warehouse: string }) => ({
            value: item.id,
            label: item.warehouse,
          }),
        );
      }
    })
    .catch((error) => {
      console.log(error);
    });
};
