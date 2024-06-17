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
            <a-form-item label="用户账号:">
              <a-input
                v-model:value.trim="where.username"
                placeholder="请输入用户账号"
                allow-clear
              />
            </a-form-item>
          </a-col>
          <a-col :lg="6" :md="12" :sm="24" :xs="24">
            <a-form-item label="用户姓名:">
              <a-input
                v-model:value.trim="where.realname"
                placeholder="请输入用户姓名"
                allow-clear
              />
            </a-form-item>
          </a-col>
          <a-col :lg="6" :md="12" :sm="24" :xs="24">
            <a-form-item label="性别:">
              <a-select
                v-model:value="where.gender"
                placeholder="请选择性别"
                allow-clear
              >
                <a-select-option :value="1">男</a-select-option>
                <a-select-option :value="2">女</a-select-option>
                <a-select-option :value="3">保密</a-select-option>
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
        :scroll="{ x: 'max-content' }"
      >
        <template #toolbar>
          <a-space>
            <a-button
              type="primary"
              @click="openEdit()"
              v-if="permission.includes('sys:user:add')"
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
              v-if="permission.includes('sys:user:dall')"
            >
              <template #icon>
                <delete-outlined />
              </template>
              <span>删除</span>
            </a-button>
          </a-space>
        </template>
        <template #realname="{ record }">
          <router-link :to="'/system/user/info?id=' + record.id">
            {{ record.realname }}
          </router-link>
        </template>
        <!-- 性别列 -->
        <template #gender="{ record }">
          <a-tag :color="['green', 'orange', 'red'][record.gender - 1]">
            {{ ["男", "女", "保密"][record.gender - 1] }}
          </a-tag>
        </template>
        <!-- 头像列 -->
        <template #avatar="{ record }">
          <a-image :width="35" :src="record.avatar" />
        </template>
        <!-- 角色列 -->
        <template #roles="{ record }">
          <a-tag
            v-for="(item, index) in record.roleList"
            :key="index"
            color="blue"
          >
            {{ item.name }}
          </a-tag>
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
              v-if="permission.includes('sys:user:update')"
              >修改</a
            >
            <a-divider type="vertical" />
            <a
              @click="resetPsw(record)"
              v-if="permission.includes('sys:user:resetPwd')"
              >重置密码</a
            >
            <a-divider type="vertical" />
            <a-popconfirm
              title="确定要删除此用户吗？"
              @confirm="remove(record)"
            >
              <a
                class="ele-text-danger"
                v-if="permission.includes('sys:user:delete')"
                >删除</a
              >
            </a-popconfirm>
          </a-space>
        </template>
      </ele-pro-table>
    </a-card>
  </div>
  <!-- 编辑弹窗 -->
  <user-edit v-model:visible="showEdit" :data="current" @done="reload" />
</template>

<script>
import { mapGetters } from "vuex";
import { createVNode } from "vue";
import {
  DeleteOutlined,
  ExclamationCircleOutlined,
  PlusOutlined,
} from "@ant-design/icons-vue";
import UserEdit from "./user-edit";

export default {
  name: "SystemUser",
  components: {
    PlusOutlined,
    DeleteOutlined,
    UserEdit,
  },
  computed: {
    ...mapGetters(["permission"]),
  },
  data() {
    return {
      // 表格数据接口
      url: "/user/list",
      // 表格列配置
      columns: [
        {
          key: "index",
          width: 48,
          customRender: ({ index }) => this.$refs.table.tableIndex + index,
        },
        {
          title: "用户账号",
          dataIndex: "username",
          align: "center",
        },
        {
          title: "用户名",
          dataIndex: "realname",
          align: "center",
          slots: { customRender: "realname" },
        },
        {
          title: "性别",
          dataIndex: "gender",
          align: "center",
          slots: { customRender: "gender" },
        },
        {
          title: "头像",
          dataIndex: "avatar",
          align: "center",
          slots: { customRender: "avatar" },
        },
        {
          title: "手机号",
          dataIndex: "mobile",
          align: "center",
        },
        {
          title: "角色",
          key: "roles",
          slots: { customRender: "roles" },
        },
        {
          title: "状态",
          dataIndex: "status",
          sorter: true,
          width: 100,
          align: "center",
          slots: { customRender: "status" },
        },
        {
          title: "职级",
          dataIndex: "level_name",
          align: "center",
        },
        {
          title: "岗位",
          dataIndex: "position_name",
          align: "center",
        },
        {
          title: "部门",
          dataIndex: "dept_name",
          align: "center",
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
          width: 200,
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
        .delete("/user/delete/" + row.id)
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
        content: "确定要删除选中的用户吗?",
        icon: createVNode(ExclamationCircleOutlined),
        maskClosable: true,
        onOk: () => {
          const hide = this.$message.loading("请求中..", 0);
          this.$http
            .delete("/user/delete/" + this.selection.map((d) => d.id).join(","))
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
        this.current = null;
        this.showEdit = true;
      } else {
        // 编辑
        this.loading = true;
        this.$http
          .get("/user/detail/" + row.id)
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
    /* 重置用户密码 */
    resetPsw(row) {
      this.$confirm({
        title: "提示",
        content: '确定要重置此用户的密码为"123456"吗?',
        icon: createVNode(ExclamationCircleOutlined),
        maskClosable: true,
        onOk: () => {
          const hide = this.$message.loading("请求中..", 0);
          this.$http
            .put("/user/resetPwd", { id: row.id })
            .then((res) => {
              hide();
              if (res.data.code === 0) {
                this.$message.success(res.data.msg);
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
    /* 修改用户状态 */
    editStatus(checked, row) {
      this.$http
        .put("/user/status", { id: row.id, status: checked ? 1 : 2 })
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
