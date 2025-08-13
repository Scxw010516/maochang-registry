<template>
  <div class="full-height-row">
    <p class="page-title">
      <a-button
        type="default"
        size="large"
        @click="props.onClickBack"
        style="height: 100%; margin-right: 30px"
        :icon="h(LeftOutlined)"
      />
      {{ eyeglass_info.sku }} - {{ eyeglass_info.model_type }}
    </p>
    <a-row class="full-height align-center">
      <!-- 试戴图片 -->
      <a-col span="12" class="tryon-image-col">
        <a-carousel>
          <div v-for="(item, index) in tryon_images" :key="index + 1">
            <p class="image-title">
              {{ item.face_name }} - {{ getTryOnStateLabel(item.tryon_state) }}
            </p>
            <img :src="item.tryon_image" class="eyeglass-frame-img" />
          </div>
        </a-carousel>
      </a-col>
      <!-- 镜架图片 操作按钮   -->
      <a-col span="12">
        <a-carousel>
          <a-col>
            <p class="image-title">
              原始镜架图：
              {{ eyeglass_info.is_tryon_beautify_origin ? "启用" : "未启用" }}
            </p>
            <img
              :src="eyeglass_frame_image.frontview_beautify"
              class="eyeglass-frame-img"
            />
            <img
              :src="eyeglass_frame_image.sideview_beautify"
              class="eyeglass-frame-img"
            />
          </a-col>
          <a-col
            v-if="
              processed_beautify_images.frontview_beautify_processed ||
              processed_beautify_images.sideview_beautify_processed
            "
          >
            <p class="image-title">
              处理后镜架图：
              {{ eyeglass_info.is_tryon_beautify_origin ? "未启用" : "启用" }}
            </p>
            <img
              v-if="processed_beautify_images.frontview_beautify_processed"
              :src="processed_beautify_images.frontview_beautify_processed"
              class="eyeglass-frame-img"
            />
            <img
              v-if="processed_beautify_images.sideview_beautify_processed"
              :src="processed_beautify_images.sideview_beautify_processed"
              class="eyeglass-frame-img"
            />
          </a-col>
        </a-carousel>
      </a-col>
    </a-row>
    <!-- 操作按钮 -->
    <a-row justify="space-around" class="operation-row">
      <a-col>
        <a-button
          type="primary"
          class="operation-button"
          @click="onClickDownload"
        >
          下载原始镜架图
        </a-button>
      </a-col>
      <a-col>
        <a-button
          type="primary"
          class="operation-button"
          @click="onClickUpload"
        >
          上传美化图
        </a-button>
      </a-col>
      <!-- <a-col>
        <a-button
          type="primary"
          class="operation-button"
          @click="onClickUpload('side')"
        >
          上传镜架侧视图
        </a-button>
      </a-col> -->
      <a-col>
        <a-button
          type="primary"
          class="operation-button"
          @click="onClickAnnotateLegs"
        >
          镜腿标注
        </a-button>
      </a-col>
      <a-col>
        <!-- 复原 -->
        <a-dropdown overlayClassName="operation-dropdown">
          <template #overlay>
            <a-menu @click="onClickReset">
              <a-menu-item key="1"> 复原镜腿标注 </a-menu-item>
              <a-menu-item key="2"> 复原镜架美化图 </a-menu-item>
              <a-menu-item key="3"> 全部复原 </a-menu-item>
            </a-menu>
          </template>
          <a-button type="primary" class="operation-button"> 复原 </a-button>
        </a-dropdown>
      </a-col>
      <a-col>
        <a-button
          type="primary"
          class="operation-button"
          @click="onClickIsActive"
        >
          {{ eyeglass_info.is_active ? "禁用" : "启用" }}
        </a-button>
      </a-col>
    </a-row>
  </div>
  <!-- 上传图片MODAL -->
  <a-modal
    v-model:open="beautify_modal.visible"
    title="上传美化图"
    width="1050px"
    :closable="false"
    centered
    :maskClosable="true"
    okText="上传美化图并生成试戴任务"
    cancelText="取消"
    @ok="onClickUploadImage"
    :confirm-loading="beautify_modal.loading"
  >
    <a-row>
      <!-- <p class="page-title" style="padding: 20px">镜架美化图</p> -->
      <a-col :span="24">
        <a-button
          @click="onClickChoseBeautifyImage('front')"
          style="margin-bottom: 10px"
          size="large"
        >
          选择正视图
        </a-button>
        <div v-if="beautify_modal.tempUploadFiles.front.file">
          <img
            :src="beautify_modal.tempUploadFiles.front.url"
            style="width: 100%; max-height: 400px; object-fit: contain"
          />
        </div>
      </a-col>
      <a-col :span="24">
        <a-button
          @click="onClickChoseBeautifyImage('side')"
          style="margin-bottom: 10px"
          size="large"
        >
          选择侧视图
        </a-button>
        <div v-if="beautify_modal.tempUploadFiles.side.file">
          <img
            :src="beautify_modal.tempUploadFiles.side.url"
            style="width: 100%; max-height: 400px; object-fit: contain"
          />
        </div>
      </a-col>
    </a-row>
  </a-modal>
  <!-- 镜腿标注MODAL -->
  <a-modal
    v-model:open="annotate_modal.show_annotate_modal"
    width="1050px"
    :footer="null"
  >
    <a-space class="page-title">
      镜腿标注步骤：{{ annotation_steps_options[annotate_modal.annotate_step] }}
      <a-button size="large" @click="onClickAnnotatePrev"> 上一步 </a-button>
      <a-button size="large" @click="onClickAnnotateNext"> 下一步 </a-button>

      <a-button type="primary" size="large" @click="onClickAnnotateConfirm">
        确定并生成试戴任务
      </a-button>
    </a-space>
    <div style="position: relative">
      <div
        v-for="(item, index) in annotation_steps_options.length - 1"
        :key="index"
        class="annotation"
        :data-annotation="index"
      ></div>
      <img
        :src="eyeglass_frame_image.sideview_seg"
        alt=""
        class="modal-image"
        @click="onClickImageToAnnotate"
      />
    </div>
  </a-modal>
