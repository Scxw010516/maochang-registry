<template>
  <div class="ele-body">
    <a-card :bordered="false">
      <!-- 搜索表单 -->
      <a-form
        :model="where"
        :label-col="{ md: { span: 8 }, sm: { span: 24 } }"
        :wrapper-col="{ md: { span: 18 }, sm: { span: 24 } }"
      >
        <a-row>
          <a-col :lg="6" :md="12" :sm="24" :xs="24">
            <a-form-item label="站点名称:">
              <a-input
                v-model:value.trim="where.name"
                placeholder="请输入站点名称"
                allow-clear
              />
            </a-form-item>
          </a-col>
          <a-col :lg="6" :md="12" :sm="24" :xs="24">
            <a-form-item label="站点类型:">
              <a-select
                v-model:value="where.type"
                placeholder="请选择站点类型"
                allow-clear
              >
                <a-select-option :value="1">普通站点</a-select-option>
                <a-select-option :value="2">其他站点</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :lg="6" :md="12" :sm="24" :xs="24">
            <a-form-item style="padding-left: 10px" :wrapper-col="{ span: 24 }">
              <a-space>
                <a-button type="primary" @click="reload">查询</a-button>
                <a-button @click="reset">重置</a-button>
              </a-space>
            </a-form-item>
          </a-col>
        </a-row>
      </a-form>
      <!-- 表格 -->
      <ele-pro-table
        ref="table"
        row-key="id"
        :datasource="url"
        :columns="columns"
        :where="where"
        v-model:selection="selection"
        :scroll="{ x: true }"
      >
        <template #toolbar>
          <a-space>
            <a-button
              type="primary"
              @click="openEdit()"
              v-if="permission.includes('sys:item:add')"
            >
              <template #icon>
                <plus-outlined />
              </template>
              <span>新建</span>
            </a-button>
            <a-button
              type="primary"
              danger
              @click="removeBatch"
              v-if="permission.includes('sys:item:dall')"
            >
              <template #icon>
                <delete-outlined />
              </template>
              <span>删除</span>
            </a-button>
          </a-space>
        </template>
        <!-- 站点图片列 -->
        <template #image="{ record }">
          <a-image :width="35" :src="record.image" />
        </template>
        <!-- 站点类型列 -->
        <template #type="{ record }">
          <a-tag :color="['green', 'orange'][record.type - 1]">
            {{ ["普通站点", "其他站点"][record.type - 1] }}
          </a-tag>
        </template>
        <!-- 状态列 -->
        <template #status="{ record }">
          <a-tag :color="['blue', 'green'][record.status - 1]">
            {{ ["在用", "停用"][record.status - 1] }}
          </a-tag>
        </template>
        <!-- 操作列 -->
        <template #action="{ record }">
          <a-space>
            <a
              @click="openEdit(record)"
              v-if="permission.includes('sys:item:update')"
              >修改</a
            >
            <a-divider type="vertical" />
            <a-popconfirm
              title="确定要删除此站点吗？"
              @confirm="remove(record)"
            >
              <a
                class="ele-text-danger"
                v-if="permission.includes('sys:item:delete')"
                >删除</a
              >
            </a-popconfirm>
          </a-space>
        </template>
      </ele-pro-table>
    </a-card>
  </div>
  <!-- 编辑弹窗 -->
  <item-edit v-model:visible="showEdit" :data="current" @done="reload" />
</template>

<script>
import { mapGetters } from "vuex";
import { createVNode } from "vue";
import {
  DeleteOutlined,
  ExclamationCircleOutlined,
  PlusOutlined,
} from "@ant-design/icons-vue";
import ItemEdit from "./item-edit";

export default {
  name: "SystemItem",
  components: {
    PlusOutlined,
    DeleteOutlined,
    ItemEdit,
  },
  computed: {
    ...mapGetters(["permission"]),
  },
  data() {
    return {
      // 表格数据接口
      url: "/item/list",
      // 表格列配置
      columns: [
        {
          key: "index",
          width: 48,
          customRender: ({ index }) => this.$refs.table.tableIndex + index,
        },
        {
          title: "站点名称",
          dataIndex: "name",
          align: "center",
          width: 200,
        },
        {
          title: "站点图片",
          dataIndex: "image",
          align: "center",
          width: 100,
          slots: { customRender: "image" },
        },
        {
          title: "站点类型",
          dataIndex: "type",
          align: "center",
          width: 100,
          slots: { customRender: "type" },
        },
        {
          title: "站点地址",
          dataIndex: "url",
          align: "center",
          width: 200,
        },
        {
          title: "站点状态",
          dataIndex: "status",
          width: 100,
          align: "center",
          slots: { customRender: "status" },
        },
        {
          title: "排序",
          dataIndex: "sort",
          width: 100,
          align: "center",
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
      where: {},
      // 表格选中数据
      selection: [],
      // 当前编辑数据
      current: null,
      // 是否显示编辑弹窗
      showEdit: false,
    };
  },
  methods: {
    /* 搜索 */
    reload() {
      this.selection = [];
      this.$refs.table.reload({ page: 1, where: this.where });
    },
    /*  重置搜索 */
    reset() {
      this.where = {};
      this.reload();
    },
    /* 删除单个 */
    remove(row) {
      const hide = this.$message.loading("请求中..", 0);
      this.$http
        .delete("/item/delete/" + row.id)
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
        content: "确定要删除选中的站点吗?",
        icon: createVNode(ExclamationCircleOutlined),
        maskClosable: true,
        onOk: () => {
          const hide = this.$message.loading("请求中..", 0);
          this.$http
            .delete("/item/delete/" + this.selection.map((d) => d.id).join(","))
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
          .get("/item/detail/" + row.id)
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
    /* 修改站点状态 */
    editStatus(checked, row) {
      this.$http
        .put("/item/status", { id: row.id, status: checked ? 1 : 2 })
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
};
</script>

<style scoped></style>
