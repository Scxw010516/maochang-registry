<template>
  <a-button @click="handleClick">upload ai faces</a-button>
</template>

<script lang="ts" setup>
import axios from "axios";
import { ref } from "vue";
const count = ref(0);
const handleClick = () => {
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
      formData.append("face_img", file);
      formData.append("pupil_distance", "63"); // 示例值，实际应用中应根据需要设置
      formData.append("name", file.name);
      axios
        .post("glassmanagement/api/upload-ai-face", formData)
        .then((response) => {
          console.log("上传成功:", response.data);
        })
        .catch((error) => {
          console.error("上传失败:", error);
        });
    }
  };
  input.click();
};
</script>
<style scoped></style>
