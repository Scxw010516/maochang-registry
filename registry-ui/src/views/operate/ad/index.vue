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
            <a-form-item label="广告标题:">
              <a-input
                v-model:value.trim="where.title"
                placeholder="请输入广告标题"
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
        :scroll="{ x: true }"
      >
        <template #toolbar>
          <a-space>
            <a-button
              type="primary"
              @click="openEdit()"
              v-if="permission.includes('sys:ad:add')"
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
              v-if="permission.includes('sys:ad:dall')"
            >
              <template #icon>
                <delete-outlined />
              </template>
              <span>删除</span>
            </a-button>
          </a-space>
        </template>
        <!-- 广告类型列 -->
        <template #type="{ record }">
          <a-tag :color="['blue', 'green', 'orange', 'pink'][record.type - 1]">
            {{ ["图片", "文字", "视频", "推荐"][record.type - 1] }}
          </a-tag>
        </template>
        <!-- 广告封面列 -->
        <template #cover="{ record }">
          <a-image :width="35" :src="record.cover" />
        </template>
        <!-- 状态列 -->
        <template #status="{ text, record }">
          <a-switch
            :checked="text === 1"
            @change="(checked) => editStatus(checked, record)"
          />
        </template>
        <!-- 广告尺寸 -->
        <template #size="{ record }">
          {{ record.width }} x {{ record.height }}
        </template>
        <!-- 操作列 -->
        <template #action="{ record }">
          <a-space>
            <a
              @click="openEdit(record)"
              v-if="permission.includes('sys:ad:update')"
              >修改</a
            >
            <a-divider type="vertical" />
            <a-popconfirm
              title="确定要删除此广告吗？"
              @confirm="remove(record)"
            >
              <a
                class="ele-text-danger"
                v-if="permission.includes('sys:ad:delete')"
                >删除</a
              >
            </a-popconfirm>
          </a-space>
        </template>
      </ele-pro-table>
    </a-card>
  </div>
  <!-- 编辑弹窗 -->
  <ad-edit
    v-model:visible="showEdit"
    :data="current"
    :sort-list="sortList"
    @done="reload"
  />
</template>

<script>
import { mapGetters } from "vuex";
import { createVNode } from "vue";
import {
  DeleteOutlined,
  ExclamationCircleOutlined,
  PlusOutlined,
} from "@ant-design/icons-vue";
import AdEdit from "./ad-edit";

export default {
  name: "SystemAd",
  components: {
    PlusOutlined,
    DeleteOutlined,
    AdEdit,
  },
  computed: {
    ...mapGetters(["permission"]),
  },
  data() {
    return {
      // 表格数据接口
      url: "/ad/list",
      // 表格列配置
      columns: [
        {
          key: "index",
          width: 48,
          customRender: ({ index }) => this.$refs.table.tableIndex + index,
        },
        {
          title: "广告标题",
          dataIndex: "title",
          align: "center",
          width: 200,
        },
        {
          title: "所属广告位",
          dataIndex: "sort_desc",
          align: "center",
          width: 200,
        },
        {
          title: "广告类型",
          dataIndex: "type",
          align: "center",
          width: 100,
          slots: { customRender: "type" },
        },
        {
          title: "广告封面",
          dataIndex: "cover",
          align: "center",
          width: 100,
          slots: { customRender: "cover" },
        },
        {
          title: "广告状态",
          dataIndex: "status",
          width: 100,
          align: "center",
          slots: { customRender: "status" },
        },
        {
          title: "广告地址",
          dataIndex: "url",
          align: "center",
          width: 200,
        },
        {
          title: "广告尺寸",
          dataIndex: "size",
          align: "center",
          width: 100,
          slots: { customRender: "size" },
        },
        {
          title: "开始时间",
          dataIndex: "start_time",
          align: "center",
          width: 160,
          customRender: ({ text }) => this.$util.toDateString(text),
        },
        {
          title: "结束时间",
          dataIndex: "end_time",
          align: "center",
          width: 160,
          customRender: ({ text }) => this.$util.toDateString(text),
        },
        {
          title: "排序",
          dataIndex: "sort",
          width: 100,
          align: "center",
        },
        {
          title: "浏览量",
          dataIndex: "click",
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
      // 广告位列表
      sortList: [],
    };
  },
  mounted() {
    // 查询广告位列表
    this.getAdSortList();
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
        .delete("/ad/delete/" + row.id)
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
        content: "确定要删除选中的广告吗?",
        icon: createVNode(ExclamationCircleOutlined),
        maskClosable: true,
        onOk: () => {
          const hide = this.$message.loading("请求中..", 0);
          this.$http
            .delete("/ad/delete/" + this.selection.map((d) => d.id).join(","))
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
          .get("/ad/detail/" + row.id)
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
    /* 修改广告状态 */
    editStatus(checked, row) {
      this.$http
        .put("/ad/status", { id: row.id, status: checked ? 1 : 2 })
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
     * 查询广告位列表
     */
    getAdSortList() {
      this.$http
        .get("/adsort/getAdSortList")
        .then((res) => {
          if (res.data.code === 0) {
            this.sortList = res.data.data;
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
