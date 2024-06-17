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
            <a-form-item label="城市名称:">
              <a-input
                v-model:value.trim="where.name"
                placeholder="请输入城市名称"
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
              v-if="permission.includes('sys:city:add')"
            >
              <template #icon>
                <plus-outlined />
              </template>
              <span>新建</span>
            </a-button>
          </a-space>
        </template>
        <template #level="{ record }">
          <a-tag :color="['blue', 'green', 'orange'][record.level - 1]">
            {{ ["省份", "城市", "县区"][record.level - 1] }}
          </a-tag>
        </template>
        <template #action="{ record }">
          <a-space>
            <a
              @click="openEdit(record)"
              v-if="permission.includes('sys:city:update')"
              >修改</a
            >
            <a-divider type="vertical" />
            <a-popconfirm
              @confirm="remove(record)"
              title="确定要删除此城市吗？"
            >
              <a
                class="ele-text-danger"
                v-if="permission.includes('sys:city:delete')"
                >删除</a
              >
            </a-popconfirm>
          </a-space>
        </template>
      </ele-pro-table>
    </a-card>
  </div>
  <!-- 编辑弹窗 -->
  <city-edit
    v-model:visible="showEdit"
    :data="current"
    :city-list="cityList"
    @done="reload"
  />
</template>

<script>
import { mapGetters } from "vuex";
import { PlusOutlined } from "@ant-design/icons-vue";
import CityEdit from "./city-edit";

export default {
  name: "SystemCity",
  emits: ["close", "update:visible"],
  components: { PlusOutlined, CityEdit },
  computed: {
    ...mapGetters(["permission"]),
    // 请求地址
    url() {
      return "/city/list?pid=" + this.cityId;
    },
  },
  props: {
    // 城市ID
    cityId: Number,
  },
  data() {
    return {
      // 表格列配置
      columns: [
        {
          key: "index",
          title: "编号",
          dataIndex: "index",
          width: 48,
          align: "center",
          customRender: ({ index }) => index + 1,
        },
        {
          title: "城市名称",
          dataIndex: "name",
          align: "center",
          width: 150,
        },
        {
          title: "城市区号",
          dataIndex: "city_code",
          align: "center",
          width: 100,
        },
        {
          title: "行政编码",
          dataIndex: "area_code",
          align: "center",
          width: 150,
        },
        {
          title: "父级编码",
          dataIndex: "parent_code",
          align: "center",
          width: 150,
        },
        {
          title: "城市等级",
          dataIndex: "level",
          align: "center",
          width: 100,
          slots: { customRender: "level" },
        },
        {
          title: "邮政编码",
          dataIndex: "zip_code",
          align: "center",
          width: 100,
        },
        {
          title: "城市简称",
          dataIndex: "short_name",
          align: "center",
          width: 100,
        },
        {
          title: "城市拼音",
          dataIndex: "pinyin",
          align: "center",
          width: 100,
        },
        {
          title: "经度",
          dataIndex: "lng",
          align: "center",
          width: 100,
        },
        {
          title: "纬度",
          dataIndex: "lat",
          align: "center",
          width: 100,
        },
        {
          title: "创建时间",
          dataIndex: "create_time",
          sorter: true,
          align: "center",
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
      // 全部城市数据
      cityList: [],
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
        this.cityList = res.data;
      }
      if (!this.expandedRowKeys.length) {
        this.expandAll();
      }
      return res;
    },
    /* 刷新表格 */
    reload() {
      this.$refs.table.reload();
    },
    /* 重置搜索 */
    reset() {
      this.where = {};
      this.$nextTick(() => {
        this.reload();
      });
    },
    /* 打开编辑弹窗 */
    openEdit(row) {
      if (!row) {
        // 添加
        this.current = Object.assign(
          {
            level: 3,
            pid: this.cityId,
          },
          row,
        );
        this.showEdit = true;
      } else {
        // 编辑
        this.loading = true;
        this.$http
          .get("/city/detail/" + row.id)
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
        .post("/city/delete/" + row.id)
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
      this.$util.eachTreeData(this.cityList, (d) => {
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
