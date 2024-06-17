<!-- 编辑弹窗 -->
<template>
  <a-modal
    :width="680"
    :visible="visible"
    :confirm-loading="loading"
    :title="isUpdate ? '修改菜单' : '新建菜单'"
    :body-style="{ paddingBottom: '8px' }"
    @update:visible="updateVisible"
    @ok="save"
  >
    <a-form
      ref="form"
      :model="form"
      :rules="rules"
      :label-col="{ md: { span: 7 }, sm: { span: 24 } }"
      :wrapper-col="{ md: { span: 17 }, sm: { span: 24 } }"
    >
      <a-row :gutter="16">
        <a-col :md="12" :sm="24" :xs="24">
          <a-form-item label="上级菜单:" name="parent_id">
            <a-tree-select
              allow-clear
              :tree-data="menuList"
              tree-default-expand-all
              placeholder="请选择上级菜单"
              v-model:value="form.parent_id"
              :dropdown-style="{ maxHeight: '360px', overflow: 'auto' }"
            />
          </a-form-item>
          <a-form-item label="菜单名称:" name="title">
            <a-input
              allow-clear
              placeholder="请输入菜单名称"
              v-model:value="form.title"
            />
          </a-form-item>
        </a-col>
        <a-col :md="12" :sm="24" :xs="24">
          <a-form-item label="菜单类型:" name="type">
            <a-radio-group v-model:value="form.type" @change="onMenuTypeChange">
              <a-radio :value="0">菜单</a-radio>
              <a-radio :value="1">按钮</a-radio>
            </a-radio-group>
          </a-form-item>
          <a-form-item label="打开方式:">
            <a-radio-group
              v-model:value="form.target"
              :disabled="form.type === 1"
              @change="onTargetChange"
            >
              <a-radio :value="0">组件</a-radio>
              <a-radio :value="1">内链</a-radio>
              <a-radio :value="2">外链</a-radio>
            </a-radio-group>
          </a-form-item>
        </a-col>
      </a-row>
      <div style="margin-bottom: 22px">
        <a-divider />
      </div>
      <a-row :gutter="16">
        <a-col :md="12" :sm="24" :xs="24">
          <a-form-item label="菜单图标:" name="icon">
            <ele-icon-picker
              v-model:value="form.icon"
              :disabled="form.type === 1"
              placeholder="请选择菜单图标"
            />
          </a-form-item>
          <a-form-item name="path">
            <template #label>
              <a-tooltip
                v-if="form.target === 2"
                title="需要以`http://`、`https://`、`//`开头"
              >
                <question-circle-outlined
                  style="vertical-align: -2px; margin-right: 4px"
                />
              </a-tooltip>
              <span>{{ form.target === 2 ? "外链地址" : "路由地址" }}</span>
            </template>
            <a-input
              allow-clear
              v-model:value="form.path"
              :disabled="form.type === 1"
              :placeholder="
                form.target === 2 ? '请输入外链地址' : '请输入路由地址'
              "
            />
          </a-form-item>
          <a-form-item name="component">
            <template #label>
              <a-tooltip
                v-if="form.target === 1"
                title="需要以`http://`、`https://`、`//`开头"
              >
                <question-circle-outlined
                  style="vertical-align: -2px; margin-right: 4px"
                />
              </a-tooltip>
              <span>{{ form.target === 1 ? "内链地址" : "组件路径" }}</span>
            </template>
            <a-input
              allow-clear
              v-model:value="form.component"
              :disabled="form.type === 1 || form.target === 2"
              :placeholder="
                form.target === 1 ? '请输入内链地址' : '请输入组件路径'
              "
            />
          </a-form-item>
        </a-col>
        <a-col :md="12" :sm="24" :xs="24">
          <a-form-item label="权限标识:" name="permission">
            <a-input
              allow-clear
              placeholder="请输入权限标识"
              v-model:value="form.permission"
              :disabled="form.type === 0"
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
          <a-form-item label="是否可见:" name="hide">
            <a-radio-group v-model:value="form.hide">
              <a-radio :value="0">可见</a-radio>
              <a-radio :value="1">不可见</a-radio>
            </a-radio-group>
            <a-tooltip
              title="选择不可见只注册路由不显示在侧边栏，比如添加页面应该选择不可见"
            >
              <question-circle-outlined
                style="vertical-align: -3px; margin-left: 16px"
              />
            </a-tooltip>
          </a-form-item>
        </a-col>
        <a-col :md="12" :sm="24" :xs="24">
          <a-form-item label="菜单状态:" name="status">
            <a-radio-group v-model:value="form.status">
              <a-radio :value="1">在用</a-radio>
              <a-radio :value="2">停用</a-radio>
            </a-radio-group>
          </a-form-item>
        </a-col>
      </a-row>
    </a-form>
  </a-modal>
</template>

<script>
import EleIconPicker from "ele-admin-pro/packages/ele-icon-picker";
import { QuestionCircleOutlined } from "@ant-design/icons-vue";

export default {
  name: "MenuEdit",
  components: { EleIconPicker, QuestionCircleOutlined },
  emits: ["done", "update:visible"],
  props: {
    // 弹窗是否打开
    visible: Boolean,
    // 修改回显的数据
    data: Object,
    // 全部菜单数据
    menuList: Array,
  },
  data() {
    return {
      // 表单数据
      form: this.initFormData(this.data),
      // 表单验证规则
      rules: {
        title: [
          {
            required: true,
            type: "string",
            message: "请输入菜单标题",
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
            this.isUpdate ? "/menu/update" : "/menu/add",
            Object.assign({}, this.form, {
              parent_id: this.form.parent_id || 0,
              target: this.form.target === 2 ? "_blank" : "_self",
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
    /* menuType选择改变 */
    onMenuTypeChange() {
      if (this.form.type === 0) {
        this.form.permission = "";
      } else {
        this.form.target = 0;
        this.form.icon = "";
        this.form.path = "";
        this.form.component = "";
        this.form.hide = 0;
        this.form.isShow = true;
      }
    },
    /* Target选择改变 */
    onTargetChange() {
      console.log(this.form.target);
      if (this.form.target === 2) {
        this.form.component = "";
      }
      console.log("组件" + this.form.component);
    },
    /* 初始化form数据 */
    initFormData(data) {
      let form = {
        type: 0,
        target: 1,
        hide: 1,
        status: 1,
      };
      if (data) {
        let target = 0;
        if (this.isUrl(data.path)) {
          target = 2;
        } else if (this.isUrl(data.component)) {
          target = 1;
        }
        Object.assign(form, data, {
          parent_id: data.parent_id === 0 ? null : data.parent_id,
          isShow: data.hide === 0,
          target: target,
        });
      }
      return form;
    },
    /* 判断是否是网址 */
    isUrl(url) {
      return (
        url &&
        (url.startsWith("http://") ||
          url.startsWith("https://") ||
          url.startsWith("://"))
      );
    },
  },
};
</script>

<style scoped></style>
