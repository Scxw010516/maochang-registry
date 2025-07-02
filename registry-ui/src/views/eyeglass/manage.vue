<template>
  <div
    v-if="!tryonPageState.showTryOnPage"
    style="
      background-color: #ffffff;
      border-radius: 12px 0px 0px 12px;
      height: 100%;
    "
  >
    <!-- 高级筛选 -->
    <div>
      <p
        style="
          margin: 0;
          padding: 40px 39.5px;
          font-size: 30px;
          font-weight: bold;
        "
      >
        高级筛选
      </p>
      <a-col style="margin: 0 49px 15px">
        <a-form
          ref="searchFormRef"
          :model="searchFormState"
          name="search"
          class="search-form"
          :labelCol="{ span: 6, offset: 0 }"
          :wrapperCol="{ span: 18, offset: 0 }"
          labelAlign="left"
        >
          <a-row :gutter="[200, 20]" style="margin-right: -48px">
            <a-col :span="8">
              <a-form-item
                name="sku"
                label="SKU"
                :labelCol="{ span: 6, offset: 0 }"
                :wrapperCol="{ span: 18, offset: 0 }"
                labelAlign="left"
              >
                <a-input
                  style="
                    border-radius: 9px;
                    padding-left: 15px;
                    border-color: #999999;
                  "
                  v-model:value="searchFormState.sku"
                  placeholder="请输入sku"
                ></a-input>
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item
                name="brand"
                label="品牌"
                :labelCol="{ span: 6, offset: 0 }"
                :wrapperCol="{ span: 18, offset: 0 }"
                labelAlign="left"
              >
                <a-auto-complete
                  v-model:value="searchFormState.brand"
                  placeholder="请输入品牌"
                  :options="options.brand_options"
                  :filter-option="filterOption"
                />
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item
                name="model_type"
                label="型号"
                :labelCol="{ span: 6, offset: 0 }"
                :wrapperCol="{ span: 18, offset: 0 }"
                labelAlign="left"
              >
                <a-auto-complete
                  v-model:value="searchFormState.model_type"
                  placeholder="请输入型号"
                  :options="options.model_type_options"
                  :filter-option="filterOption"
                />
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item
                label="价格"
                :labelCol="{ span: 6, offset: 0 }"
                :wrapperCol="{ span: 18, offset: 0 }"
                labelAlign="left"
              >
                <a-input-group
                  compact
                  style="
                    display: flex;
                    align-items: center;
                    justify-content: center;
                  "
                >
                  <a-form-item name="searchMinPrice" style="width: 100%">
                    <a-input
                      v-model:value="searchFormState.searchMinPrice"
                      :precision="2"
                      :controls="false"
                      style="
                        border-color: #999999;
                        border-radius: 9px 0 0 9px;
                        border-right-width: 0;
                        padding-left: 15px;
                      "
                    >
                    </a-input>
                  </a-form-item>
                  <a-input
                    style="
                      width: 30px;
                      border-radius: 0;
                      pointer-events: none;
                      border-color: #999999;
                      border-left-color: transparent;
                      border-right-color: transparent;
                      background-color: #ffffff;
                      height: 30px;
                    "
                    placeholder="-"
                    :controls="false"
                    disabled
                  />
                  <a-form-item name="searchMaxPrice" style="width: 100%">
                    <a-input
                      v-model:value="searchFormState.searchMaxPrice"
                      :precision="2"
                      :controls="false"
                      style="
                        border-color: #999999;
                        border-radius: 0 9px 9px 0;
                        border-left-width: 0;
                      "
                    >
                    </a-input>
                  </a-form-item>
                </a-input-group>
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item
                name="material"
                label="材质"
                :labelCol="{ span: 6, offset: 0 }"
                :wrapperCol="{ span: 18, offset: 0 }"
                labelAlign="left"
              >
                <a-select
                  v-model:value="searchFormState.material"
                  mode="multiple"
                  :max-tag-count="1"
                  :max-tag-text-length="5"
                  placeholder="请选择材质"
                  :options="options.material_options"
                />
              </a-form-item>
            </a-col>
            <a-col :span="8" style="display: flex; justify-content: end">
              <a-button
                style="
                  margin: 0 22px;
                  border-color: #999999;
                  border-radius: 8px;
                "
                @click="onClickReset"
                >重置
              </a-button>
              <a-button
                type="primary"
                style="background-color: #8675ff; border-radius: 8px"
                @click="onClickSearch"
                >查询
              </a-button>
            </a-col>
          </a-row>
        </a-form>
      </a-col>
    </div>

    <span style="margin-left: 8px">
      <template v-if="hasSelected || !hasSelected">
        {{ `已选择 ${tableSelectionState.selectedRowKeys.length} 个条目` }}
        <a-button
          style="margin-bottom: 10px"
          :disabled="!hasSelected"
          danger
          @click="onClickDeleteAllSelected"
          >全部删除</a-button
        >
      </template>
    </span>
    <!-- table -->
    <div>
      <!-- 表格 -->
      <a-table
        :data-source="dataSource"
        :row-key="(record: any) => record.id"
        :columns="columns"
        :pagination="pagination"
        :loading="loading"
        :scroll="{ y: 600 }"
        @change="handleTableChange"
        :row-selection="{
          selectedRowKeys: tableSelectionState.selectedRowKeys,
          onChange: onSelectChange,
        }"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'operation'">
            <span>
              <a-space>
                <a-button danger @click="onClickDelete(record.id)"
                  >删除</a-button
                >
              </a-space>
            </span>
          </template>
          <template v-if="column.key === 'tryon'">
            <span>
              <a-button type="primary" ghost @click="onClickTryOn(record.id)">{{
                getTryOnStateLabel(record.id)
              }}</a-button>
            </span>
          </template>
        </template>
      </a-table>
    </div>
  </div>
  <!-- 试戴详情页面 -->
  <div
    v-if="tryonPageState.showTryOnPage"
    style="
      background-color: #ffffff;
      border-radius: 12px 0px 0px 12px;
      height: 100%;
    "
  >
    <tryon-page :id="tryonPageState.id" />
  </div>
