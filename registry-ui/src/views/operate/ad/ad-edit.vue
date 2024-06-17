<!-- 广告编辑弹窗 -->
<template>
  <a-modal
    :width="750"
    :visible="visible"
    :confirm-loading="loading"
    :title="isUpdate ? '修改广告' : '新建广告'"
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
        label="广告图片:"
        name="cover"
        :label-col="{ sm: { span: 3 }, xs: { span: 6 } }"
        :wrapper-col="{ sm: { span: 21 }, xs: { span: 18 } }"
      >
        <uploadImage :limit="1" v-model:value="form.cover" />
      </a-form-item>
      <a-row :gutter="16">
        <a-col :md="12" :sm="24" :xs="24">
          <a-form-item label="广告标题:" name="title">
            <a-input
              allow-clear
              :maxlength="20"
              placeholder="请输入广告标题"
              v-model:value="form.title"
            />
          </a-form-item>
          <a-form-item label="广告地址:" name="url">
            <a-input
              allow-clear
              :maxlength="20"
              placeholder="请输入广告地址"
              v-model:value="form.url"
            />
          </a-form-item>
          <a-form-item label="广告宽度:" name="width">
            <a-input-number
              :min="0"
              class="ele-fluid"
              placeholder="请输入广告宽度"
              v-model:value="form.width"
            />
          </a-form-item>
          <a-form-item label="开始时间:" name="start_time">
            <a-date-picker
              class="ele-fluid"
              show-time
              value-format="YYYY-MM-DD hh:mm:ss"
              placeholder="请选择开始时间"
              v-model:value="form.start_time"
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
        </a-col>
        <a-col :md="12" :sm="24" :xs="24">
          <a-form-item label="广告类型:" name="type">
            <a-select
              allow-clear
              placeholder="请选择广告类型"
              v-model:value="form.type"
            >
              <a-select-option :value="1">图片</a-select-option>
              <a-select-option :value="2">文字</a-select-option>
              <a-select-option :value="3">视频</a-select-option>
              <a-select-option :value="4">推荐</a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="广告位:" name="sort_id">
            <a-select
              v-model:value="form.sort_id"
              placeholder="请选择广告位"
              allow-clear
            >
              <a-select-option
                v-for="(item, index) in sortList"
                :key="index"
                :value="item.id"
              >
                {{ item.description }}
              </a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="广告高度:" name="height">
            <a-input-number
              :min="0"
              class="ele-fluid"
              placeholder="请输入广告高度"
              v-model:value="form.height"
            />
          </a-form-item>
          <a-form-item label="结束时间:" name="end_time">
            <a-date-picker
              class="ele-fluid"
              show-time
              value-format="YYYY-MM-DD hh:mm:ss"
              placeholder="请选择结束时间"
              v-model:value="form.end_time"
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
import uploadImage from "@/components/uploadImage";

export default {
  name: "AdEdit",
  emits: ["done", "update:visible"],
  props: {
    // 弹窗是否打开
    visible: Boolean,
    // 修改回显的数据
    data: Object,
    // 全部广告位数据
    sortList: Array,
  },
  components: { uploadImage },
  data() {
    return {
      // 表单数据
      form: Object.assign({}, this.data),
      // 表单验证规则
      rules: {
        title: [
          {
            required: true,
            message: "请输入广告标题",
            type: "string",
            trigger: "blur",
          },
        ],
        type: [
          {
            required: true,
            message: "请选择广告类型",
            type: "number",
            trigger: "blur",
          },
        ],
        url: [
          {
            required: true,
            message: "请输入广告地址",
            type: "string",
            trigger: "blur",
          },
        ],
        sort_id: [
          {
            required: true,
            message: "请选择所属广告位",
            type: "number",
            trigger: "blur",
          },
        ],
        status: [
          {
            required: true,
            message: "请选择广告状态",
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
        this.form = Object.assign({}, this.data, {
          start_time: this.$util.toDateString(this.data.start_time),
          end_time: this.$util.toDateString(this.data.end_time),
        });
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
            this.isUpdate ? "/ad/update" : "/ad/add",
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
