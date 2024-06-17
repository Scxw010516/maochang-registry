<!-- 修改密码弹窗 -->
<template>
  <a-modal
    :width="420"
    title="修改密码"
    :visible="visible"
    :confirm-loading="loading"
    :body-style="{ paddingBottom: '16px' }"
    @update:visible="onUpdateVisible"
    @cancel="onCancel"
    @ok="onOk"
  >
    <a-form
      ref="form"
      :model="form"
      :rules="rules"
      :label-col="{ sm: { span: 6 } }"
      :wrapper-col="{ sm: { span: 18 } }"
    >
      <a-form-item label="旧密码" name="oldPassword">
        <a-input-password
          v-model:value="form.oldPassword"
          placeholder="请输入旧密码"
        />
      </a-form-item>
      <a-form-item label="新密码" name="newPassword">
        <a-input-password
          v-model:value="form.newPassword"
          placeholder="请输入新密码"
        />
      </a-form-item>
      <a-form-item label="确认密码" name="rePassword">
        <a-input-password
          v-model:value="form.rePassword"
          placeholder="请再次输入新密码"
        />
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script>
export default {
  name: "UpdatePwd",
  emits: ["update:visible"],
  props: {
    visible: Boolean,
  },
  data() {
    return {
      // 表单数据
      form: {
        oldPassword: "",
        newPassword: "",
        rePassword: "",
      },
      // 表单验证
      rules: {
        oldPassword: [
          {
            required: true,
            message: "请输入旧密码",
            type: "string",
            trigger: "blur",
          },
        ],
        newPassword: [
          {
            required: true,
            message: "请输入新密码",
            type: "string",
            trigger: "blur",
          },
        ],
        rePassword: [
          {
            required: true,
            type: "string",
            trigger: "blur",
            validator: async (rule, value) => {
              if (!value) {
                return Promise.reject("请再次输入新密码");
              }
              if (value === this.form.newPassword) {
                return Promise.resolve();
              }
              return Promise.reject("两次输入密码不一致");
            },
          },
        ],
      },
      // 按钮loading
      loading: false,
    };
  },
  methods: {
    /* 保存修改 */
    onOk() {
      this.$refs.form
        .validate()
        .then(() => {
          this.loading = true;
          this.$http
            .put("/index/updatePwd", this.form)
            .then((res) => {
              this.loading = false;
              if (res.data.code === 0) {
                this.$message.success(res.data.msg);
                this.onUpdateVisible(false);
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
    /* 关闭回调 */
    onCancel() {
      this.form = {};
      this.loading = false;
      this.$refs.form.resetFields();
    },
    /* 修改visible */
    onUpdateVisible(value) {
      this.$emit("update:visible", value);
    },
  },
};
</script>
