<template>
  <div class="ele-body">
    <a-card title="基本信息" :bordered="false">
      <a-form
        ref="form"
        :model="form"
        :rules="rules"
        :label-col="{ md: { span: 6 }, sm: { span: 24 } }"
        :wrapper-col="{ md: { span: 17 }, sm: { span: 24 } }"
      >
        <a-form-item
          label="头像:"
          name="avatar"
          :label-col="{ sm: { span: 3 }, xs: { span: 6 } }"
          :wrapper-col="{ sm: { span: 21 }, xs: { span: 18 } }"
        >
          <uploadImage :limit="1" v-model:value="form.avatar" />
        </a-form-item>
        <a-row :gutter="16">
          <a-col :md="12" :sm="24" :xs="24">
            <a-form-item label="用户姓名:" name="realname">
              <a-input
                allow-clear
                :maxlength="20"
                placeholder="请输入用户姓名"
                v-model:value="form.realname"
              />
            </a-form-item>
            <a-form-item label="性别:" name="gender">
              <a-select
                allow-clear
                placeholder="请选择性别"
                v-model:value="form.gender"
              >
                <a-select-option :value="1">男</a-select-option>
                <a-select-option :value="2">女</a-select-option>
                <a-select-option :value="3">保密</a-select-option>
              </a-select>
            </a-form-item>
            <a-form-item label="邮箱:" name="email">
              <a-input
                allow-clear
                :maxlength="100"
                placeholder="请输入邮箱"
                v-model:value="form.email"
              />
            </a-form-item>
            <a-form-item label="职级:" name="level_id">
              <a-select
                v-model:value="form.level_id"
                placeholder="请选择职级"
                allow-clear
              >
                <a-select-option
                  v-for="(item, index) in levelList"
                  :key="index"
                  :value="item.id"
                >
                  {{ item.name }}
                </a-select-option>
              </a-select>
            </a-form-item>
            <a-form-item label="所属部门:" name="dept_id">
              <a-tree-select
                allow-clear
                :tree-data="deptList"
                tree-default-expand-all
                placeholder="请选择所属部门"
                v-model:value="form.dept_id"
                :dropdown-style="{ maxHeight: '360px', overflow: 'auto' }"
              />
            </a-form-item>
            <a-form-item label="所在城市:" name="city">
              <a-cascader
                v-model:value="form.city"
                :options="regions.cityData"
                placeholder="请选择所在城市"
                popup-class-name="ele-pop-wrap-higher"
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
            <a-form-item label="用户昵称:" name="nickname">
              <a-input
                allow-clear
                :maxlength="20"
                placeholder="请输入用户昵称"
                v-model:value="form.nickname"
              />
            </a-form-item>
            <a-form-item label="出生日期:" name="birthday">
              <a-date-picker
                class="ele-fluid"
                value-format="YYYY-MM-DD"
                placeholder="请选择出生日期"
                v-model:value="form.birthday"
              />
            </a-form-item>
            <a-form-item label="手机号:" name="mobile">
              <a-input
                allow-clear
                :maxlength="11"
                placeholder="请输入手机号"
                v-model:value="form.mobile"
              />
            </a-form-item>
            <a-form-item label="岗位:" name="position_id">
              <a-select
                v-model:value="form.position_id"
                placeholder="请选择岗位"
                allow-clear
              >
                <a-select-option
                  v-for="(item, index) in positionList"
                  :key="index"
                  :value="item.id"
                >
                  {{ item.name }}
                </a-select-option>
              </a-select>
            </a-form-item>
            <a-form-item label="状态" name="status">
              <a-radio-group v-model:value="form.status">
                <a-radio :value="1">正常</a-radio>
                <a-radio :value="2">禁用</a-radio>
              </a-radio-group>
            </a-form-item>
            <a-form-item label="详细地址:" name="address">
              <a-input
                v-model:value="form.address"
                placeholder="请输入详细地址"
                allow-clear
              />
            </a-form-item>
            <a-form-item label="角色:" name="roles">
              <a-select
                allow-clear
                mode="multiple"
                placeholder="请选择角色"
                v-model:value="form.roles"
              >
                <a-select-option
                  v-for="item in roleList"
                  :key="item.id"
                  :value="item.id"
                >
                  {{ item.name }}
                </a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>
        <a-form-item
          label="个人简介:"
          :label-col="{ sm: { span: 3 }, xs: { span: 6 } }"
          :wrapper-col="{ sm: { span: 21 }, xs: { span: 18 } }"
        >
          <a-textarea
            :rows="3"
            :maxlength="200"
            placeholder="请输入个人简介"
            v-model:value="form.intro"
          />
        </a-form-item>
        <a-form-item :wrapper-col="{ md: { offset: 3 } }">
          <a-button type="primary" @click="save" :loading="loading">
            {{ loading ? "保存中.." : "保存更改" }}
          </a-button>
        </a-form-item>
      </a-form>
    </a-card>
  </div>
</template>

<script>
import { setPageTab } from "@/utils/page-tab-util";
import validate from "ele-admin-pro/packages/validate";
import uploadImage from "@/components/uploadImage";
import regions from "@/assets/regions.js";

