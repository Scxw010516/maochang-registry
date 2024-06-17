<template>
  <div class="ele-body ele-body-card">
    <a-card :bordered="false" class="setting-info-tabs">
      <a-tabs v-model:activeKey="activeKey" @change="handleChange">
        <a-tab-pane v-for="(item, index) in config_list" :key="index">
          <template #tab>
            <span>
              <setting-filled />
              {{ item.config_name }}
            </span>
          </template>
          <a-form
            ref="form"
            :model="form"
            :label-col="{ md: { span: 5 }, sm: { span: 24 } }"
            :wrapper-col="{ md: { span: 19 }, sm: { span: 24 } }"
            v-for="(subItem, val) in item.data_list"
            :key="val"
          >
            <!-- 单行文本输入框 -->
            <a-form-item
              v-if="subItem.type == 'text'"
              :label="subItem.title + ':'"
              :name="subItem.code"
            >
              <a-input
                v-model:value="form[subItem.code]"
                :placeholder="'请输入' + subItem.title"
                allow-clear
              />
            </a-form-item>
            <!-- 多行文本框 -->
            <a-form-item
              v-if="subItem.type == 'textarea'"
              :label="subItem.title + ':'"
              :label-col="{ sm: { span: 5 }, xs: { span: 6 } }"
              :wrapper-col="{ sm: { span: 19 }, xs: { span: 18 } }"
            >
              <a-textarea
                v-model:value="form[subItem.code]"
                :placeholder="'请输入' + subItem.title"
                :rows="4"
              />
            </a-form-item>
            <!-- 单图上传 -->
            <a-form-item
              v-if="subItem.type == 'image'"
              :label="subItem.title + ':'"
              :name="subItem.code"
              :label-col="{ sm: { span: 5 }, xs: { span: 6 } }"
              :wrapper-col="{ sm: { span: 19 }, xs: { span: 18 } }"
            >
              <uploadImage :limit="1" v-model:value="form[subItem.code]" />
            </a-form-item>
            <!-- 多图上传 -->
            <a-form-item
              v-if="subItem.type == 'images'"
              :label="subItem.title + ':'"
              :name="subItem.code"
              :label-col="{ sm: { span: 5 }, xs: { span: 6 } }"
              :wrapper-col="{ sm: { span: 19 }, xs: { span: 18 } }"
            >
              <uploadImage
                :limit="10"
                :isMultiple="true"
                v-model:value="form[subItem.code]"
              />
            </a-form-item>
            <!-- 日期选择 -->
            <a-form-item
              v-if="subItem.type == 'date'"
              :label="subItem.title + ':'"
              :name="subItem.code"
            >
              <a-date-picker
                v-model:value="form[subItem.code]"
                value-format="YYYY-MM-DD"
                :placeholder="'请选择' + subItem.title"
                class="ele-fluid"
              />
            </a-form-item>
            <!-- 日期时间选择 -->
            <a-form-item
              v-if="subItem.type == 'datetime'"
              :label="subItem.title + ':'"
              :name="subItem.code"
            >
              <a-date-picker
                v-model:value="form[subItem.code]"
                show-time
                value-format="YYYY-MM-DD HH:mm:ss"
                :placeholder="'请选择' + subItem.title"
                class="ele-fluid"
              />
            </a-form-item>
            <!-- 单选按钮 -->
            <a-form-item
              v-if="subItem.type == 'radio'"
              :label="subItem.title + ':'"
              :name="subItem.code"
            >
              <a-radio-group v-model:value="form[subItem.code]">
                <a-radio
                  v-for="(val, key) in subItem.optionsList"
                  :value="key"
                  :key="val"
                  >{{ val }}</a-radio
                >
              </a-radio-group>
            </a-form-item>
            <!-- 数字输入框 -->
            <a-form-item
              v-if="subItem.type == 'number'"
              :label="subItem.title + ':'"
              :name="subItem.code"
            >
              <a-input-number
                :min="0"
                class="ele-fluid"
                :placeholder="'请输入' + subItem.title"
                v-model:value="form[subItem.code]"
              />
            </a-form-item>
            <!-- 密码输入框 -->
            <a-form-item
              v-if="subItem.type == 'password'"
              :label="subItem.title + ':'"
              :name="subItem.code"
            >
              <a-input-password
                v-model:value="form[subItem.code]"
                :placeholder="'请输入' + subItem.title"
              />
            </a-form-item>
            <!-- 复选框 -->
            <a-form-item
              v-if="subItem.type == 'checkbox'"
              :label="subItem.title + ':'"
              :name="subItem.code"
            >
              <a-checkbox-group
                v-model:value="form[subItem.code]"
                :options="subItem.optionsList"
                :value="subItem.value"
              />
            </a-form-item>
            <!-- 下拉单选框 -->
            <a-form-item
              v-if="subItem.type == 'select'"
              :label="subItem.title + ':'"
              :name="subItem.code"
            >
              <a-select
                v-model:value="form[subItem.code]"
                :placeholder="'请选择' + subItem.title"
                allow-clear
              >
                <a-select-option
                  v-for="(val, key) in subItem.optionsList"
                  :key="key"
                  :value="key"
                >
                  {{ val }}
                </a-select-option>
              </a-select>
            </a-form-item>
            <!-- 富文本编辑器 -->
            <a-form-item
              v-if="subItem.type == 'ueditor'"
              :label="subItem.title + ':'"
              :label-col="{ sm: { span: 5 }, xs: { span: 6 } }"
              :wrapper-col="{ sm: { span: 19 }, xs: { span: 18 } }"
            >
              <!-- 编辑器 -->
              <tinymce-editor
                v-model:value="form[subItem.code]"
                :init="initEditor"
              />
            </a-form-item>
            <!-- 图标 -->
            <a-form-item
              v-if="subItem.type == 'icon'"
              :label="subItem.title + ':'"
              :name="subItem.code"
            >
              <ele-icon-picker
                v-model:value="form[subItem.code]"
                :disabled="false"
                :placeholder="'请选择' + subItem.title"
              />
            </a-form-item>
          </a-form>
          <a-form-item :wrapper-col="{ md: { offset: 2 } }">
            <a-button type="primary" @click="save" :loading="loading">
              {{ loading ? "保存中.." : "保存更改" }}
            </a-button>
          </a-form-item>
        </a-tab-pane>
      </a-tabs>
    </a-card>
  </div>
