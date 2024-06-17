<!-- 编辑弹窗 -->
<template>
  <a-modal
    :width="680"
    :visible="visible"
    :confirm-loading="loading"
    :title="isUpdate ? '修改部门' : '新建部门'"
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
          <a-form-item label="部门名称" name="name">
            <a-input
              allow-clear
              placeholder="请输入部门名称"
              v-model:value="form.name"
            />
          </a-form-item>
          <a-form-item label="部门类型：" name="type">
            <a-select
              v-model:value="form.type"
              placeholder="请选择部门类型"
              allow-clear
            >
              <a-select-option :value="1">公司</a-select-option>
              <a-select-option :value="2">子公司</a-select-option>
              <a-select-option :value="3">部门</a-select-option>
              <a-select-option :value="4">小组</a-select-option>
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
        <a-col :md="12" :sm="24" :xs="24">
          <a-form-item label="部门编码" name="code">
            <a-input
              allow-clear
              placeholder="请输入部门编码"
              v-model:value="form.code"
            />
          </a-form-item>
          <a-form-item label="上级部门" name="pid">
            <a-tree-select
              allow-clear
              :tree-data="deptList"
              tree-default-expand-all
              placeholder="请选择上级部门"
              v-model:value="form.pid"
              :dropdown-style="{ maxHeight: '360px', overflow: 'auto' }"
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
          v-model:value="form.note"
          placeholder="请输入备注"
          :rows="3"
        />
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script>
export default {
  name: "DeptEdit",
  components: {},
  emits: ["done", "update:visible"],
  props: {
    // 弹窗是否打开
    visible: Boolean,
    // 修改回显的数据
    data: Object,
    // 全部部门数据
    deptList: Array,
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
            type: "string",
            message: "请输入部门名称",
            trigger: "blur",
          },
        ],
        fullname: [
          {
            required: true,
            type: "string",
            message: "请输入部门全称",
            trigger: "blur",
          },
        ],
        code: [
          {
            required: true,
            type: "string",
            message: "请输入部门编码",
            trigger: "blur",
          },
        ],
        pid: [
          {
            required: true,
            type: "number",
            message: "请选择上级部门",
            trigger: "blur",
          },
        ],
        type: [
          {
            required: true,
            type: "number",
            message: "请选择部门类型",
            trigger: "blur",
          },
        ],
        sort: [
          {
            required: true,
            type: "number",
            message: "请输入排序号",
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
      this.isUpdate = !!(this.data && this.data.id);
      this.form = this.initFormData(this.data);
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
          this.$http[this.isUpdate ? "put" : "post"](
            this.isUpdate ? "/dept/update" : "/dept/add",
            Object.assign({}, this.form, {
              pid: this.form.pid || 0,
            }),
          )
            .then((res) => {
              this.loading = false;
              if (res.data.code === 0) {
                this.$message.success(res.data.msg);
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
    /* 初始化form数据 */
    initFormData(data) {
      // 初始化默认值
      let form = { type: 1 };
      if (data) {
        Object.assign(form, data, {
          pid: data.pid === 0 ? null : data.pid,
        });
      }
      return form;
    },
  },
};
</script>

<style scoped></style>
