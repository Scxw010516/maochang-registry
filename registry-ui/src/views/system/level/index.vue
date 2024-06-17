<template>
  <div class="ele-body">
    <a-card :bordered="false">
      <!-- 搜索表单 -->
      <a-form
        :model="where"
        :label-col="{ md: { span: 6 }, sm: { span: 24 } }"
        :wrapper-col="{ md: { span: 18 }, sm: { span: 24 } }"
      >
        <a-row>
          <a-col :lg="6" :md="12" :sm="24" :xs="24">
            <a-form-item label="职级名称:">
              <a-input
                v-model:value.trim="where.name"
                placeholder="请输入职级名称"
                allow-clear
              />
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
        :scroll="{ x: 'max-content' }"
      >
        <template #toolbar>
          <a-space>
            <a-button
              type="primary"
              @click="openEdit()"
              v-if="permission.includes('sys:level:add')"
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
              v-if="permission.includes('sys:level:dall')"
            >
              <template #icon>
                <delete-outlined />
              </template>
              <span>删除</span>
            </a-button>
            <!-- <a-button @click="showImport=true" v-if="permission.includes('sys:level:import')">
              <template #icon>
                <upload-outlined/>
              </template>
              <span>导入</span>
            </a-button>
            <a-button type="primary" @click="exportData" v-if="permission.includes('sys:level:export')">
              <template #icon>
                <download-outlined/>
              </template>
              <span>导出</span>
            </a-button> -->
          </a-space>
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
              v-if="permission.includes('sys:level:update')"
              >修改</a
            >
            <a-divider type="vertical" />
            <a-popconfirm
              title="确定要删除此职级吗？"
              @confirm="remove(record)"
            >
              <a
                class="ele-text-danger"
                v-if="permission.includes('sys:level:delete')"
                >删除</a
              >
            </a-popconfirm>
          </a-space>
        </template>
      </ele-pro-table>
    </a-card>
  </div>
  <!-- 编辑弹窗 -->
  <level-edit v-model:visible="showEdit" :data="current" @done="reload" />
  <!-- 导入弹窗 -->
  <level-import v-model:visible="showImport" @done="reload" />
</template>

<script>
import { mapGetters } from "vuex";
import { createVNode } from "vue";
import {
  DeleteOutlined,
  // DownloadOutlined,
  ExclamationCircleOutlined,
  PlusOutlined,
  // UploadOutlined
} from "@ant-design/icons-vue";
import LevelEdit from "./level-edit";
import LevelImport from "./level-import";

export default {
  name: "SystemLevel",
  components: {
    PlusOutlined,
    DeleteOutlined,
    // UploadOutlined,
    // DownloadOutlined,
    LevelEdit,
    LevelImport,
  },
  computed: {
    ...mapGetters(["permission"]),
  },
  data() {
    return {
      // 表格数据接口
      url: "/level/list",
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
          title: "职级名称",
          dataIndex: "name",
          align: "center",
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
          title: "排序",
          dataIndex: "sort",
          width: 100,
          align: "center",
        },
        {
          title: "创建时间",
          dataIndex: "create_time",
          align: "center",
          customRender: ({ text }) => this.$util.toDateString(text),
        },
        {
          title: "更新时间",
          dataIndex: "update_time",
          align: "center",
          customRender: ({ text }) => this.$util.toDateString(text),
        },
        {
          title: "操作",
          key: "action",
          width: 150,
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
      // 是否显示用户导入弹窗
      showImport: false,
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
        .delete("/level/delete/" + row.id)
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
        content: "确定要删除选中的职级吗?",
        icon: createVNode(ExclamationCircleOutlined),
        maskClosable: true,
        onOk: () => {
          const hide = this.$message.loading("请求中..", 0);
          this.$http
            .delete(
              "/level/delete/" + this.selection.map((d) => d.id).join(","),
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
          .get("/level/detail/" + row.id)
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
    /* 修改状态 */
    editStatus(checked, row) {
      this.$http
        .put("/level/status", { id: row.id, status: checked ? 1 : 2 })
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
    /**
     * 导出数据
     */
    exportData() {
      let info = JSON.parse(JSON.stringify(this.$refs.table.where));
      this.$http
        .get("/level/exportExcel", info)
        .then((res) => {
          let data = res.data;
          if (data.code == 0) {
            // 下载文件
            window.location.href = data.data;
            this.$message.success(res.data.msg);
          } else {
            this.$message.error(res.data.msg);
          }
        })
        .catch((e) => {
          console.log(e);
          this.$message.error("导出失败");
        });
    },
  },
};
</script>

<style scoped></style>