</template>

<script lang="ts" setup>
//#####################################第三方库及定义类初始化#####################################
import {
  computed,
  onMounted,
  ref,
  reactive,
  UnwrapRef,
  createVNode,
  h,
  watch,
  onBeforeUnmount,
} from "vue";
import { message, Modal } from "ant-design-vue";
import { ExclamationCircleOutlined } from "@ant-design/icons-vue";
// import { useRouter } from "vue-router";
import { useOptionStore, useUserStore, useStateStore } from "@/stores/store";
import axios from "@/config/axios-config";
import { usePagination } from "vue-request";
import { Key } from "ant-design-vue/lib/_util/type";

import { initFormOptions } from "./utils";
import { Item } from "ant-design-vue/es/menu";
import tryonPage from "./tryon.vue";
//#########################################参数初始化###########################################
// const router = useRouter();
const options = useOptionStore();
const user = useUserStore();
const state = useStateStore();
// 定时器，用于定时刷新表格
let timer: number;
// 父组件传递参数接口
interface managePageProps {
  goToScan: () => void; //跳转到镜架管理页面
}
// 父组件传递参数实例
const props = withDefaults(defineProps<managePageProps>(), {
  goToScan: () => {},
});

// 镜架表格栏目
const columns = [
  {
    title: "SKU",
    dataIndex: "sku",
    sorter: true,
    showSorterTooltip: false,
    key: "sku",
  },
  {
    title: "品牌",
    dataIndex: "brand",
    key: "brand",
  },
  {
    title: "型号",
    dataIndex: "model_type",
    key: "model_type",
  },
  {
    title: "价格",
    dataIndex: "price",
    sorter: true,
    showSorterTooltip: false,
    key: "price",
  },
  {
    title: "材质",
    dataIndex: "material",
    key: "material",
  },
  {
    title: "更新时间",
    dataIndex: "update_time",
    sorter: true,
    showSorterTooltip: false,
    key: "update_time",
  },
  {
    title: "操作",
    key: "operation",
  },
  {
    title: "试戴",
    key: "tryon",
  },
  {
    title: "启用状态",
    key: "is_active",
  },
];
// 镜架table请求API携带参数格式
type getAllEyeglassFrameEntryAPIParams = {
  page: number;
  pageSize: number;
  sortField?: string;
  sortOrder?: number;
  sku?: string;
  brand?: string;
  model_type?: string;
  searchMinPrice?: number;
  searchMaxPrice?: number;
  material?: number[];
  [key: string]: any;
};
// 镜架table请求API数据格式
type getAllEyeglassFrameEntryAPIResult = {
  data: {
    id: number;
    sku: string;
    brand: string;
    model_type: string;
    price: number;
    material: number;
    update_time: string;
    aiface_tryon_state: number; // 试戴状态
    is_active: number; // 启用状态
  }[];
  count: number;
};

