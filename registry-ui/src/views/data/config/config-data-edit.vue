<!-- 配置项编辑弹窗 -->
<template>
  <a-modal
    :width="750"
    :visible="visible"
    :confirm-loading="loading"
    :body-style="{ paddingBottom: '8px' }"
    :title="isUpdate ? '修改配置项' : '添加配置项'"
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
      <a-row :gutter="16">
        <a-col :md="12" :sm="24" :xs="24">
          <a-form-item label="配置项名称:" name="title">
            <a-input
              allow-clear
              :maxlength="20"
              placeholder="请输入配置项名称"
              v-model:value="form.title"
            />
          </a-form-item>
          <a-form-item label="配置项类型：" name="type">
            <a-select
              v-model:value="form.type"
              placeholder="请选择配置项类型"
              allow-clear
            >
              <a-select-option value="readonly">只读文本</a-select-option>
              <a-select-option value="number">数字</a-select-option>
              <a-select-option value="text">单行文本</a-select-option>
              <a-select-option value="textarea">多行文本</a-select-option>
              <a-select-option value="array">数组</a-select-option>
              <a-select-option value="password">密码</a-select-option>
              <a-select-option value="radio">单选框</a-select-option>
              <a-select-option value="checkbox">复选框</a-select-option>
              <a-select-option value="select">下拉框</a-select-option>
              <a-select-option value="icon">字体图标</a-select-option>
              <a-select-option value="date">日期</a-select-option>
              <a-select-option value="datetime">时间</a-select-option>
              <a-select-option value="image">单张图片</a-select-option>
              <a-select-option value="images">多张图片</a-select-option>
              <a-select-option value="file">单个文件</a-select-option>
              <a-select-option value="files">多个文件</a-select-option>
              <a-select-option value="ueditor">富文本</a-select-option>
            </a-select>
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
        </a-col>
        <a-col :md="12" :sm="24" :xs="24">
          <a-form-item label="配置编码:" name="code">
            <a-input
              allow-clear
              :maxlength="20"
              placeholder="请输入配置编码"
              v-model:value="form.code"
            />
          </a-form-item>
          <a-form-item label="配置项值:" name="value">
            <a-input
              v-model:value="form.value"
              placeholder="请输入配置项值"
              allow-clear
            />
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
export default {
  name: "ConfigDataEdit",
  emits: ["done", "update:visible"],
  props: {
    // 弹窗是否打开
    visible: Boolean,
    // 修改回显的数据
    data: Object,
    // 配置id
    configId: Number,
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
            message: "请输入配置项名称",
            type: "string",
            trigger: "blur",
          },
        ],
        code: [
          {
            required: true,
            message: "请输入配置项值",
            type: "string",
            trigger: "blur",
          },
        ],
        status: [
          {
            required: true,
            message: "请选择配置项状态",
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
  methods: {
    /* 保存编辑 */
    save() {
      this.$refs.form
        .validate()
        .then(() => {
          this.loading = true;
          if (!this.isUpdate) {
            this.form.config_id = this.configId;
          }
          this.$http[this.isUpdate ? "put" : "post"](
            this.isUpdate ? "/configdata/update" : "/configdata/add",
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