</template>
<script lang="ts" setup>
import axios from "axios";
import { reactive, onMounted, ref, h } from "vue";
import { message, Modal, Button, Space, Row, Col } from "ant-design-vue";
import type { MenuProps } from "ant-design-vue";
import { set } from "nprogress";
import { siderProps } from "ant-design-vue/es/layout/Sider";
import { LeftOutlined } from "@ant-design/icons-vue";

interface TryonPageProps {
  id: number; // 试戴的ID
  onClickBack: () => void; // 功能函数：返回
  getTryOnStateLabel: (state: number) => string;
  getIsActiveLabelFromId: (id: number) => string;
  changeIsActive: (
    id: number,
    sku: string,
    is_active: boolean,
    try_on_state: number,
    refresh_func: () => void,
  ) => void; // 功能函数：点击试戴状态按钮
}
const props = withDefaults(defineProps<TryonPageProps>(), {
  onClickBack: () => {},
  id: 0,
});
// 镜架基本信息
const eyeglass_info = ref({
  id: props.id,
  sku: "",
  model: "",
  is_tryon_leg_auto: true, // 是否自动试戴镜腿
  is_tryon_beautify_origin: true, // 是否使用原始美化图像
  try_on_state: 0,
  is_active: true, // 是否启用
  model_type: "",
});
// 原始镜架图
const eyeglass_frame_image = reactive({
  frontview_beautify: "",
  sideview_beautify: "",
  sideview_seg: "",
  contour_points: [],
});
// 处理后镜架图
const processed_beautify_images = reactive({
  frontview_beautify_processed: "",
  sideview_beautify_processed: "",
});
// 上传镜架美化图modal
const beautify_modal = reactive({
  visible: false,
  loading: false,
  tempUploadFiles: {
    front: {
      file: null as File | null,
      url: "",
    },
    side: {
      file: null as File | null,
      url: "",
    },
  },
});
// 试戴图片
interface TryOnImage {
  face_name: string;
  tryon_image: string;
  tryon_state: number; // 试戴状态
}
const tryon_images = reactive<TryOnImage[]>([]);
const annotation_steps_options = ["左上", "右上", "左下", "右下", "完成"];
// 镜腿标注modal
const annotate_modal = ref({
  show_annotate_modal: false,
  annotate_step: 0, // 镜腿标注步骤 0 左上 1 右上 2 左下 3 右下 4 完成
  annotation_result: [] as Array<{ x: number; y: number }>,
});
const reset_confirm_loading = ref(false);
// ###########################################点击事件###########################################
// 点击上传美化图：打开上传镜架美化图modal
const onClickUpload = () => {
  beautify_modal.visible = true;
};
const onClickChoseBeautifyImage = (type: "front" | "side") => {
  // 打开上传窗口
  const input = document.createElement("input");
  input.type = "file";
  input.accept = "image/*";
  input.onchange = (event: Event) => {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files.length > 0) {
      const file = target.files[0];
      // 保存文件到临时变量
      beautify_modal.tempUploadFiles[type].file = file;
      // 创建预览URL
      const previewUrl = URL.createObjectURL(file);
      // 更新预览图片显示
      if (type === "front") {
        beautify_modal.tempUploadFiles.front.url = previewUrl;
      } else {
        beautify_modal.tempUploadFiles.side.url = previewUrl;
      }
    }
  };
  input.click();
  if (type === "front") {
    console.log("上传镜架正视图");
    // 替换镜架修改后正视图
  } else if (type === "side") {
    // 替换镜架修改后侧视图
    console.log("上传镜架侧视图");
  }
};