// 镜架试戴状态接口
interface try_on_state {
  id: number;
  aiface_tryon_state: number;
  is_active: number;
}

// 镜架试戴状态数组
const tryOnStates = ref<try_on_state[]>([]);

// 镜架查询表单实例
const searchFormRef = ref();

// 定义SearchForm接口
interface searchForm {
  sku?: string;
  brand?: string;
  model_type?: string;
  searchMinPrice?: number | undefined;
  searchMaxPrice?: number | undefined;
  material?: number[];
}

// 镜架搜索数据表单数据
const searchFormState = reactive<searchForm>({
  sku: "",
  brand: "",
  model_type: "",
  searchMinPrice: undefined,
  searchMaxPrice: undefined,
  material: [],
});

// select和autocompe下拉框选项接口定义
interface Option {
  value: string;
  label: string;
}
// 镜架表格项选择
const tableSelectionState = reactive<{
  selectedRowKeys: Key[]; // 选中的表格项
}>({
  selectedRowKeys: [],
});

// 表格项是否有选中的标识符
const hasSelected = computed(
  () => tableSelectionState.selectedRowKeys.length > 0,
); // 是否有选中表格项

// 试戴详情页面相关
const tryonPageState = reactive<{
  showTryOnPage: boolean; // 试戴弹窗可见状态
  id: number;
}>({
  showTryOnPage: false,
  id: 0,
});

// #########################################生命周期函数############################################
// 生命周期钩子：组件挂载完成后执行
onMounted(async () => {
  // 判断状态管理store中是否有需要查询的sku
  if (state.searchSku) {
    // 将store中的sku赋值给searchFormState
    searchFormState.sku = state.searchSku;
    // 清空store中的sku
    state.searchSku = "";
    // 通过searchFormState的sku请求Table
    run({
      page: 1,
      pageSize: 10,
      ...searchFormFilter.value,
    });
  } else {
    // 通过searchFormState请求Table
    run({
      page: 1,
      pageSize: 10,
    });
  }
  timer = setInterval(() => {
    // 刷新页面
    setTimeout(() => {
      refreshTryOnStates();
    }, 0);
  }, 5000);
});

// 生命钩子函数：组件卸载前执行
onBeforeUnmount(() => {
  clearInterval(timer);
});

// #########################################静态功能函数定义#########################################
// 功能函数：selct和auto-complete的输入框和option不区分大小写
const filterOption = (input: string, option: Option) => {
  // 判断option的value是否为空
  if (!option.value) {
    return false;
  } else {
    // selct和auto-complete的输入框和option不区分大小写
    return option.value.toUpperCase().indexOf(input.toUpperCase()) >= 0;
  }
};

// 功能函数:获取Table数据
const getTableData = (params: getAllEyeglassFrameEntryAPIParams) => {
  return axios
    .get<getAllEyeglassFrameEntryAPIResult>(
      "/glassmanagement/api/get-all-eyeglassframes_entrys",
      { params },
    )
    .catch((error) => {
      console.log(error);
    });
};

// 功能函数:Table分页逻辑与数据请求
const {
  data, // 返回数据
  run, // 请求数据
  loading, // 加载状态
  current, // 当前页码
  pageSize, // 每页条数
  total, // 总条数
} = usePagination(getTableData, {
  pagination: {
    currentKey: "page",
    pageSizeKey: "pageSize",
    totalKey: "data.count",
  },
});

// 功能函数:处理Table请求的返回数据
const dataSource = computed(() => {
  if (data.value?.data.data == null) {
    return [];
  } else {
    // 处理Table请求的返回数据
    return data.value?.data.data.map((item) => ({
      id: item.id,
      sku: item.sku,
      brand: item.brand,
      model_type: item.model_type,
      price: item.price,
      update_time: item.update_time,
      // 将material字段转化为对应的Label
      material:
        options.material_options?.find(
          (option) => option.value === item.material,
        )?.label || item.material,
    }));
  }
});

// 功能函数:处理Table的pagination
const pagination = computed(() => ({
  total: total.value,
  current: current.value,
  pageSize: pageSize.value,
  showSizeChanger: true,
  pageSizeOptions: ["10", "20", "50", "100"],
  showQuickJumper: true,
  showTotal: (total: number) => `共 ${total} 条`,
  position: ["bottomCenter"],
}));

