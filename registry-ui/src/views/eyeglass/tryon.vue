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
      {{ eyeglass_info.sku }} 待处理：{{ tryon_count.wait }}个 、处理中：{{
        tryon_count.processing
      }}个、处理完成：{{ tryon_count.success }}个、处理失败：{{
        tryon_count.failed
      }}个、未进行试戴：{{ tryon_count.undealt }}个
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
        <!-- todo：可能要用走马灯展示原始图像和修改后的图像 -->
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
          @click="onClickUpload('front')"
        >
          上传镜架正视图
        </a-button>
      </a-col>
      <a-col>
        <a-button
          type="primary"
          class="operation-button"
          @click="onClickUpload('side')"
        >
          上传镜架侧视图
        </a-button>
      </a-col>
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
        <a-button
          type="primary"
          class="operation-button"
          @click="onClickChangeTryonMode"
        >
          修改试戴模式
        </a-button>
      </a-col>
    </a-row>
  </div>
  <a-modal
    v-model:open="annotate_modal.show_annotate_modal"
    width="80%"
    :footer="null"
  >
    <a-space class="page-title">
      镜腿标注步骤：{{ annotation_steps_options[annotate_modal.annotate_step] }}
      <a-button size="large" @click="onClickAnnotatePrev"> 上一步 </a-button>
      <a-button size="large" @click="onClickAnnotateNext"> 下一步 </a-button>

      <a-button type="primary" size="large" @click="onClickAnnotateConfirm">
        确定
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
  <a-modal
    v-model:open="change_tryon_mode_modal.show_change_tryon_mode_modal"
    centered
    title="修改试戴模式"
    okText="修改并生成试戴任务"
    cancelText="取消"
    :confirm-loading="change_tryon_mode_modal.confirm_loading"
    @ok="onClickGenerateTryonTask"
  >
    <a-form-item label="是否自动处理镜腿">
      <a-switch v-model:checked="change_tryon_mode_modal.is_tryon_leg_auto" />
    </a-form-item>
    <a-form-item label="是否使用原始美化图像">
      <a-switch
        v-model:checked="change_tryon_mode_modal.is_tryon_beautify_origin"
      />
    </a-form-item>
  </a-modal>
</template>
<script lang="ts" setup>
import axios from "axios";
import { reactive, onMounted, ref, h } from "vue";
import { message, Modal } from "ant-design-vue";
import { set } from "nprogress";
import { siderProps } from "ant-design-vue/es/layout/Sider";
import { LeftOutlined } from "@ant-design/icons-vue";
interface TryonPageProps {
  id: number; // 试戴的ID
  onClickBack: () => void; // 功能函数：返回
}
const props = withDefaults(defineProps<TryonPageProps>(), {
  onClickBack: () => {},
  id: 0,
});
// 原始镜架图
const eyeglass_info = ref({
  id: props.id,
  sku: "",
  is_tryon_leg_auto: true, // 是否自动试戴镜腿
  is_tryon_beautify_origin: true, // 是否使用原始美化图像
});
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
// 试戴图片
interface TryOnImage {
  face_name: string;
  tryon_image: string;
  tryon_state: number; // 试戴状态
}
const tryon_images = reactive<TryOnImage[]>([]);

const tryon_count = reactive({
  wait: 0, // 待处理
  processing: 0, // 处理中
  success: 0, // 处理完成
  failed: 0, // 处理失败
  undealt: 0, // 未进行试戴
});
const annotation_steps_options = ["左上", "右上", "左下", "右下", "完成"];
// 镜腿标注modal
const annotate_modal = ref({
  show_annotate_modal: false,
  annotate_step: 0, // 镜腿标注步骤 0 左上 1 右上 2 左下 3 右下 4 完成
  annotation_result: [] as Array<{ x: number; y: number }>,
});

// 修改试戴模式modal
const change_tryon_mode_modal = ref({
  show_change_tryon_mode_modal: false,
  confirm_loading: false,
  is_tryon_leg_auto: true, // 是否自动试戴镜腿
  is_tryon_beautify_origin: true, // 是否使用原始美化图像
});
// ###########################################点击事件###########################################
const onClickUpload = (type: "front" | "side") => {
  // 打开上传窗口
  const input = document.createElement("input");
  input.type = "file";
  input.accept = "image/*";
  input.onchange = (event: Event) => {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files.length > 0) {
      const file = target.files[0];
      // 构建FormData对象
      const formData = new FormData();
      formData.append("image", file);
      formData.append("type", type);
      formData.append("id", eyeglass_info.value.id.toString());
      axios
        .post("glassmanagement/api/upload-processed-beautify-image", formData)
        .then((response) => {
          if (response.data.code === 0) {
            message.success(response.data.msg);
          } else {
            message.error(response.data.msg);
          }
        })
        .catch((error) => {
          console.error("上传失败:", error);
          message.error(error);
        });
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
        message.success(response.data.msg);
      });
  } else {
    message.error("请标注完整4个镜腿位置");
  }
};

// 点击修改试戴模式：展开修改试戴模式modal
const onClickChangeTryonMode = () => {
  // 展开修改试戴模式modal
  change_tryon_mode_modal.value.show_change_tryon_mode_modal = true;
  change_tryon_mode_modal.value.is_tryon_leg_auto =
    eyeglass_info.value.is_tryon_leg_auto;
  change_tryon_mode_modal.value.is_tryon_beautify_origin =
    eyeglass_info.value.is_tryon_beautify_origin;
};

// 点击更新试戴模式并生成试戴任务：更新试戴模式并生成试戴任务
const onClickGenerateTryonTask = () => {
  change_tryon_mode_modal.value.confirm_loading = true;
  // 构建表单
  const form = new FormData();
  form.append("id", eyeglass_info.value.id.toString());
  form.append(
    "is_tryon_beautify_origin",
    change_tryon_mode_modal.value.is_tryon_beautify_origin.toString(),
  );
  form.append(
    "is_tryon_leg_auto",
    change_tryon_mode_modal.value.is_tryon_leg_auto.toString(),
  );
  axios
    .post("/glassmanagement/api/update-tryon-mode", form)
    .then((response) => {
      // console.log(response);
      const data = response.data.data;
      if (data.data) {
        eyeglass_info.value.is_tryon_beautify_origin =
          data.data.is_tryon_beautify_origin;
        eyeglass_info.value.is_tryon_leg_auto = data.data.is_tryon_leg_auto;
        message.success(data.msg);
      } else {
        message.error(data.msg);
      }
      change_tryon_mode_modal.value.show_change_tryon_mode_modal = false;
      change_tryon_mode_modal.value.confirm_loading = false;
    });
};

// ###########################################静态函数###########################################
const getTryOnStateLabel = (state: number) => {
  switch (state) {
    case -1:
      return "未进行试戴";
    case 0:
      return "待处理";
    case 1:
      return "处理中";
    case 2:
      return "处理完成";
    case 3:
      return "处理失败";
    default:
      return "无";
  }
};

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

// ###########################################生命周期钩子###########################################
onMounted(() => {
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
        tryon_count.wait = data.tryon_wait_count;
        tryon_count.processing = data.tryon_processing_count;
        tryon_count.success = data.tryon_success_count;
        tryon_count.failed = data.tryon_failed_count;
        tryon_count.undealt = data.tryon_undealt_count;
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