// 点击模态框上传美化图:上传处理后图片到服务器并生成试戴任务
const onClickUploadImage = () => {
  beautify_modal.loading = true;
  // 检查两张图片是否都上传了
  if (!beautify_modal.tempUploadFiles.front.file) {
    message.error("请上传正视图");
    return;
  }
  if (!beautify_modal.tempUploadFiles.side.file) {
    message.error("请上传侧视图");
    return;
  }
  // 构建FormData对象
  const formData = new FormData();
  formData.append(
    "frontview_beautify_processed",
    beautify_modal.tempUploadFiles.front.file as File,
  );
  formData.append(
    "sideview_beautify_processed",
    beautify_modal.tempUploadFiles.side.file as File,
  );
  formData.append("id", eyeglass_info.value.id.toString());
  axios
    .post("glassmanagement/api/upload-processed-beautify-image", formData)
    .then((response) => {
      if (response.data.code === 0) {
        message.success(response.data.msg);
        getPageData(); // 刷新页面数据
        beautify_modal.visible = false;
      } else {
        message.error(response.data.msg);
      }
    })
    .catch((error) => {
      console.error("上传失败:", error);
      message.error(error);
    })
    .finally(() => {
      beautify_modal.loading = false;
    });
};
// 点击下载镜架图：下载侧视图和正视图
const onClickDownload = () => {
  // 下载镜架图
  const linkfront = document.createElement("a");
  linkfront.href = eyeglass_frame_image.frontview_beautify;
  document.body.appendChild(linkfront);
  linkfront.click();
  document.body.removeChild(linkfront);
  // 下载侧视图，延迟触发，防止浏览器忽略
  setTimeout(() => {
    const linkside = document.createElement("a");
    linkside.href = eyeglass_frame_image.sideview_beautify;
    document.body.appendChild(linkside);
    linkside.click();
    document.body.removeChild(linkside);
  }, 500); // 延迟500毫秒
};
// 点击镜腿标注：展开标注modal
const onClickAnnotateLegs = () => {
  // 展开标注modal
  annotate_modal.value.show_annotate_modal = true;
  const form = new FormData();
  form.append("id", eyeglass_info.value.id.toString());
  axios.post("glassmanagement/api/get-annotate-leg-data", form).then((res) => {
    // 获取标注数据
    console.log(res.data);
    const data = res.data.data;
    if (!data) {
      message.error(res.data.msg);
      return;
    }
    // 解析返回数据
    eyeglass_frame_image.contour_points = data.contour_points;
    // 获取标注结果
    const annotation_result = data.annotation_result;
    if (annotation_result) {
      annotate_modal.value.annotation_result[0] = {
        x: annotation_result["top_left_point"][0],
        y: annotation_result["top_left_point"][1],
      };
      annotate_modal.value.annotation_result[1] = {
        x: annotation_result["top_right_point"][0],
        y: annotation_result["top_right_point"][1],
      };
      annotate_modal.value.annotation_result[2] = {
        x: annotation_result["bottom_left_point"][0],
        y: annotation_result["bottom_left_point"][1],
      };
      annotate_modal.value.annotation_result[3] = {
        x: annotation_result["bottom_right_point"][0],
        y: annotation_result["bottom_right_point"][1],
      };
      console.log(annotate_modal.value.annotation_result);
      // 将标注数据赋值给标注modal
      for (const [
        index,
        item,
      ] of annotate_modal.value.annotation_result.entries()) {
        setAnnotationDot(item.x, item.y, index);
      }
      annotate_modal.value.annotate_step = 4; // 标注完成
    }
  });
};
// 点击图片位置进行标注：获取点击位置并显示
const onClickImageToAnnotate = (event: MouseEvent) => {
  if (
    annotate_modal.value.annotate_step >=
    annotation_steps_options.length - 1
  ) {
    return;
  }
  // 获取点击位置并显示
  if (event.target) {
    // 获取点击位置
    const img = event.target as HTMLImageElement;
    const rect = img.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    console.log(`点击位置：(${x}, ${y})`);
    // 转化为对于图片的坐标
    let x_real = (x / rect.width) * img.naturalWidth;
    let y_real = (y / rect.height) * img.naturalHeight;
    // 吸附到轮廓上
    ({ x_real, y_real } = findNearestPoint(x_real, y_real));
    annotate_modal.value.annotation_result[annotate_modal.value.annotate_step] =
      {
        x: x_real,
        y: y_real,
      };
    console.log("吸附转化后实际坐标", x_real, y_real);
    // 在图片上显示标注点
    setAnnotationDot(x_real, y_real, annotate_modal.value.annotate_step);
  }
};

