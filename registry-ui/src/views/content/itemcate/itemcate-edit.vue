<!-- 编辑弹窗 -->
<template>
  <a-modal
    :width="680"
    :visible="visible"
    :confirm-loading="loading"
    :title="isUpdate ? '修改栏目' : '新建栏目'"
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
          <a-form-item label="栏目名称" name="name">
            <a-input
              allow-clear
              placeholder="请输入栏目名称"
              v-model:value="form.name"
            />
          </a-form-item>
          <a-form-item label="拼音(全)" name="pinyin">
            <a-input
              allow-clear
              placeholder="请输入拼音(全)"
              v-model:value="form.pinyin"
            />
          </a-form-item>
          <a-form-item label="所属站点:" name="item_id">
            <a-select
              v-model:value="form.item_id"
              placeholder="请选择所属站点"
              allow-clear
            >
              <a-select-option
                v-for="(item, index) in itemList"
                :key="index"
                :value="item.id"
              >
                {{ item.name }}
              </a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="栏目状态" name="status">
            <a-radio-group v-model:value="form.status">
              <a-radio :value="1">正常</a-radio>
              <a-radio :value="2">禁用</a-radio>
            </a-radio-group>
          </a-form-item>
        </a-col>
        <a-col :md="12" :sm="24" :xs="24">
          <a-form-item label="上级栏目" name="pid">
            <a-tree-select
              allow-clear
              :tree-data="cateList"
              tree-default-expand-all
              placeholder="请选择上级栏目"
              v-model:value="form.pid"
              :dropdown-style="{ maxHeight: '360px', overflow: 'auto' }"
            />
          </a-form-item>
          <a-form-item label="拼音(简)" name="code">
            <a-input
              allow-clear
              placeholder="请输入拼音(简)"
              v-model:value="form.code"
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
          <a-form-item label="有无封面" name="is_cover">
            <a-radio-group
              v-model:value="form.is_cover"
              @change="onis_coverChange"
            >
              <a-radio :value="1">有封面</a-radio>
              <a-radio :value="2">无封面</a-radio>
            </a-radio-group>
          </a-form-item>
        </a-col>
      </a-row>
      <a-form-item
        label="栏目封面:"
        name="cover"
        :label-col="{ sm: { span: 3 }, xs: { span: 6 } }"
        :wrapper-col="{ sm: { span: 21 }, xs: { span: 18 } }"
        v-if="form.is_cover === 1"
      >
        <uploadImage :limit="1" v-model:value="form.cover" />
      </a-form-item>
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
import uploadImage from "@/components/uploadImage";

export default {
  name: "ItemCateEdit",
  components: { uploadImage },
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
        name: [
          {
            required: true,
            type: "string",
            message: "请输入栏目名称",
            trigger: "blur",
          },
        ],
        pid: [
          {
            required: true,
            type: "number",
            message: "请选择上级栏目",
            trigger: "blur",
          },
        ],
        pinyin: [
          {
            required: true,
            type: "string",
            message: "请输入拼音(全)",
            trigger: "blur",
          },
        ],
        code: [
          {
            required: true,
            type: "string",
            message: "请输入拼音(简)",
            trigger: "blur",
          },
        ],
        item_id: [
          {
            required: true,
            type: "number",
            message: "请选择所属站点",
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
        status: [
          {
            required: true,
            type: "number",
            message: "请选择栏目状态",
            trigger: "blur",
          },
        ],
        is_cover: [
          {
            required: true,
            type: "number",
            message: "请选择有无封面",
            trigger: "blur",
          },
        ],
      },
      // 提交状态
      loading: false,
      // 是否是修改
      isUpdate: false,
      // 站点列表
      itemList: [],
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
  mounted() {
    // 获取站点列表
    this.getItemList();
  },
  methods: {
    /* 保存编辑 */
    save() {
      this.$refs.form
        .validate()
        .then(() => {
          this.loading = true;
          this.$http[this.isUpdate ? "put" : "post"](
            this.isUpdate ? "/itemcate/update" : "/itemcate/add",
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
      let form = {};
      if (data) {
        Object.assign(form, data, {
          pid: data.pid === 0 ? null : data.pid,
        });
      }
      return form;
    },
    /* is_cover选择改变 */
    onis_coverChange() {
      console.log(this.form.is_cover);
      if (this.form.is_cover === 1) {
        this.form.is_cover = 1;
      } else {
        this.form.is_cover = 2;
      }
    },
    /**
     * 获取站点列表
     */
    getItemList() {
      this.$http
        .get("/item/getItemList")
        .then((res) => {
          if (res.data.code === 0) {
            this.itemList = res.data.data;
          } else {
            this.$message.error(res.data.msg);
          }
        })
        .catch((e) => {
          this.$message.error(e.message);
        });
    },
  },
};
</script>

<style scoped></style>