</template>

<script>
import { SettingFilled } from "@ant-design/icons-vue";
import uploadImage from "@/components/uploadImage";
import TinymceEditor from "@/components/TinymceEditor";
import EleIconPicker from "ele-admin-pro/packages/ele-icon-picker";

export default {
  name: "ConfigWeb",
  components: {
    SettingFilled,
    uploadImage,
    TinymceEditor,
    EleIconPicker,
  },
  data() {
    return {
      // tab页选中
      activeKey: 0,
      // 表单数据
      form: {},
      // 保存按钮loading
      loading: false,
      // 配置
      config_list: [],
      checked: true,
    };
  },
  mounted() {
    this.getConfigInfo();
  },
  computed: {
    /**
     * 初始化编辑器
     */
    initEditor() {
      return {
        height: 300,
        branding: false,
        skin_url: "/tinymce/skins/ui/oxide",
        content_css: "/tinymce/skins/content/default/content.css",
        language_url: "/tinymce/langs/zh_CN.js",
        language: "zh_CN",
        plugins:
          "code print preview fullscreen paste searchreplace save autosave link autolink image imagetools media table codesample lists advlist hr charmap emoticons anchor directionality pagebreak quickbars nonbreaking visualblocks visualchars wordcount",
        toolbar:
          "fullscreen preview code | undo redo | forecolor backcolor | bold italic underline strikethrough | alignleft aligncenter alignright alignjustify | outdent indent | numlist bullist | formatselect fontselect fontsizeselect | link image media emoticons charmap anchor pagebreak codesample | ltr rtl",
        toolbar_drawer: "sliding",
        images_upload_handler: (blobInfo, success, error) => {
          let file = blobInfo.blob();
          // 使用axios上传
          const formData = new FormData();
          formData.append("file", file, file.name);
          this.$http
            .post("/upload/uploadImage", formData)
            .then((res) => {
              if (res.data.code == 0) {
                success(res.data.data);
              } else {
                error(res.data.msg);
              }
            })
            .catch((e) => {
              console.error(e);
              error(e.message);
            });
        },
        file_picker_types: "media",
        file_picker_callback: () => {},
      };
    },
  },
  methods: {
    /**
     * 获取配置信息
     */
    getConfigInfo() {
      this.$http
        .get("/configweb/index")
        .then((res) => {
          if (res.data.code === 0) {
            this.config_list = res.data.data;
            if (this.config_list.length > 0) {
              let data_list = this.config_list[0]["data_list"];
              let itemArr = {};
              data_list.forEach((item) => {
                itemArr[item.code] = item.value;
              });
              this.form = itemArr;
            } else {
              this.form = {};
            }
          }
        })
        .catch((e) => {
          this.$message.error(e.message);
        });
    },
    /* 保存更改 */
    save() {
      this.loading = true;
      this.$http
        .put("/configweb/save", this.form)
        .then((res) => {
          this.loading = false;
          if (res.data.code === 0) {
            this.$message.success(res.data.msg);
          } else {
            this.$message.error(res.data.msg);
          }
        })
        .catch((e) => {
          this.loading = false;
          this.$message.error(e.message);
        });
    },
    /**
     * Tabs切换事件
     */
    handleChange(activeKey) {
      let data_list = this.config_list[activeKey]["data_list"];
      let itemArr = {};
      data_list.forEach((item) => {
        itemArr[item.code] = item.value;
        console.log(item.code + " " + item.value);
      });
      this.form = itemArr;
    },
  },
};
</script>

<style scoped>
/* 右侧卡片 */
.setting-info-tabs :deep(.ant-card-body) {
  padding: 0;
}

.setting-info-tabs :deep(.ant-tabs-tab) {
  padding-left: 4px;
  padding-right: 4px;
  margin: 0 12px 0 28px !important;
}

.setting-info-tabs .ant-form {
  max-width: 580px;
  margin-top: 20px;
  padding: 0 24px;
}
</style>
