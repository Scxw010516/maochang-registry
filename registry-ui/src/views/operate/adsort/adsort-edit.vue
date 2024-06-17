<!-- 广告位编辑弹窗 -->
<template>
  <a-modal
    :width="500"
    :visible="visible"
    :confirm-loading="loading"
    :title="isUpdate ? '修改广告位' : '添加广告位'"
    :body-style="{ paddingBottom: '8px' }"
    @update:visible="updateVisible"
    @ok="save"
  >
    <a-form
      ref="form"
      :model="form"
      :rules="rules"
      :label-col="{ md: { span: 6 }, sm: { span: 24 } }"
      :wrapper-col="{ md: { span: 19 }, sm: { span: 24 } }"
    >
      <a-form-item label="广告位描述:" name="description">
        <a-input
          allow-clear
          :maxlength="20"
          placeholder="请输入广告位描述"
          v-model:value="form.description"
        />
      </a-form-item>
      <a-form-item label="广告位位置:" name="loc_id">
        <a-input-number
          :min="0"
          class="ele-fluid"
          placeholder="请输入广告位位置"
          v-model:value="form.loc_id"
        />
      </a-form-item>
      <a-form-item label="投放平台:" name="platform">
        <a-select
          allow-clear
          placeholder="请选择投放平台"
          v-model:value="form.platform"
        >
          <a-select-option :value="1">PC网站</a-select-option>
          <a-select-option :value="2">WAP手机站</a-select-option>
          <a-select-option :value="3">微信小程序</a-select-option>
          <a-select-option :value="4">APP客户端</a-select-option>
        </a-select>
      </a-form-item>
      <a-form-item label="所属栏目" name="cate_id">
        <a-tree-select
          allow-clear
          :tree-data="cateList"
          tree-default-expand-all
          placeholder="请选择所属栏目"
          v-model:value="form.cate_id"
          :dropdown-style="{ maxHeight: '360px', overflow: 'auto' }"
        />
      </a-form-item>
      <a-form-item label="排序号:" name="sort">
        <a-input-number
          :min="0"
          class="ele-fluid"
          placeholder="请输入排序号"
          v-model:value="form.sort"
        />
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script>
export default {
  name: "AdSortEdit",
  emits: ["done", "update:visible"],
  props: {
    // 弹窗是否打开
    visible: Boolean,
    // 修改回显的数据
    data: Object,
    // 全部栏目数据
    cateList: Array,
  },
  data() {
    return {
      // 表单数据
      form: Object.assign({}, this.data),
      // 表单验证规则
      rules: {
        description: [
          {
            required: true,
            message: "请输入广告位描述",
            type: "string",
            trigger: "blur",
          },
        ],
        loc_id: [
          {
            required: true,
            message: "请输入广告位位置",
            type: "number",
            trigger: "blur",
          },
        ],
        platform: [
          {
            required: true,
            message: "请选择投放平台",
            type: "number",
            trigger: "blur",
          },
        ],
        cate_id: [
          {
            required: true,
            message: "请选择所属栏目",
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
          this.$http[this.isUpdate ? "put" : "post"](
            this.isUpdate ? "/adsort/update" : "/adsort/add",
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
