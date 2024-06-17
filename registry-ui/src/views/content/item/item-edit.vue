<!-- 站点编辑弹窗 -->
<template>
  <a-modal
    :width="750"
    :visible="visible"
    :confirm-loading="loading"
    :title="isUpdate ? '修改站点' : '新建站点'"
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
      <a-form-item
        label="站点图片:"
        name="image"
        :label-col="{ sm: { span: 3 }, xs: { span: 6 } }"
        :wrapper-col="{ sm: { span: 21 }, xs: { span: 18 } }"
      >
        <uploadImage :limit="1" v-model:value="form.image" />
      </a-form-item>
      <a-row :gutter="16">
        <a-col :md="12" :sm="24" :xs="24">
          <a-form-item label="站点名称:" name="name">
            <a-input
              allow-clear
              :maxlength="20"
              placeholder="请输入站点姓名"
              v-model:value="form.name"
            />
          </a-form-item>
          <a-form-item label="站点地址:" name="url">
            <a-input
              allow-clear
              :maxlength="20"
              placeholder="请输入站点地址"
              v-model:value="form.url"
            />
          </a-form-item>
          <a-form-item label="状态" name="status">
            <a-radio-group v-model:value="form.status">
              <a-radio :value="1">正常</a-radio>
              <a-radio :value="2">停用</a-radio>
            </a-radio-group>
          </a-form-item>
        </a-col>
        <a-col :md="12" :sm="24" :xs="24">
          <a-form-item label="站点类型:" name="type">
            <a-select
              allow-clear
              placeholder="请选择站点类型"
              v-model:value="form.type"
            >
              <a-select-option :value="1">普通站点</a-select-option>
              <a-select-option :value="2">其他站点</a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="排序号:" name="sort">
            <a-input-number
              :min="0"
              class="ele-fluid"
              placeholder="请输入排序号"
              v-model:value="form.sort"
            />
          </a-form-item>
        </a-col>
      </a-row>
      <a-form-item
        label="备注:"
        :label-col="{ sm: { span: 3 }, xs: { span: 6 } }"
        :wrapper-col="{ sm: { span: 21 }, xs: { span: 18 } }"
      >
        <a-textarea
          :rows="3"
          :maxlength="200"
          placeholder="请输入备注"
          v-model:value="form.note"
        />
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script>
import uploadImage from "@/components/uploadImage";

export default {
  name: "ItemEdit",
  emits: ["done", "update:visible"],
  props: {
    // 弹窗是否打开
    visible: Boolean,
    // 修改回显的数据
    data: Object,
  },
  components: { uploadImage },
  data() {
    return {
      // 表单数据
      form: Object.assign({}, this.data),
      // 表单验证规则
      rules: {
        name: [
          {
            required: true,
            message: "请输入站点名称",
            type: "string",
            trigger: "blur",
          },
        ],
        type: [
          {
            required: true,
            message: "请选择站点类型",
            type: "number",
            trigger: "blur",
          },
        ],
        url: [
          {
            required: true,
            message: "请输入站点地址",
            type: "string",
            trigger: "blur",
          },
        ],
        status: [
          {
            required: true,
            message: "请选择站点状态",
            type: "number",
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
  mounted() {},
  methods: {
    /* 保存编辑 */
    save() {
      this.$refs.form
        .validate()
        .then(() => {
          this.loading = true;
          this.$http[this.isUpdate ? "put" : "post"](
            this.isUpdate ? "/item/update" : "/item/add",
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