// 点击标注下一步
const onClickAnnotateNext = () => {
  if (annotate_modal.value.annotate_step < 4) {
    // 当前标注点取消激活样式
    const annotations = Array.from(document.querySelectorAll(".annotation"));
    annotations.forEach((annotation) => {
      const el = annotation as HTMLElement; // 断言为 HTMLElement
      if (el.dataset.annotation === `${annotate_modal.value.annotate_step}`) {
        el.classList.remove("active");
      }
      if (
        el.dataset.annotation === `${annotate_modal.value.annotate_step + 1}`
      ) {
        el.classList.add("active");
      }
    });
    annotate_modal.value.annotate_step++;
  }
};
// 点击标注上一步
const onClickAnnotatePrev = () => {
  if (annotate_modal.value.annotate_step > 0) {
    const annotations = Array.from(document.querySelectorAll(".annotation"));
    annotations.forEach((annotation) => {
      const el = annotation as HTMLElement; // 断言为 HTMLElement
      if (el.dataset.annotation === `${annotate_modal.value.annotate_step}`) {
        el.classList.remove("active");
      }
      if (
        el.dataset.annotation === `${annotate_modal.value.annotate_step - 1}`
      ) {
        el.classList.add("active");
      }
    });
    annotate_modal.value.annotate_step--;
  } else {
    // 已经是第一步了
    console.warn("已经是第一步，无法返回");
  }
};

// 点击标注确认
const onClickAnnotateConfirm = () => {
  console.log("确认标注结果：", annotate_modal.value.annotation_result);
  // 检查标注结果
  if (
    annotate_modal.value.annotation_result[0] &&
    annotate_modal.value.annotation_result[1] &&
    annotate_modal.value.annotation_result[2] &&
    annotate_modal.value.annotation_result[3]
  ) {
    // 构建表单
    const formData = new FormData();
    formData.append(
      "annotation_result",
      JSON.stringify(annotate_modal.value.annotation_result),
    );
    formData.append("id", eyeglass_info.value.id.toString());
    axios
      .post("/glassmanagement/api/update-annotation-leg", formData)
      .then((response) => {
        console.log(response);
        getPageData(); // 刷新页面数据
        message.success(response.data.msg);
        annotate_modal.value.show_annotate_modal = false; // 关闭标注modal
      });
  } else {
    message.error("请标注完整4个镜腿位置");
  }
};

