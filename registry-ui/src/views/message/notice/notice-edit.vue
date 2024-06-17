<!-- 通知编辑弹窗 -->
<template>
  <a-modal
    :width="1000"
    :visible="visible"
    :confirm-loading="loading"
    :title="isUpdate ? '修改通知' : '新建通知'"
    :body-style="{ paddingBottom: '8px' }"
    @update:visible="updateVisible"
    @ok="save"
  >
    <a-form
      ref="form"
      :model="form"
      :rules="rules"
      :label-col="{ md: { span: 6 }, sm: { span: 24 } }"
      :wrapper-col="{ md: { span: 17 }, sm: { span: 24 } }"
    >
      <a-row :gutter="16">
        <a-col :md="12" :sm="24" :xs="24">
          <a-form-item label="通知标题:" name="title">
            <a-input
              allow-clear
              :maxlength="20"
              placeholder="请输入通知标题"
              v-model:value="form.title"
            />
          </a-form-item>
          <a-form-item label="是否置顶" name="is_top">
            <a-radio-group v-model:value="form.is_top">
              <a-radio :value="1">置顶</a-radio>
              <a-radio :value="2">不置顶</a-radio>
            </a-radio-group>
          </a-form-item>
        </a-col>
        <a-col :md="12" :sm="24" :xs="24">
          <a-form-item label="通知来源:" name="source">
            <a-select
              allow-clear
              placeholder="请选择通知来源"
              v-model:value="form.source"
            >
              <a-select-option :value="1">内部通知</a-select-option>
              <a-select-option :value="2">外部通知</a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="状态" name="status">
            <a-radio-group v-model:value="form.status">
              <a-radio :value="1">正常</a-radio>
              <a-radio :value="2">停用</a-radio>
            </a-radio-group>
          </a-form-item>
        </a-col>
      </a-row>
      <a-form-item
        label="通知内容:"
        name="content"
        :label-col="{ sm: { span: 3 }, xs: { span: 6 } }"
        :wrapper-col="{ sm: { span: 21 }, xs: { span: 18 } }"
      >
        <tinymce-editor v-model:value="form.content" :init="{ height: 450 }" />
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script>
import TinymceEditor from "@/components/TinymceEditor";

export default {
  name: "NoticeEdit",
  emits: ["done", "update:visible"],
  props: {
    // 弹窗是否打开
    visible: Boolean,
    // 修改回显的数据
    data: Object,
  },
  components: { TinymceEditor },
  data() {
    return {
      // 表单数据
      form: Object.assign({}, this.data),
      // 表单验证规则
      rules: {
        title: [
          {
            required: true,
            message: "请输入通知标题",
            type: "string",
            trigger: "blur",
          },
        ],
        source: [
          {
            required: true,
            message: "请选择通知来源",
            type: "number",
            trigger: "blur",
          },
        ],
        is_top: [
          {
            required: true,
            message: "请选择是否置顶",
            type: "number",
            trigger: "blur",
          },
        ],
        status: [
          {
            required: true,
            message: "请选择通知状态",
            type: "number",
            trigger: "blur",
          },
        ],
        content: [
          {
            required: true,
            message: "请输入通知内容",
            type: "string",
            trigger: "blur",
          },
        ],
      },
      // 提交状态
      loading: false,
      // 是否是修改
      isUpdate: false,
    };
  },
  watch: {
    data() {
      if (this.data && this.data.id) {
        this.form = Object.assign({}, this.data);
        this.isUpdate = true;
      } else {
        this.form = {};
        this.isUpdate = false;
      }
      if (this.$refs.form) {
        this.$refs.form.clearValidate();
      }
    },
  },
  mounted() {},
  methods: {
    /* 保存编辑 */
    save() {
      this.$refs.form
        .validate()
        .then(() => {
          this.loading = true;
          this.$http[this.isUpdate ? "put" : "post"](
            this.isUpdate ? "/notice/update" : "/notice/add",
            this.form,
          )
            .then((res) => {
              this.loading = false;
              if (res.data.code === 0) {
                this.$message.success(res.data.msg);
                if (!this.isUpdate) {
                  this.form = {};
                }
                this.updateVisible(false);
                this.$emit("done");
              } else {
                this.$message.error(res.data.msg);
              }
            })
            .catch((e) => {
              this.loading = false;
              this.$message.error(e.message);
            });
        })
        .catch(() => {});
    },
    /* 更新visible */
    updateVisible(value) {
      this.$emit("update:visible", value);
    },
  },
};
</script>

<style scoped></style>
