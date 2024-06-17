<template>
  <div>
    <a-upload
      :action="uploadAction"
      list-type="picture-card"
      class="avatar-uploader"
      :disabled="disabled"
      :headers="headers"
      :file-list="fileList"
      :beforeUpload="beforeUpload"
      :data="{ biz: bizPath }"
      :multiple="isMultiple"
      :showUploadList="isMultiple"
      @preview="handlePreview"
      @change="handleChange"
    >
      <img
        v-if="!isMultiple && picUrl"
        :src="getAvatarView()"
        style="height: 85px; width: 85px"
      />
      <div
        v-else-if="
          (isMultiple && fileList.length < limit && !disabled) ||
          (!isMultiple && !picUrl)
        "
      >
        <loading-outlined v-if="loading"></loading-outlined>
        <plus-outlined v-else></plus-outlined>
        <div class="ant-upload-text">{{ text }}</div>
      </div>
    </a-upload>
    <span class="delete-img" @click="deleteImg" v-if="picUrl && limit == 1">
      <img :src="require('@/assets/delete.png')" />
    </span>
    <a-modal
      :visible="previewVisible"
      :footer="null"
      @cancel="previewHandleCancel"
    >
      <img alt="example" style="width: 100%" :src="previewImage" />
    </a-modal>
  </div>
</template>

<script>
import { LoadingOutlined, PlusOutlined } from "@ant-design/icons-vue";
import setting from "@/config/setting";

const getFileAccessHttpUrl = (avatar, subStr) => {
  if (!subStr) subStr = "http";
  if (avatar && avatar.startsWith(subStr)) {
    return avatar;
  } else {
    if (avatar && avatar.length > 0 && avatar.indexOf("[") == -1) {
      return process.env.VUE_APP_API_BASE_URL + "/uploads/" + avatar;
    }
  }
};