// 点击复原：展开复原确认modal
const onClickReset: MenuProps["onClick"] = (e) => {
  console.log("click", e.key); // 获取点击的菜单项的 key
  // 在这里添加你想要执行的逻辑，例如根据 key 值进行不同的操作
  switch (e.key) {
    case "1":
      // 处理 "复原镜腿标注" 逻辑
      Modal.confirm({
        title: "确认复原镜腿标注",
        centered: true,
        okText: "确认并生成试戴任务",
        cancelText: "取消",
        onOk: () => {
          onClickResetAndGenerateTryonTask("reset_leg");
        },
        okButtonProps: {
          loading: reset_confirm_loading.value,
        },
      });
      break;
    case "2":
      // 处理 "复原镜架美化图" 逻辑
      Modal.confirm({
        title: "确认复原镜架美化图",
        centered: true,
        okText: "确认并生成试戴任务",
        cancelText: "取消",
        onOk: () => {
          onClickResetAndGenerateTryonTask("reset_beautify_image");
        },
        okButtonProps: {
          loading: reset_confirm_loading.value,
        },
      });
      break;
    default:
      // 处理 "全部复原"
      Modal.confirm({
        title: "确认全部复原",
        centered: true,
        okText: "确认并生成试戴任务",
        cancelText: "取消",
        onOk: () => {
          onClickResetAndGenerateTryonTask("reset_all");
        },
        okButtonProps: {
          loading: reset_confirm_loading.value,
        },
      });
      break;
  }
};

// 点击更新试戴模式并生成试戴任务：更新试戴模式并生成试戴任务
const onClickResetAndGenerateTryonTask = (
  reset_type: "reset_leg" | "reset_beautify_image" | "reset_all",
) => {
  reset_confirm_loading.value = true;
  // 构建表单
  const form = new FormData();
  form.append("id", eyeglass_info.value.id.toString());
  switch (reset_type) {
    case "reset_leg":
      form.append("is_tryon_leg_auto", true.toString());
      break;
    case "reset_beautify_image":
      form.append("is_tryon_beautify_origin", true.toString());
      break;
    case "reset_all":
      form.append("is_tryon_beautify_origin", true.toString());
      form.append("is_tryon_leg_auto", true.toString());
      break;
  }
  axios.post("/glassmanagement/api/reset-tryon-mode", form).then((response) => {
    // console.log(response);
    const data = response.data.data;
    if (data.data) {
      getPageData();
      message.success(data.msg);
    } else {
      message.error(data.msg);
    }
    reset_confirm_loading.value = false;
  });
};

const onClickIsActive = () => {
  props.changeIsActive(
    eyeglass_info.value.id,
    eyeglass_info.value.sku,
    eyeglass_info.value.is_active,
    eyeglass_info.value.try_on_state,
    getPageData,
  );
};

// ###########################################静态函数###########################################

const setAnnotationDot = (
  x_real: number,
  y_real: number,
  annotate_step: number,
) => {
  const img = document.querySelector(".modal-image") as HTMLImageElement;
  const rect = img.getBoundingClientRect();
  const x = (x_real / img.naturalWidth) * rect.width;
  const y = (y_real / img.naturalHeight) * rect.height;
  // 在图片上显示标注
  // 删除之前的标注
  const annotations = document.querySelectorAll(".annotation");
  annotations.forEach((annotation) => {
    const el = annotation as HTMLElement; // 断言为 HTMLElement
    if (el.dataset.annotation === `${annotate_step}`) {
      el.remove();
    }
  });
  const annotation = document.createElement("div");
  annotation.className = "annotation active"; // 添加激活样式
  annotation.dataset.annotation = `${annotate_step}`;
  const parent = img.parentElement;
  if (!parent) {
    console.error("图片没有父元素，无法添加标注");
    return;
  }
  //
  const offset_rect = parent.getBoundingClientRect();
  const x_offset = x + rect.left - offset_rect.left - 5;
  const y_offset = y + rect.top - offset_rect.top - 5;
  annotation.style.left = `${x_offset}px`;
  annotation.style.top = `${y_offset}px`;
  parent?.appendChild(annotation);
};

