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
            <a-form-item label="栏目名称:">
              <a-input
                v-model:value.trim="where.title"
                placeholder="请输入栏目名称"
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
        :scroll="{ x: 'max-content' }"
        @expandedRowsChange="onExpandedRowsChange"
      >
        <template #toolbar>
          <a-space>
            <a-button
              type="primary"
              @click="openEdit()"
              v-if="permission.includes('sys:itemcate:add')"
            >
              <template #icon>
                <plus-outlined />
              </template>
              <span>新建</span>
            </a-button>
            <a-button
              @click="expandAll"
              v-if="permission.includes('sys:itemcate:expand')"
              >展开全部</a-button
            >
            <a-button
              @click="foldAll"
              v-if="permission.includes('sys:itemcate:collapse')"
              >折叠全部</a-button
            >
          </a-space>
        </template>
        <!-- 有无封面列 -->
        <template #is_cover="{ record }">
          <a-tag :color="['green', 'orange'][record.is_cover - 1]">
            {{ ["有封面", "无封面"][record.is_cover - 1] }}
          </a-tag>
        </template>
        <!-- 封面列 -->
        <template #cover="{ record }">
          <a-image :width="35" :src="record.cover" />
        </template>
        <!-- 操作列 -->
        <template #action="{ record }">
          <a-space>
            <a
              @click="openEdit(null, record.id)"
              v-if="permission.includes('sys:itemcate:addz')"
              >添加</a
            >
            <a-divider type="vertical" />
            <a
              @click="openEdit(record)"
              v-if="permission.includes('sys:itemcate:update')"
              >修改</a
            >
            <a-divider type="vertical" />
            <a-popconfirm
              @confirm="remove(record)"
              title="确定要删除此栏目吗？"
            >
              <a
                class="ele-text-danger"
                v-if="permission.includes('sys:itemcate:delete')"
                >删除</a
              >
            </a-popconfirm>
          </a-space>
        </template>
      </ele-pro-table>
    </a-card>
  </div>
  <!-- 编辑弹窗 -->
  <item-cate-edit
    v-model:visible="showEdit"
    :data="current"
    :cate-list="cateList"
    @done="reload"
  />
</template>

<script>
import { mapGetters } from "vuex";
import { PlusOutlined } from "@ant-design/icons-vue";
import ItemCateEdit from "./itemcate-edit";

export default {
  name: "SystemItemCate",
  components: { PlusOutlined, ItemCateEdit },
  computed: {
    ...mapGetters(["permission"]),
  },
  data() {
    return {
      // 表格数据接口
      url: "/itemcate/list",
      // 表格列配置
      columns: [
        {
          key: "index",
          dataIndex: "index",
          width: 48,
          align: "center",
          customRender: ({ index }) => index + 1,
        },
        {
          title: "栏目名称",
          dataIndex: "name",
          width: 200,
          align: "left",
        },
        {
          title: "所属站点",
          dataIndex: "item_name",
          align: "center",
          width: 100,
        },
        {
          title: "拼音(全)",
          dataIndex: "pinyin",
          align: "center",
          width: 150,
        },
        {
          title: "拼音(简)",
          dataIndex: "code",
          align: "center",
          width: 100,
        },
        {
          title: "有无封面",
          dataIndex: "is_cover",
          align: "center",
          width: 100,
          slots: { customRender: "is_cover" },
        },
        {
          title: "封面",
          dataIndex: "cover",
          align: "center",
          width: 100,
          slots: { customRender: "cover" },
        },
        {
          title: "排序号",
          dataIndex: "sort",
          align: "center",
          sorter: true,
          width: 100,
        },
        {
          title: "备注",
          dataIndex: "sort",
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
      // 全部栏目数据
      cateList: [],
    };
  },
  methods: {
    /* 解析接口返回数据 */
    parseData(res) {
      res.data = this.$util.toTreeData(
        res.data.map((d) => {
          d.key = d.id;
          d.value = d.id;
          d.title = d.name;
          return d;
        }),
        "id",
        "pid",
      );
      if (!Object.keys(this.where).length) {
        this.cateList = res.data;
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
    openEdit(row, parentId) {
      if (!row) {
        // 添加
        this.current = Object.assign(
          {
            pid: parentId,
          },
          row,
        );
        this.showEdit = true;
      } else {
        // 编辑
        this.loading = true;
        this.$http
          .get("/itemcate/detail/" + row.id)
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
        .delete("/itemcate/delete/" + row.id)
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
      this.$util.eachTreeData(this.cateList, (d) => {
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
  },
};
</script>

<style scoped></style>
