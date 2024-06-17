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
            <a-form-item label="菜单名称:">
              <a-input
                v-model:value.trim="where.title"
                placeholder="请输入菜单名称"
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
        :need-page="false"
        :parse-data="parseData"
        :expand-icon-column-index="1"
        :expanded-row-keys="expandedRowKeys"
        :scroll="{ x: true }"
        @expandedRowsChange="onExpandedRowsChange"
      >
        <template #toolbar>
          <a-space>
            <a-button type="primary" @click="openEdit()">
              <template #icon>
                <plus-outlined />
              </template>
              <span>新建</span>
            </a-button>
            <a-button
              @click="expandAll"
              v-if="permission.includes('sys:menu:expand')"
              >展开全部</a-button
            >
            <a-button
              @click="foldAll"
              v-if="permission.includes('sys:menu:collapse')"
              >折叠全部</a-button
            >
          </a-space>
        </template>
        <template #type="{ record }">
          <a-tag v-if="isUrl(record.path)" color="orange">外链 </a-tag>
          <a-tag v-else-if="isUrl(record.component)" color="green">内链 </a-tag>
          <a-tag v-else :color="['blue', ''][record.type]">
            {{ ["菜单", "按钮"][record.type] }}
          </a-tag>
        </template>
        <!-- 菜单状态列 -->
        <template #status="{ record }">
          <a-badge
            :status="['success', 'error'][record.status - 1]"
            :text="['在用', '停用'][record.status - 1]"
          />
        </template>
        <!-- 操作列 -->
        <template #action="{ record }">
          <a-space>
            <a
              @click="openEdit(null, record.id)"
              v-if="permission.includes('sys:menu:add')"
              >添加</a
            >
            <a-divider type="vertical" />
            <a
              @click="openEdit(record)"
              v-if="permission.includes('sys:menu:update')"
              >修改</a
            >
            <a-divider type="vertical" />
            <a-popconfirm
              @confirm="remove(record)"
              title="确定要删除此菜单吗？"
            >
              <a
                class="ele-text-danger"
                v-if="permission.includes('sys:menu:delete')"
                >删除</a
              >
            </a-popconfirm>
          </a-space>
        </template>
      </ele-pro-table>
    </a-card>
  </div>
  <!-- 编辑弹窗 -->
  <menu-edit
    v-model:visible="showEdit"
    :data="current"
    :menu-list="menuList"
    @done="reload"
  />
</template>

<script>
import { mapGetters } from "vuex";
import { PlusOutlined } from "@ant-design/icons-vue";
import MenuEdit from "./menu-edit";

export default {
  name: "SystemMenu",
  components: { PlusOutlined, MenuEdit },
  computed: {
    ...mapGetters(["permission"]),
  },
  data() {
    return {
      // 表格数据接口
      url: "/menu/list",
      // 表格列配置
      columns: [
        {
          title: "ID",
          dataIndex: "id",
          align: "center",
          width: 80,
        },
        {
          title: "菜单标题",
          dataIndex: "title",
          align: "left",
          width: 200,
        },
        {
          title: "菜单类型",
          dataIndex: "type",
          align: "center",
          width: 100,
          slots: { customRender: "type" },
        },
        {
          title: "路由地址",
          dataIndex: "path",
          align: "center",
          width: 200,
        },
        {
          title: "组件路径",
          dataIndex: "component",
          align: "center",
          width: 200,
        },
        {
          title: "权限标识",
          dataIndex: "permission",
          align: "center",
          width: 200,
        },
        {
          title: "状态",
          dataIndex: "status",
          align: "center",
          width: 100,
          slots: { customRender: "status" },
        },
        {
          title: "排序",
          dataIndex: "sort",
          align: "center",
          width: 100,
        },
        {
          title: "可见",
          dataIndex: "hide",
          align: "center",
          width: 100,
          customRender: ({ text }) => ["是", "否"][text],
        },
        {
          title: "创建时间",
          dataIndex: "create_time",
          align: "center",
          width: 160,
          customRender: ({ text }) => this.$util.toDateString(text),
        },
        {
          title: "操作",
          key: "action",
          width: 150,
          align: "center",
          fixed: "right",
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
      // 表格展开的行
      expandedRowKeys: [],
      // 全部菜单数据
      menuList: [],
    };
  },
  methods: {
    /* 解析接口返回数据 */
    parseData(res) {
      res.data = this.$util.toTreeData(
        res.data.map((d) => {
          d.key = d.id;
          d.value = d.id;
          return d;
        }),
        "id",
        "parent_id",
      );
      if (!Object.keys(this.where).length) {
        this.menuList = res.data;
      }
      if (!this.expandedRowKeys.length) {
        this.expandAll();
      }
      return res;
    },
    /* 刷新表格 */
    reload() {
      this.$refs.table.reload({ where: this.where });
    },
    /* 重置搜索 */
    reset() {
      this.where = {};
      this.reload();
    },
    /* 打开编辑弹窗 */
    openEdit(row, parent_id) {
      if (!row) {
        // 添加
        this.current = Object.assign(
          {
            type: 0,
            hide: 0,
            parent_id: parent_id,
          },
          row,
        );
        this.showEdit = true;
      } else {
        // 编辑
        this.loading = true;
        this.$http
          .get("/menu/detail/" + row.id)
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
      if (row.children && row.children.length > 0) {
        this.$message.error("请先删除子节点");
        return;
      }
      const hide = this.$message.loading("请求中..", 0);
      this.$http
        .delete("/menu/delete/" + row.id)
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
    /* 展开全部 */
    expandAll() {
      let keys = [];
      this.$util.eachTreeData(this.menuList, (d) => {
        if (d.children && d.children.length) {
          keys.push(d.id);
        }
      });
      this.expandedRowKeys = keys;
    },
    /* 折叠全部 */
    foldAll() {
      this.expandedRowKeys = [];
    },
    /* 展开的行变化 */
    onExpandedRowsChange(expandedRows) {
      this.expandedRowKeys = expandedRows;
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