// 将search表单项加入请求参数列表
const searchFormFilter = computed(() => {
  // 初始化空的searchForm
  const searchForm = {} as searchForm;
  // 分别判断searchFormState的表单数据是否为空，不为空则添加到searchForm
  if (searchFormState.sku) {
    // 将sku的键值对加入searchForm
    searchForm.sku = searchFormState.sku;
  }
  if (searchFormState.brand) {
    // 将brand的键值对加入searchForm
    searchForm.brand = searchFormState.brand;
  }
  if (searchFormState.model_type) {
    // 将model_type的键值对加入searchForm
    searchForm.model_type = searchFormState.model_type;
  }
  if (searchFormState.searchMinPrice) {
    // 将searchMinPrice的键值对加入searchForm
    searchForm.searchMinPrice = searchFormState.searchMinPrice;
  }
  if (searchFormState.searchMaxPrice) {
    // 将searchMaxPrice的键值对加入searchForm
    searchForm.searchMaxPrice = searchFormState.searchMaxPrice;
  }
  if (searchFormState.material) {
    // 将material的键值对加入searchForm
    searchForm.material = searchFormState.material;
  }
  return searchForm;
});

// 功能函数:处理Table的onChange事件
const handleTableChange = (
  pag: { pageSize: number; current: number },
  filters: any,
  sorter: any,
) => {
  run({
    page: pag.current,
    pageSize: pag.pageSize,
    sortField: sorter.field,
    sortOrder: sorter.order,
    ...filters,
    ...searchFormFilter.value,
  });
};

// 功能函数：table选择项选择触发函数，将选中的表格项的key存入selectedRowKeys
const onSelectChange = (selectedRowKeys: Key[]) => {
  // 将选中的表格项的key存入selectedRowKeys
  tableSelectionState.selectedRowKeys = selectedRowKeys;
};

// #########################################onClick函数定义#########################################
// 搜索栏重置按钮点击事件
const onClickReset = () => {
  // 重置搜索栏
  searchFormRef.value.resetFields();
  // 再次请求Table
  run({
    page: 1,
    pageSize: 10,
  });
};

// 搜索栏搜索按钮点击事件
const onClickSearch = () => {
  // 通过搜索栏表单数据请求Table
  run({
    page: 1,
    pageSize: 10,
    ...searchFormFilter.value,
  });
};

