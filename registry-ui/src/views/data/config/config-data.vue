<template>
  <!-- 表格 -->
  <ele-pro-table
    ref="table"
    row-key="id"
    :datasource="url"
    :columns="columns"
    :where="where"
    tool-class="ele-toolbar-form"
    v-model:selection="selection"
    :scroll="{ x: 1000 }"
  >
    <template #toolbar>
      <a-row :gutter="16">
        <a-col :lg="6" :md="8" :sm="24" :xs="24">
          <a-input
            v-model:value.trim="where.keywords"
            placeholder="输入关键字搜索"
            allow-clear
          />
        </a-col>
        <a-col :lg="6" :md="8" :sm="24" :xs="24">
          <a-space size="middle">
            <a-button type="primary" @click="reload">查询</a-button>
            <a-button
              type="primary"
              @click="openEdit()"
              v-if="permission.includes('sys:config:add')"
              >新建</a-button
            >
            <a-button
              type="primary"
              danger
              @click="removeBatch"
              v-if="permission.includes('sys:config:dall')"
              >删除</a-button
            >
          </a-space>
        </a-col>
      </a-row>
    </template>
    <!-- 配置项类型列 -->
    <template #type="{ record }">
      <a-tag v-if="record.type === 'readonly'" color="blue">只读文本</a-tag>
      <a-tag v-if="record.type === 'number'" color="green">数字</a-tag>
      <a-tag v-if="record.type === 'text'" color="orange">单行文本</a-tag>
      <a-tag v-if="record.type === 'textarea'" color="green">多行文本</a-tag>
      <a-tag v-if="record.type === 'array'" color="blue">数组</a-tag>
      <a-tag v-if="record.type === 'password'" color="green">密码</a-tag>
      <a-tag v-if="record.type === 'radio'" color="orange">单选框</a-tag>
      <a-tag v-if="record.type === 'checkbox'" color="green">复选框</a-tag>
      <a-tag v-if="record.type === 'select'" color="orange">下拉框</a-tag>
      <a-tag v-if="record.type === 'icon'" color="green">字体图标</a-tag>
      <a-tag v-if="record.type === 'date'" color="orange">日期</a-tag>
      <a-tag v-if="record.type === 'datetime'" color="green">时间</a-tag>
      <a-tag v-if="record.type === 'image'" color="orange">单张图片</a-tag>
      <a-tag v-if="record.type === 'images'" color="green">多张图片</a-tag>
      <a-tag v-if="record.type === 'file'" color="orange">单个文件</a-tag>
      <a-tag v-if="record.type === 'files'" color="green">多个文件</a-tag>
      <a-tag v-if="record.type === 'ueditor'" color="blue">富文本编辑器</a-tag>
    </template>
    <!-- 状态列 -->
    <template #status="{ text, record }">
      <a-switch
        :checked="text === 1"
        @change="(checked) => editStatus(checked, record)"
      />
    </template>
    <!-- 操作列 -->
    <template #action="{ record }">
      <a-space>
        <a
          @click="openEdit(record)"
          v-if="permission.includes('sys:config:update')"
          >修改</a
        >
        <a-divider type="vertical" />
        <a-popconfirm title="确定要删除此配置项吗？" @confirm="remove(record)">
          <a
            class="ele-text-danger"
            v-if="permission.includes('sys:config:delete')"
            >删除</a
          >
        </a-popconfirm>
      </a-space>
    </template>
  </ele-pro-table>
  <!-- 编辑弹窗 -->
  <config-data-edit
    v-model:visible="showEdit"
    :data="current"
    :config-id="configId"
    @done="reload"
  />
</template>

<script>
import { mapGetters } from "vuex";
import { createVNode } from "vue";
import { ExclamationCircleOutlined } from "@ant-design/icons-vue";
import ConfigDataEdit from "./config-data-edit";

