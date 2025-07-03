<template>
  <div class="full-height-row">
    <p
      style="
        margin: 0;
        padding: 40px 39.5px;
        font-size: 30px;
        font-weight: bold;
      "
    >
      试戴状态 待处理：0个 、处理中：0个、处理完成：0个、处理失败：0个
    </p>
    <a-row class="full-height align-center">
      <!-- 试戴图片 -->
      <a-col span="12" class="tryon-image-col">
        <a-carousel>
          <div v-for="item in 2" :key="item">
            <img :src="`src/assets/ai-face-${item}.png`" />
          </div>
        </a-carousel>
      </a-col>
      <!-- 镜架图片 操作按钮   -->
      <a-col span="12">
        <!-- todo：可能要用走马灯展示原始图像和修改后的图像 -->
        <a-col> 正视图 </a-col>
        <a-col> 侧视图 </a-col>
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
</template>
<script lang="ts" setup>
const props = defineProps<{
  id: number; // 试戴的ID
  getTryOnStateLabel: (state: number) => string; // 功能函数：获取试戴标签
}>();

// 试戴图片

// ###########################################点击事件###########################################
const onClickAnnotateLegs = () => {
  // 展开标注modal
  console.log("点击镜腿标注");
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
      console.log("上传的文件:", file);
      // 在这里可以添加上传逻辑
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
  // 模拟下载镜架图
  const linkfront = document.createElement("a");
  linkfront.href = "src/assets/ai-face-1.png"; // 假设这是镜架图的URL
  linkfront.download = "eyeglass-frame-front.png";
  document.body.appendChild(linkfront);
  linkfront.click();
  document.body.removeChild(linkfront);
  const linkside = document.createElement("a");
  linkside.href = "src/assets/ai-face-2.png"; // 假设这是镜架图的URL
  linkside.download = "eyeglass-frame-side.png";
  document.body.appendChild(linkside);
  linkside.click();
  document.body.removeChild(linkside);
};
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

.align-center {
  align-items: center;
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
</style>