// table选择项全部删除按钮点击事件
const onClickDeleteAllSelected = async () => {
  // 打开删除确认modal
  Modal.confirm({
    title: "确认删除",
    okText: "确认",
    cancelText: "取消",
    centered: true,
    icon: createVNode(ExclamationCircleOutlined),
    content: "是否确定删除所选项？",
    onOk: async () => {
      // 构造post请求表单formdata
      const formData = new FormData();
      // 将待删除的表格项的key存入formdata
      formData.append(
        "ids",
        JSON.stringify(tableSelectionState.selectedRowKeys),
      );
      // 删除选中的表格项
      await axios
        .post("/glassmanagement/api/delete-eyeglassframes", formData)
        .then((response) => {
          // 删除成功
          if (response.data.code === 0) {
            // 提示删除成功
            message.success(response.data.msg);
            // 清空选中的表格项
            tableSelectionState.selectedRowKeys = [];
            // 重新请求Table，定位在当前页
            run({
              page: current.value,
              pageSize: pageSize.value,
              ...searchFormFilter.value,
            });
          } else {
            // 提示删除失败
            message.error(response.data.msg);
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
  });
};

// table单项试戴按钮点击事件
const onClickTryOn = (id: number) => {
  // 跳转到试戴页面
  tryonPageState.showTryOnPage = true;
  tryonPageState.id = id;
};

// table单项删除按钮点击事件
const onClickDelete = async (id: number) => {
  // 打开删除确认modal
  Modal.confirm({
    title: "确认删除",
    okText: "确认",
    cancelText: "取消",
    centered: true,
    icon: createVNode(ExclamationCircleOutlined),
    content: "是否确定删除所选项？",
    onOk: async () => {
      // 构造post请求表单formdata
      const formData = new FormData();
      // 将待删除的表格项的key存入formdata
      formData.append("ids", JSON.stringify([id]));
      // 删除单项
      await axios
        .post("/glassmanagement/api/delete-eyeglassframes", formData)
        .then((response) => {
          // 删除成功
          if (response.data.code === 0) {
            // 提示删除成功
            message.success(response.data.msg);
            // 重新请求Table，定位在当前页
            run({
              page: current.value,
              pageSize: pageSize.value,
              ...searchFormFilter.value,
            });
          } else {
            // 提示删除失败
            message.error(response.data.msg);
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
  });
};

// 试戴状态相关
// 功能函数：获取试戴状态标签
const getTryOnStateLabel = (state: number) => {
  if (state == 0) {
    return "待处理";
  } else if (state == 1) {
    return "处理中";
  } else if (state == 2) {
    return "处理成功";
  } else if (state == 3) {
    return "处理失败";
  } else {
    return "无";
  }
};

// 功能函数: 只获取试戴状态数据
const refreshTryOnStates = async () => {
  try {
    const ids = tryOnStates.value.map((item) => item.id);
    const response = await axios.get(
      "/glassmanagement/api/get-all-try-on-states",
      {
        params: {
          ids: ids.join(","), // 将数组转换为逗号分隔的字符串
        },
      },
    );
    if (response.data.code === 0) {
      // console.log(response.data.data);
      tryOnStates.value = response.data.data.map((item: try_on_state) => ({
        id: item.id,
        aiface_tryon_state: item.aiface_tryon_state,
        is_active: item.is_active,
      }));
    }
  } catch (error) {
    console.error("获取试戴状态失败:", error);
  }
};

// #########################################监视函数#########################################
watch(dataSource, () => {
  // 清空试戴状态
  tryOnStates.value = [];
  // 遍历dataSource，将试戴状态加入tryOnStates
  data.value?.data.data.forEach((item) => {
    tryOnStates.value.push({
      id: item.id,
      aiface_tryon_state: item.aiface_tryon_state,
      is_active: item.is_active,
    });
  });
});
</script>

<style scoped>
.full-height-row {
  height: 100vh;
}

.title {
  text-align: center;
}

/* 搜索栏 */
.search-form :deep(.ant-select-selector) {
  width: 100%;
  height: 32px;
  font-size: 16px;
  border-color: #999999;
  border-radius: 9px;
  padding-left: 15px;
}

.registry-preview-sub-image {
  margin: 16px;
  height: calc(80% - 32px);
  width: calc(80% - 32px);
  background-color: #ababab;
  border: none;
  border-radius: 12px;
}

.ant-form-item {
  margin: 0;
  color: #999999;
}

/* 修改modal */
:deep(.slick-slide) {
  height: 265px;
  background: white;
  display: flex !important;
  align-items: center;
  justify-content: center;
}

:deep(.slick-arrow.custom-slick-arrow) {
  width: 30px;
  height: 30px;
  font-size: 30px;
  color: #8675ff;
  z-index: 1;
}

:deep(.slick-arrow.custom-slick-arrow:before) {
  display: none;
}

:deep(.slick-dots li button) {
  background-color: #8675ff !important;
}

/* 修改modal baisc */
.modal-basic-item :deep(.ant-select-selector),
.ant-input,
.ant-input-number {
  padding-left: 11px;
  width: 100%;
  height: 30px;
  border-radius: 9px;
  font-size: 15px;
}

/* 修改modal basic：消除input-number的重复padding */
.modal-basic-item :deep(.ant-input-number-input) {
  padding: 0;
}
.modal-basic-item :deep(.ant-radio-button-wrapper) {
  padding-inline: 7.85px;
}

/* 修改modal explicit item 用于镜架重量和风格 */
.modal-explicit-item {
  width: 100%;
  /* height 用于和下面的表单隔开间距 */
  height: 60px;
}

/* 修改modal：信息栏目选择 */
.detailTypeChosen :deep(.ant-btn-text) {
  background-color: #ffffff;
  width: 163.5px;
  height: 49px;
  border-radius: 7px;
  justify-content: center;
  text-align: center;
  color: #8675ff;
  font-size: 18px;
}

.detailTypeUnchosen :deep(.ant-btn-text) {
  width: 163.9px;
  height: 49px;
  border-radius: 7px;
  justify-content: center;
  text-align: center;
  color: #ffffff;
  font-size: 18px;
}

/* 去除a-image预览字样 */
.custom-a-image :deep(.ant-image-mask-info) {
  visibility: hidden;
  font-size: 0;
}

.custom-a-image :deep(.ant-image-mask-info span) {
  visibility: visible;
  font-size: 20;
}
</style>
