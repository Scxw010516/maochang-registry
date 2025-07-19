<template>
  <div class="full-height-row">
    <p class="page-title">
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
              <a-button size="large" @click="onClickChangeTryonMode(1, 0)">
                切换镜架图
              </a-button>
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
              <a-button size="large" @click="onClickChangeTryonMode(1, 0)">
                切换镜架图
              </a-button>
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
    </a-row>
  </div>
  <a-modal
    v-model:visible="annotate_modal.show_annotate_modal"
    width="80%"
    :footer="null"
  >
    <a-space class="page-title">
      镜腿标注步骤：{{ annotate_steps_options[annotate_modal.annotate_step] }}
      <a-button size="large" @click="onClickAnnotatePrev"> 上一步 </a-button>
      <a-button size="large" @click="onClickAnnotateNext"> 下一步 </a-button>

      <a-button type="primary" size="large" @click="onClickAnnotateConfirm">
        确定
      </a-button>
      <a-button size="large" @click="onClickChangeTryonMode(0, 1)">
        {{ eyeglass_info.is_tryon_leg_auto ? "使用标注" : "使用自动" }}
      </a-button>
    </a-space>
    <div style="position: relative">
      <img
        :src="eyeglass_frame_image.sideview_beautify"
        alt=""
        class="modal-image"
        @click="onClickImageToAnnotate"
      />
    </div>
  </a-modal>
</template>
<script lang="ts" setup>
import axios from "axios";
import { reactive, onMounted, ref } from "vue";
import { message, Modal } from "ant-design-vue";
const props = defineProps<{
  id: number; // 试戴的ID
  getTryOnStateLabel: (state: number) => string; // 功能函数：获取试戴标签
}>();
// 原始镜架图
const eyeglass_info = reactive({
  id: props.id,
  sku: "",
  is_tryon_leg_auto: 1, // 是否自动试戴镜腿
  is_tryon_beautify_origin: 1, // 是否使用原始美化图像
});
const eyeglass_frame_image = reactive({
  frontview_beautify: "",
  sideview_beautify: "",
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
const annotate_steps_options = ["左上", "右上", "左下", "右下", "完成"];
// 镜腿标注modal
const annotate_modal = ref({
  show_annotate_modal: false,
  annotate_step: 0, // 镜腿标注步骤 0 左上 1 右上 2 左下 3 右下 4 完成
  annotation_result: [] as Array<{ x: number; y: number }>,
});
// ###########################################点击事件###########################################
const onClickAnnotateLegs = () => {
  // 展开标注modal
  annotate_modal.value.show_annotate_modal = true;
};
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
      formData.append("id", eyeglass_info.id.toString());
      axios
        .post("glassmanagement/api/upload-processed-beautify-image", formData)
        .then((response) => {
          console.log("上传成功:", response.data);
        })
        .catch((error) => {
          console.error("上传失败:", error);
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
// 点击图片标注：获取点击位置并显示
const onClickImageToAnnotate = (event: MouseEvent) => {
  // 获取点击位置并显示
  if (event.target) {
    // 获取点击位置
    const img = event.target as HTMLImageElement;
    const rect = img.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    console.log(`点击位置：(${x}, ${y})`);
    annotate_modal.value.annotation_result[annotate_modal.value.annotate_step] =
      {
        x: x,
        y: y,
      };
    // 在图片上显示标注
    // 删除之前的标注
    const annotations = document.querySelectorAll(".annotation");
    annotations.forEach((annotation) => {
      const el = annotation as HTMLElement; // 断言为 HTMLElement
      if (el.dataset.annotation === `${annotate_modal.value.annotate_step}`) {
        el.remove();
      }
    });
    const annotation = document.createElement("div");
    annotation.className = "annotation active"; // 添加激活样式
    annotation.dataset.annotation = `${annotate_modal.value.annotate_step}`;
    const parent = img.parentElement;
    if (!parent) {
      console.error("图片没有父元素，无法添加标注");
      return;
    }
    //
    const offset_rect = parent.getBoundingClientRect();
    const x_offset = event.clientX - offset_rect.left;
    const y_offset = event.clientY - offset_rect.top;
    annotation.style.left = `${x_offset}px`;
    annotation.style.top = `${y_offset}px`;
    parent?.appendChild(annotation);
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
  } else {
    // 完成标注
    annotate_modal.value.show_annotate_modal = false;
    // 提交标注结果
    console.log("提交标注结果：", annotate_modal.value.annotation_result);
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
  // 构建表单
  const formData = new FormData();
  formData.append(
    "annotation_result",
    JSON.stringify(annotate_modal.value.annotation_result),
  );
  formData.append("id", eyeglass_info.id.toString());
  axios
    .post("/glassmanagement/api/update-annotation-leg", formData)
    .then((response) => {
      console.log(response);
    });
};

// 点击修改试戴模式：切换是否使用美化镜架 ， 切换是否使用自动镜腿
const onClickChangeTryonMode = (changeBeautify: number, changeAuto: number) => {
  if (changeBeautify === 1) {
    // 将布尔值转换为 0 或 1
    eyeglass_info.is_tryon_beautify_origin =
      eyeglass_info.is_tryon_beautify_origin ? 0 : 1;
  }
  if (changeAuto === 1) {
    eyeglass_info.is_tryon_leg_auto = eyeglass_info.is_tryon_leg_auto ? 0 : 1;
  }
  // 创建表单
  const form = new FormData();
  form.append("id", eyeglass_info.id.toString());
  form.append(
    "is_tryon_beautify_origin",
    eyeglass_info.is_tryon_beautify_origin.toString(),
  );
  form.append("is_tryon_leg_auto", eyeglass_info.is_tryon_leg_auto.toString());
  console.log("提交试戴模式修改：", {
    id: eyeglass_info.id,
    is_tryon_beautify_origin: eyeglass_info.is_tryon_beautify_origin,
    is_tryon_leg_auto: eyeglass_info.is_tryon_leg_auto,
  });
  axios
    .post("/glassmanagement/api/update-tryon-mode", form)
    .then((response) => {
      console.log(response);
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
        eyeglass_info.sku = data.sku;
        eyeglass_info.is_tryon_beautify_origin = data.is_tryon_beautify_origin
          ? 1
          : 0;
        eyeglass_info.is_tryon_leg_auto = data.is_tryon_leg_auto ? 1 : 0;
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
        eyeglass_info.sku = data.sku;
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