const findNearestPoint = (x_real: number, y_real: number) => {
  const contour_points = eyeglass_frame_image.contour_points;
  let x_counter = x_real;
  let y_counter = y_real;
  if (contour_points.length > 0) {
    let minDistance = Infinity;
    // 遍历所有轮廓点找到最近的点
    for (let point of contour_points) {
      const distance =
        Math.pow(point[0] - x_real, 2) + Math.pow(point[1] - y_real, 2);
      if (distance < minDistance) {
        minDistance = distance;
        x_counter = point[0];
        y_counter = point[1];
      }
    }
  }
  return { x_real: x_counter, y_real: y_counter };
};

// 获取页面数据
const getPageData = async () => {
  // 获取镜架美化图片
  axios
    .get("/glassmanagement/api/get-eyeglassframe-tryon-and-beautify", {
      params: {
        id: props.id,
      },
    })
    .then((response) => {
      const data = response.data.data;
      console.log(data);
      if (data) {
        eyeglass_info.value.sku = data.sku;
        eyeglass_info.value.is_tryon_beautify_origin =
          data.is_tryon_beautify_origin;
        eyeglass_info.value.is_tryon_leg_auto = data.is_tryon_leg_auto;
        eyeglass_info.value.try_on_state = data.aiface_tryon_state;
        eyeglass_info.value.is_active = data.is_active;
        eyeglass_info.value.model_type = data.model_type;
        eyeglass_frame_image.frontview_beautify = data.frontview_beautify;
        eyeglass_frame_image.sideview_beautify = data.sideview_beautify;
        processed_beautify_images.frontview_beautify_processed =
          data.frontview_beautify_processed;
        processed_beautify_images.sideview_beautify_processed =
          data.sideview_beautify_processed;
        eyeglass_frame_image.sideview_seg = data.sideview_seg;
        tryon_images.length = 0; // 清空之前的试戴图片
        for (let i = 0; i < data.tryon_images.length; i++) {
          tryon_images.push({
            face_name: data.tryon_images[i].face_name,
            tryon_image: data.tryon_images[i].tryon_image,
            tryon_state: data.tryon_images[i].tryon_state,
          });
        }
      } else {
        console.error("未获取到镜架美化图片数据");
        alert("未获取到镜架美化图片数据");
      }
    });
};
// ###########################################生命周期钩子###########################################
onMounted(() => {
  getPageData();
});
</script>

<style scoped>
.full-height-row {
  height: 100vh;
  display: flex;
  flex-direction: column; /* 子元素垂直排列 */
}
.full-height {
  flex: 1;
  height: max-content;
}
.align-center {
  align-items: center;
}
.page-title {
  margin: 0;
  padding: 40px 39.5px;
  font-size: 30px;
  font-weight: bold;
  display: flex;
  align-items: center;
}

.operation-row {
  width: 100%;
  height: min-content;
  margin: 60px 0;
  padding: 0 39.5px;
}

.operation-button {
  width: 250px;
  height: 75px;
  font-size: 24px;
}

.operation-dropdown {
  width: 250px;
  height: 75px;
  font-size: 24px;
}

:deep(.slick-slide) {
  height: 676px !important;
}
:deep(.slick-slide img) {
  border: 5px solid #fff;
  display: block;
  margin: auto;
  max-width: 80%;
}
:deep(.slick-dots) {
  bottom: -25px;
}

.tryon-image-col {
  /* top: -100px; */
}

.eyeglass-frame-img {
  width: 75%;
  max-height: 40%;
}

.image-title {
  font-size: 30px;
  font-weight: bold;
  margin: 0 15%;
}
:global(.annotation) {
  position: absolute;
  width: 10px;
  height: 10px;
  background-color: rgba(255, 0, 0, 0.5);
  border-radius: 50%;
}

:global(.annotation.active) {
  background-color: rgba(0, 255, 0, 0.5);
}
/* 镜架标注modal相关 */
.modal-image {
  width: 100%;
  height: auto;
  display: block;
  margin: auto;
}
</style>
