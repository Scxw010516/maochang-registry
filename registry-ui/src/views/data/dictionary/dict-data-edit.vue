<!-- 字典项编辑弹窗 -->
<template>
  <a-modal
    :width="460"
    :visible="visible"
    :confirm-loading="loading"
    :body-style="{ paddingBottom: '8px' }"
    :title="isUpdate ? '修改字典项' : '添加字典项'"
    @update:visible="updateVisible"
    @ok="save"
  >
    <a-form
      ref="form"
      :model="form"
      :rules="rules"
      :label-col="{ md: { span: 6 }, sm: { span: 24 } }"
      :wrapper-col="{ md: { span: 18 }, sm: { span: 24 } }"
    >
      <a-form-item label="字典项名称:" name="name">
        <a-input
          allow-clear
          :maxlength="20"
          placeholder="请输入字典项名称"
          v-model:value="form.name"
        />
      </a-form-item>
      <a-form-item label="字典项值:" name="value">
        <a-input
          allow-clear
          :maxlength="20"
          placeholder="请输入字典项值"
          v-model:value="form.value"
        />
      </a-form-item>
      <a-form-item label="排序号:" name="sort">
        <a-input-number
          :min="0"
          :max="9999"
          class="ele-fluid"
          placeholder="请输入排序号"
          v-model:value="form.sort"
        />
      </a-form-item>
      <a-form-item label="备注:">
        <a-textarea
          :rows="4"
          :maxlength="200"
          placeholder="请输入备注"
          v-model:value="form.note"
        />
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script>
export default {
  name: "SysDictDataEdit",
  emits: ["done", "update:visible"],
  props: {
    // 弹窗是否打开
    visible: Boolean,
    // 修改回显的数据
    data: Object,
    // 字典id
    dictId: Number,
  },
  data() {
    return {
      // 表单数据
      form: Object.assign({}, this.data),
      // 表单验证规则
      rules: {
        name: [
          {
            required: true,
            message: "请输入字典项名称",
            type: "string",
            trigger: "blur",
          },
        ],
        code: [
          {
            required: true,
            message: "请输入字典项值",
            type: "string",
            trigger: "blur",
          },
        ],
        sort: [
          {
            required: true,
            message: "请输入排序号",
            type: "number",
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
  methods: {
    /* 保存编辑 */
    save() {
      this.$refs.form
        .validate()
        .then(() => {
          this.loading = true;
          if (!this.isUpdate) {
            this.form.dict_id = this.dictId;
          }
          this.$http[this.isUpdate ? "put" : "post"](
            this.isUpdate ? "/dictdata/update" : "/dictdata/add",
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