const uidGenerator = () => {
  return "-" + parseInt(Math.random() * 10000 + 1, 10);
};
const getFileName = (path) => {
  if (path.lastIndexOf("\\") >= 0) {
    let reg = new RegExp("\\\\", "g");
    path = path.replace(reg, "/");
  }
  return path.substring(path.lastIndexOf("/") + 1);
};
export default {
  name: "UploadImage",
  components: {
    PlusOutlined,
    LoadingOutlined,
  },
  data() {
    return {
      uploadAction: process.env.VUE_APP_API_BASE_URL + "/upload/uploadImage",
      headers: {},
      fileList: [],
      previewImage: "",
      previewVisible: false,
      picUrl: false,
      // 上传组件是否可点击
      canClick: true,
      loading: false,
    };
  },
  props: {
    text: {
      type: String,
      default: "上传图片",
    },
    // 父组件传进来的已有的图片数据
    value: {
      type: [String, Array],
      required: false,
    },
    // 后端要求携带的其他参数
    bizPath: {
      type: String,
      required: false,
      default: "temp",
    },
    // 只能查看不可上传和删除时开启该属性
    disabled: {
      type: Boolean,
      required: false,
      default: false,
    },
    // 是否多图
    isMultiple: {
      type: Boolean,
      required: false,
      default: false,
    },
    // 多图情况下限制图片张数
    limit: {
      type: Number,
      required: false,
      default: 1,
    },
  },
  watch: {
    value: {
      handler(val) {
        if (!val) {
          this.picUrl = false;
        }
        this.picUrl = false;
        if (val instanceof Array) {
          this.initFileList(val.join(","));
        } else {
          this.initFileList(val);
        }
      },
      deep: true,
      immediate: true,
    },
  },
  created() {
    const token = setting.takeToken();
    if (token) {
      this.headers[setting.tokenHeaderName] = token;
    }
  },
  methods: {
    // 显示已有图片
    initFileList(paths) {
      // console.log('initFileList', paths)
      if (!paths || paths.length == 0) {
        this.fileList = [];
        return;
      }
      this.picUrl = true;
      let fileList = [];
      let item = paths.split(",");
      for (var i = 0; i < item.length; i++) {
        let url = getFileAccessHttpUrl(item[i]);
        fileList.push({
          uid: uidGenerator(),
          name: getFileName(item[i]),
          status: "done",
          url: url,
          response: {
            status: "history",
            data: item[i],
          },
        });
      }
      this.fileList = fileList;
      // console.log('fileList', this.fileList)
    },
    beforeUpload: function (file) {
      var fileType = file.type;
      if (fileType.indexOf("image") < 0) {
        this.$message.warning("请上传图片");
        return false;
      }
      const isJPG =
        file.type === "image/jpeg" ||
        file.type === "image/jpg" ||
        file.type === "image/png" ||
        file.type === "image/bmp" ||
        file.type === "image/gif";
      if (!isJPG) {
        this.$message.error(
          "上传图片的格式不正确，不是JPG、JPEG、GIF、PNG、BMP",
        );
      }
      const isLt2M = file.size / 1024 / 1024 < 2;
      if (!isLt2M) {
        this.$message.error("文件大小不得超过2M");
      }
      return isJPG && isLt2M;
    },
    /**
     * 删除图片
     */
    deleteImg(e) {
      this.canClick = true;
      this.picUrl = false;
      this.fileList = [];
      // 绑定空值
      this.$emit("update:value", "");
      e.stopPropagation();
    },
    // 关闭弹框
    previewHandleCancel() {
      this.previewVisible = false;
    },
    // 预览
    handlePreview(file) {
      this.previewImage = file.url || file.preview;
      this.previewVisible = true;
    },
    // 上传
    handleChange(info) {
      // console.log('info----handleChange', info)
      this.picUrl = false;
      let fileList = info.fileList;
      if (info.file.status === "done") {
        if (info.file.response.success) {
          this.picUrl = true;
          fileList = fileList.map((file) => {
            if (file.response) {
              file.url = getFileAccessHttpUrl(file.response.data);
            }
            return file;
          });
        }
      } else if (info.file.status === "error") {
        this.$message.error(`${info.file.name} 上传失败.`);
      } else if (info.file.status === "removed") {
        this.handleDelete(info.file);
      }
      this.fileList = fileList;
      if (info.file.status === "done" || info.file.status === "removed") {
        if (info.file.response.code !== 0) {
          // this.$message.error(info.file.response.msg);
        } else {
          this.handlePathChange();
        }
      }
    },
    // 回传父组件
    handlePathChange() {
      let uploadFiles = this.fileList;
      let item = [];
      if (!this.isMultiple) {
        item = uploadFiles[uploadFiles.length - 1].response.data.fileUrl;
      } else {
        for (var i = 0; i < uploadFiles.length; i++) {
          if (typeof uploadFiles[i].response.data == "string") {
            item.push(uploadFiles[i].response.data);
          } else {
            item.push(uploadFiles[i].response.data.fileUrl);
          }
        }
      }
      this.$emit("update:value", item);
      this.$emit("change", item);
    },
    // 删除
    handleDelete(file) {
      console.log(file);
    },
    // 单图上传显示最新的一张
    getAvatarView() {
      if (this.fileList.length > 0) {
        let url = this.fileList[this.fileList.length - 1].url;
        return getFileAccessHttpUrl(url);
      }
    },
  },
  model: {
    prop: "value",
    event: "change",
  },
};
</script>

<style scoped>
.avatar-uploader > .ant-upload {
  width: 128px;
  height: 128px;
}

.ant-upload-select-picture-card i {
  font-size: 32px;
  color: #999;
}

.ant-upload-select-picture-card .ant-upload-text {
  margin-top: 8px;
  color: #666;
}

.delete-img {
  display: inline-block;
  position: absolute;
  left: 105px;
  top: 10px;
  font-size: 20px;
  z-index: 999;
}

.delete-img img {
  position: absolute;

  right: -10px;
  top: -10px;
  width: 25px;
  height: 25px;
  display: inline-block;
}

.delete-img:hover {
  color: #fff;
}
</style>