export default {
  name: "SystemUserInfo",
  data() {
    return {
      // 省市区数据
      regions: regions,
      form: {},
      // 表单验证规则
      rules: {
        realname: [
          {
            required: true,
            message: "请输入用户姓名",
            type: "string",
            trigger: "blur",
          },
        ],
        nickname: [
          { required: true, message: "请输入用户名", trigger: "blur" },
        ],
        gender: [
          {
            required: true,
            message: "请选择性别",
            type: "number",
            trigger: "blur",
          },
        ],
        birthday: [
          {
            required: true,
            message: "请选择出生日期",
            type: "string",
            trigger: "blur",
          },
        ],
        level_id: [
          {
            required: true,
            message: "请选择职级",
            type: "number",
            trigger: "blur",
          },
        ],
        position_id: [
          {
            required: true,
            message: "请选择岗位",
            type: "number",
            trigger: "blur",
          },
        ],
        dept_id: [
          {
            required: true,
            message: "请选择部门",
            type: "number",
            trigger: "blur",
          },
        ],
        status: [
          {
            required: true,
            message: "请选择状态",
            type: "number",
            trigger: "blur",
          },
        ],
        city: [
          {
            required: true,
            message: "请选择省市区",
            type: "array",
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
        roles: [
          {
            required: true,
            message: "请选择角色",
            type: "array",
            trigger: "blur",
          },
        ],
        email: [
          {
            pattern: validate.email,
            message: "邮箱格式不正确",
            type: "string",
            trigger: "blur",
          },
        ],
        password: [
          {
            required: true,
            pattern: /^[\S]{5,18}$/,
            message: "密码必须为5-18位非空白字符",
            type: "string",
            trigger: "blur",
          },
        ],
        mobile: [
          {
            pattern: validate.phone,
            message: "手机号格式不正确",
            type: "string",
            trigger: "blur",
          },
        ],
      },
      // 提交状态
      loading: false,
      // 是否是修改
      isUpdate: false,
      // 角色列表
      roleList: [],
      // 职级列表
      levelList: [],
      // 岗位列表
      positionList: [],
      // 部门列表
      deptList: [],
    };
  },
  components: { uploadImage },
  mounted() {
    this.query(this.$route.query.id);
    this.queryRoles(); // 查询角色列表
    this.queryLevelList(); // 查询职级列表
    this.queryPositionList(); // 查询岗位列表
    this.queryDeptList(); // 查询部门列表
  },
  methods: {
    /* 查询用户信息 */
    query(id) {
      if (!id) {
        return;
      }
      this.loading = true;
      this.$http
        .get("/user/detail/" + id)
        .then((res) => {
          this.loading = false;
          if (res.data.code === 0) {
            this.form = Object.assign({}, res.data.data, {});
            this.isUpdate = true;
            // 修改页签标题
            setPageTab({
              fullPath: this.$route.fullPath,
              title: this.form.realname + "的详情",
            });
          } else {
            this.$message.error(res.data.msg);
          }
        })
        .catch((e) => {
          this.loading = false;
          this.$message.error(e.message);
        });
    },
    /* 保存编辑 */
    save() {
      this.$refs.form
        .validate()
        .then(() => {
          this.loading = true;
          this.$http[this.isUpdate ? "put" : "post"](
            this.isUpdate ? "/user/update" : "/user/add",
            this.form,
          )
            .then((res) => {
              this.loading = false;
              if (res.data.code === 0) {
                this.$message.success(res.data.msg);
                if (!this.isUpdate) {
                  this.form = {};
                }
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
    /* 查询角色列表 */
    queryRoles() {
      this.$http
        .get("/role/getRoleList")
        .then((res) => {
          if (res.data.code === 0) {
            this.roleList = res.data.data;
          } else {
            this.$message.error(res.data.msg);
          }
        })
        .catch((e) => {
          this.$message.error(e.message);
        });
    },
    /**
     * 获取职级列表
     */
    queryLevelList() {
      this.$http
        .get("/level/getLevelList")
        .then((res) => {
          if (res.data.code === 0) {
            this.levelList = res.data.data;
          } else {
            this.$message.error(res.data.msg);
          }
        })
        .catch((e) => {
          this.$message.error(e.message);
        });
    },
    /**
     * 获取岗位列表
     */
    queryPositionList() {
      this.$http
        .get("/position/getPositionList")
        .then((res) => {
          if (res.data.code === 0) {
            this.positionList = res.data.data;
          } else {
            this.$message.error(res.data.msg);
          }
        })
        .catch((e) => {
          this.$message.error(e.message);
        });
    },
    /**
     * 获取部门列表
     */
    queryDeptList() {
      this.$http
        .get("/dept/getDeptList")
        .then((res) => {
          if (res.data.code === 0) {
            this.deptList = this.$util.toTreeData(
              res.data.data.map((d) => {
                d.key = d.id;
                d.value = d.id;
                d.title = d.name;
                return d;
              }),
              "id",
              "pid",
            );
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
    $route() {
      this.query(this.$route.query.id);
    },
  },
};
</script>

<style scoped></style>