export default {
  name: "ConfigData",
  components: { ConfigDataEdit },
  props: {
    // 配置id
    configId: Number,
  },
  computed: {
    ...mapGetters(["permission"]),
  },
  data() {
    return {
      // 表格数据接口
      url: "/configdata/list",
      // 表格列配置
      columns: [
        {
          key: "index",
          title: "编号",
          width: 48,
          align: "center",
          customRender: ({ index }) => this.$refs.table.tableIndex + index,
        },
        {
          title: "配置项标题",
          dataIndex: "title",
          align: "center",
          width: 150,
        },
        {
          title: "配置编码",
          dataIndex: "code",
          align: "center",
          width: 150,
        },
        {
          title: "配置类型",
          dataIndex: "type",
          align: "center",
          width: 100,
          slots: { customRender: "type" },
        },
        {
          title: "配置项值",
          dataIndex: "value",
          align: "center",
          ellipsis: true,
          width: 200,
        },
        {
          title: "状态",
          dataIndex: "status",
          width: 100,
          align: "center",
          slots: { customRender: "status" },
        },
        {
          title: "排序号",
          dataIndex: "sort",
          align: "center",
          width: 100,
        },
        {
          title: "备注",
          dataIndex: "note",
          align: "center",
          width: 200,
        },
        {
          title: "创建时间",
          dataIndex: "create_time",
          align: "center",
          width: 160,
          customRender: ({ text }) => this.$util.toDateString(text),
        },
        {
          title: "更新时间",
          dataIndex: "update_time",
          align: "center",
          width: 160,
          customRender: ({ text }) => this.$util.toDateString(text),
        },
        {
          title: "操作",
          key: "action",
          width: 100,
          align: "center",
          slots: { customRender: "action" },
        },
      ],
      // 表格搜索条件
      where: {
        configId: this.configId,
      },
      // 表格选中数据
      selection: [],
      // 当前编辑数据
      current: null,
      // 是否显示编辑弹窗
      showEdit: false,
    };
  },
  methods: {
    /* 刷新表格 */
    reload() {
      this.$refs.table.reload({ page: 1, where: this.where });
    },
    /* 打开编辑弹窗 */
    openEdit(row) {
      if (!row) {
        // 添加
        this.current = row;
        this.showEdit = true;
      } else {
        // 编辑
        this.loading = true;
        this.$http
          .get("/configdata/detail/" + row.id)
          .then((res) => {
            this.loading = false;
            if (res.data.code === 0) {
              this.current = Object.assign({}, res.data.data);
              this.showEdit = true;
            } else {
              this.$message.error(res.data.msg);
            }
          })
          .catch((e) => {
            this.loading = false;
            this.$message.error(e.message);
          });
      }
    },
    /* 删除单个 */
    remove(row) {
      const hide = this.$message.loading("请求中..", 0);
      this.$http
        .delete("/configdata/delete/" + row.id)
        .then((res) => {
          hide();
          if (res.data.code === 0) {
            this.$message.success(res.data.msg);
            this.reload();
          } else {
            this.$message.error(res.data.msg);
          }
        })
        .catch((e) => {
          hide();
          this.$message.error(e.message);
        });
    },
    /* 批量删除 */
    removeBatch() {
      if (!this.selection.length) {
        this.$message.error("请至少选择一条数据");
        return;
      }
      this.$confirm({
        title: "提示",
        content: "确定要删除选中的配置项吗?",
        icon: createVNode(ExclamationCircleOutlined),
        maskClosable: true,
        onOk: () => {
          const hide = this.$message.loading("请求中..", 0);
          this.$http
            .delete(
              "/configdata/delete/" + this.selection.map((d) => d.id).join(","),
            )
            .then((res) => {
              hide();
              if (res.data.code === 0) {
                this.$message.success(res.data.msg);
                this.reload();
              } else {
                this.$message.error(res.data.msg);
              }
            })
            .catch((e) => {
              hide();
              this.$message.error(e.message);
            });
        },
      });
    },
    /* 修改状态 */
    editStatus(checked, row) {
      this.$http
        .put("/configdata/status", { id: row.id, status: checked ? 1 : 2 })
        .then((res) => {
          if (res.data.code === 0) {
            row.status = checked ? 1 : 2;
            this.$message.success(res.data.msg);
          } else {
            this.$message.error(res.data.msg);
          }
        })
        .catch((e) => {
          this.$message.error(e.message);
        });
    },
  },
  watch: {
    // 监听配置id变化
    configId() {
      this.where.configId = this.configId;
      this.reload();
    },
  },
};
</script>

<style scoped></style>
