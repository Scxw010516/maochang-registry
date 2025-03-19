<template>
  <div
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
                <a-button type="primary" @click="onClickEditModal(record.id)"
                  >修改</a-button
                >
                <a-button danger @click="onClickDelete(record.id)"
                  >删除</a-button
                >
              </a-space>
            </span>
          </template>
          <template v-if="column.key === 'all_calculate_state'">
            <span>
              <a-button
                type="primary"
                ghost
                @click="onClickCalculationState(record.id)"
                >{{ getAllCalculateLabel(record.id) }}</a-button
              >
            </span>
          </template>
        </template>
      </a-table>
    </div>
    <!-- 镜架修改modal -->
    <a-modal
      v-model:open="editModalState.showDetailEditModal"
      centered
      :keyboard="false"
      :maskClosable="false"
      width="1000px"
      :bodyStyle="modalBodyStyle"
      footer=""
      @cancel="onClickCancelEditModal"
      :after-close="afterCloseEditModal"
    >
      <a-col>
        <!-- 信息栏目选择 -->
        <a-row justify="center">
          <a-col>
            <a-row
              style="
                margin-top: 61px;
                height: 53px;
                width: 333px;
                background-color: #dedee1;
                border-radius: 7px;
                justify-content: space-around;
                align-items: center;
              "
            >
              <a-col
                :class="
                  editModalState.modalDetailsType === 'basic'
                    ? 'detailTypeChosen'
                    : 'detailTypeUnchosen'
                "
              >
                <a-button
                  type="text"
                  @click="
                    () => {
                      editModalState.modalDetailsType = 'basic';
                    }
                  "
                  >基础信息
                </a-button>
              </a-col>
              <a-col
                :class="
                  editModalState.modalDetailsType === 'explicit'
                    ? 'detailTypeChosen'
                    : 'detailTypeUnchosen'
                "
              >
                <a-button
                  type="text"
                  @click="
                    () => {
                      editModalState.modalDetailsType = 'explicit';
                    }
                  "
                  >详细信息
                </a-button>
              </a-col>
            </a-row>
          </a-col>
        </a-row>
        <!-- 基础信息 -->
        <a-row
          v-show="editModalState.modalDetailsType === 'basic'"
          justify="center"
        >
          <!-- 图片 -->
          <div
            style="
              height: 265px;
              width: 333px;
              margin: 25px calc(50% - 333px / 2) 30px;
              background-color: #dedee1;
            "
          >
            <a-carousel
              class="custom-a-image"
              arrows
              style="height: 100%; width: 100%"
            >
              <template #prevArrow>
                <div class="custom-slick-arrow" style="left: -60px; z-index: 1">
                  <left-circle-outlined />
                </div>
              </template>
              <template #nextArrow>
                <div class="custom-slick-arrow" style="right: -60px">
                  <right-circle-outlined />
                </div>
              </template>
              <a-image
                style="height: 100%; width: 100%; object-fit: contain"
                :src="EyeGlassImagePathFormState.topview"
              />
              <a-image
                style="height: 100%; width: 100%; object-fit: contain"
                :src="EyeGlassImagePathFormState.frontview"
              />
              <a-image
                style="height: 100%; width: 100%; object-fit: contain"
                :src="EyeGlassImagePathFormState.sideview"
              />
            </a-carousel>
          </div>
          <!-- 基础信息列表 -->
          <a-form
            ref="EyeGlassBasicFormRef"
            :model="EyeGlassBasicFormState"
            :rules="EyeGlassBasicFormRules"
            :labelCol="{ span: 6 }"
            :wrapperCol="{ span: 18 }"
            labelAlign="left"
            hideRequiredMark
          >
            <a-row :gutter="[30, 30]" style="margin-top: 25px; width: 850px">
              <a-col style="height: 30px" :span="8">
                <a-form-item label="SKU" name="sku" class="modal-basic-item">
                  <a-input
                    v-model:value="EyeGlassBasicFormState.sku"
                    disabled
                  ></a-input>
                </a-form-item>
              </a-col>
              <a-col style="height: 30px" :span="8">
                <a-form-item label="品牌" name="brand" class="modal-basic-item">
                  <a-auto-complete
                    v-model:value="EyeGlassBasicFormState.brand"
                    :options="options.brand_options"
                    :filter-option="filterOption"
                  ></a-auto-complete>
                </a-form-item>
              </a-col>
              <a-col style="height: 30px" :span="8">
                <a-form-item
                  label="型号"
                  name="model_type"
                  class="modal-basic-item"
                >
                  <a-auto-complete
                    v-model:value="EyeGlassBasicFormState.model_type"
                    :options="options.model_type_options"
                    :filter-option="filterOption"
                  ></a-auto-complete>
                </a-form-item>
              </a-col>
              <a-col style="height: 30px" :span="8">
                <a-form-item label="价格" name="price" class="modal-basic-item">
                  <a-input-number
                    v-model:value="EyeGlassBasicFormState.price"
                    :precision="2"
                    :controls="false"
                    decimalSeparator="."
                  ></a-input-number>
                </a-form-item>
              </a-col>
              <a-col style="height: 30px" :span="8">
                <a-form-item
                  label="材质"
                  name="material"
                  class="modal-basic-item"
                >
                  <a-select
                    v-model:value="EyeGlassBasicFormState.material"
                    placeholder="选择材质（单选）"
                    :options="options.material_options"
                  ></a-select>
                </a-form-item>
              </a-col>
              <a-col style="height: 30px" :span="8">
                <a-form-item label="颜色" name="color" class="modal-basic-item">
                  <a-select
                    v-model:value="EyeGlassBasicFormState.color"
                    placeholder="选择颜色（单选）"
                    :options="options.color_options"
                  ></a-select>
                </a-form-item>
              </a-col>
              <a-col style="height: 30px" :span="8">
                <a-form-item label="形状" name="shape" class="modal-basic-item">
                  <a-select
                    v-model:value="EyeGlassBasicFormState.shape"
                    placeholder="选择形状（单选）"
                    :options="options.shape_options"
                  ></a-select>
                </a-form-item>
              </a-col>

              <a-col style="height: 30px" :span="8">
                <a-form-item
                  label="鼻托"
                  name="isnosepad"
                  class="modal-basic-item"
                >
                  <a-radio-group
                    v-model:value="EyeGlassBasicFormState.isnosepad"
                  >
                    <a-radio-button
                      :value="1"
                      style="
                        border-top-left-radius: 9px;
                        border-bottom-left-radius: 9px;
                      "
                      >有
                    </a-radio-button>
                    <a-radio-button
                      :value="0"
                      style="
                        border-top-right-radius: 9px;
                        border-bottom-right-radius: 9px;
                      "
                      >无
                    </a-radio-button>
                  </a-radio-group>
                </a-form-item>
              </a-col>
              <a-col :span="8">
                <a-form-item
                  label="透明"
                  name="is_transparent"
                  class="modal-basic-item"
                >
                  <a-radio-group
                    v-model:value="EyeGlassBasicFormState.is_transparent"
                    :options="options.is_transparent_options"
                    option-type="button"
                  >
                  </a-radio-group>
                </a-form-item>
              </a-col>
              <a-col :span="8">
                <a-form-item
                  label="镜框类型"
                  name="frame_type"
                  class="modal-basic-item"
                >
                  <a-radio-group
                    v-model:value="EyeGlassBasicFormState.frame_type"
                    :options="options.frame_type_options"
                    option-type="button"
                  >
                  </a-radio-group>
                </a-form-item>
              </a-col>
              <a-col style="height: 30px" :span="8">
                <a-form-item label="库存" name="stock" class="modal-basic-item">
                  <a-input-number
                    v-model:value="EyeGlassBasicFormState.stock"
                    min="0"
                    :controls="false"
                  ></a-input-number>
                </a-form-item>
              </a-col>
              <a-col style="height: 30px" :span="8">
                <a-form-item
                  label="撑片弧度"
                  name="lens_radian"
                  class="modal-basic-item"
                >
                  <a-input-number
                    v-model:value="EyeGlassBasicFormState.lens_radian"
                    :controls="false"
                  />
                </a-form-item>
              </a-col>
              <a-col style="height: 30px" :span="8">
                <a-form-item
                  label="镜片宽度"
                  name="lens_width_st"
                  class="modal-basic-item"
                >
                  <a-input-number
                    v-model:value="EyeGlassBasicFormState.lens_width_st"
                    :controls="false"
                  />
                </a-form-item>
              </a-col>
              <a-col style="height: 30px" :span="8">
                <a-form-item
                  label="鼻梁宽度"
                  name="bridge_width_st"
                  class="modal-basic-item"
                >
                  <a-input-number
                    v-model:value="EyeGlassBasicFormState.bridge_width_st"
                    :controls="false"
                  />
                </a-form-item>
              </a-col>
              <a-col style="height: 30px" :span="8">
                <a-form-item
                  label="镜腿长度"
                  name="temple_length_st"
                  class="modal-basic-item"
                >
                  <a-input-number
                    v-model:value="EyeGlassBasicFormState.temple_length_st"
                    :controls="false"
                  />
                </a-form-item>
              </a-col>
              <a-col style="height: 30px" :span="8">
                <a-form-item
                  label="镜架重量"
                  name="weight"
                  class="modal-basic-item"
                >
                  <a-input
                    v-model:value="EyeGlassBasicFormState.weight"
                    :controls="false"
                  ></a-input>
                </a-form-item>
              </a-col>
            </a-row>
          </a-form>
        </a-row>
        <!-- 详细信息 计算成功：显示详细信息-->
        <div
          v-show="
            editModalState.modalDetailsType === 'explicit' &&
            editModalState.millimeter_measurement_state == 2
          "
          style="height: 590px; overflow: auto; margin-top: 25px"
        >
          <a-row :gutter="[30, 30]" style="width: 800px">
            <a-col
              v-for="(value, key) in EyeGlassDetailFormLabel"
              :key="key"
              :span="6"
            >
              <a-row
                style="height: 100%; width: 100%"
                justify="center"
                align="bottom"
              >
                <a-col :span="24">
                  <img
                    :src="`/src/assets/params_pic/${key}.svg`"
                    alt="SVG Image"
                    width="70%"
                    style="display: block; margin: 0 auto"
                  />
                </a-col>
                <a-col>
                  {{ EyeGlassDetailFormLabel[key] }}
                </a-col>
                <a-col :span="24">
                  <a-input
                    v-model:value="EyeGlassDetailFormState[key]"
                    :suffix="EyeGlassDetailFormUnit[key]"
                    style="border-radius: 9px; padding-left: 11px; height: 30px"
                  ></a-input>
                </a-col>
              </a-row>
            </a-col>
          </a-row>
        </div>
        <!-- 保存按钮 -->
        <a-button
          style="
            margin: 30px calc(50% - 144px / 2) 39px;
            height: 72px;
            width: 144px;
            background-color: #8675ff;
            border-radius: 12px;
            color: white;
            font-size: 20px;
          "
          @click="onClickSaveEditModal"
        >
          保存
        </a-button>
      </a-col>
    </a-modal>
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
} from "vue";
import { message, Modal } from "ant-design-vue";
import {
  ExclamationCircleOutlined,
  LeftCircleOutlined,
  RightCircleOutlined,
} from "@ant-design/icons-vue";
// import { useRouter } from "vue-router";
import { useOptionStore, useUserStore, useStateStore } from "@/stores/store";
import axios from "@/config/axios-config";
import { usePagination } from "vue-request";
import { Key } from "ant-design-vue/lib/_util/type";
import type { Rule } from "ant-design-vue/es/form"; // 引入表单验证规则Rule组件
import {
  EyeGlassBasicForm, // 镜架基础参数接口
  // EyeGlassBasicFormLabel, // 镜架基础参数标签
  // EyeGlassStyleFormLabel, // 镜架风格参数标签
  EyeGlassDetailForm, // 镜架详细参数接口
  EyeGlassDetailFormLabel, // 镜架详细参数标签
  // EyeGlassDetailToviewFormLabel, // 镜架详细参数转视图参数标签
  EyeGlassDetailFormUnit, // 镜架详细参数单位
  // EyeGlassWeightFormLabel, // 镜架重量参数标签
  // EyeGlassImageForm, // 镜架图像参数接口
  EyeGlassImagePathForm, // 镜架图像路径参数接口
  // EyeGlassImageFormLabel, // 镜架图像参数标签
  // EyeGlassImageBackgroundForm, // 镜架图像背景参数接口
  // EyeGlassCalculateParams, // 镜架计算参数
  // EyeGlassCalculateParamsLabel, // 镜架计算参数标签
  // EyeGlassCalculateParamsExample, // 镜架计算参数示例
} from "./params";
import { initFormOptions } from "./utils";

//#########################################参数初始化###########################################
// const router = useRouter();
const options = useOptionStore();
const user = useUserStore();
const state = useStateStore();
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
    title: "计算状态",
    key: "all_calculate_state",
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
    pixel_measurement_state: number;
    millimeter_measurement_state: number;
    calculation_state: number;
    coordinate_state: number;
    image_mask_state: number;
    image_seg_state: number;
    image_beautify_state: number;
  }[];
  count: number;
};

// 镜架计算状态接口
interface calculate_state {
  id: number;
  pixel_measurement_state: number;
  millimeter_measurement_state: number;
  calculation_state: number;
  coordinate_state: number;
  image_mask_state: number;
  image_seg_state: number;
  image_beautify_state: number;
}

// 镜架计算状态数组
const calculateStates = ref<calculate_state[]>([]);

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

// 镜架基础参数表单实例
const EyeGlassBasicFormRef = ref();
// 镜架基础参数表单初始化数据
const EyeGlassBasicFormInitState: UnwrapRef<EyeGlassBasicForm> = reactive({
  sku: "",
  brand: "",
  model_type: "",
  price: null,
  material: null,
  color: null,
  shape: null,
  isnosepad: null,
  is_transparent: null,
  frame_type: null,
  stock: null,
  lens_radian: null,
  lens_width_st: null,
  bridge_width_st: null,
  temple_length_st: null,
  weight: "",
});
const EyeGlassBasicFormState: UnwrapRef<EyeGlassBasicForm> = reactive({
  sku: "",
  brand: "",
  model_type: "",
  price: null,
  material: null,
  color: null,
  shape: null,
  isnosepad: null,
  is_transparent: null,
  frame_type: null,
  stock: null,
  lens_radian: null,
  lens_width_st: null,
  bridge_width_st: null,
  temple_length_st: null,
  weight: "",
});
// 镜架基础参数表单校验规则
const EyeGlassBasicFormRules: Record<string, Rule[]> = {
  sku: [
    { required: true, message: "请输入镜框SKU", trigger: ["blur", "change"] },
  ],
  brand: [
    { required: true, message: "请输入镜框品牌", trigger: ["blur", "change"] },
  ],
  model_type: [
    { required: true, message: "请输入镜框型号", trigger: ["blur", "change"] },
  ],
  price: [
    {
      required: true,
      message: "请输入镜框价格",
      trigger: ["blur", "change"],
    },
    {
      message: "价格格式错误",
      type: "number",
      max: 999999999999.99,
      min: 0,
      trigger: ["blur", "change"],
    },
  ],
  material: [
    { required: true, message: "请选择镜框材质", trigger: ["blur", "change"] },
  ],
  color: [
    { required: true, message: "请选择镜框颜色", trigger: ["blur", "change"] },
  ],
  shape: [
    { required: true, message: "请选择镜框形状", trigger: ["blur", "change"] },
  ],
  isnosepad: [
    {
      required: true,
      message: "请选择是否有鼻托",
      trigger: ["blur", "change"],
    },
  ],
  is_transparent: [
    {
      required: true,
      message: "请选择镜框是否透明",
      trigger: ["blur", "change"],
    },
  ],
  frame_type: [
    {
      required: true,
      message: "请选择镜框类型",
      trigger: ["blur", "change"],
    },
  ],
  stock: [
    {
      required: false,
      message: "请输入镜框库存",
      trigger: ["blur", "change"],
    },
    {
      message: "库存格式错误",
      type: "number",
      max: 999999999999999,
      min: 0,
      trigger: ["blur", "change"],
    },
  ],
  lens_radian: [
    { required: true, message: "请输入撑片弧度", trigger: ["blur", "change"] },
    {
      type: "number",
      min: -9999999999.9999,
      max: 9999999999.9999,
      message: "弧度格式错误",
      trigger: ["blur", "change"],
    },
  ],
  lens_width_st: [
    {
      required: false,
      message: "请输入镜片宽度",
      trigger: ["blur", "change"],
    },
    {
      message: "宽度格式错误",
      type: "number",
      max: 9999999999.9999,
      min: 0,
      trigger: ["blur", "change"],
    },
  ],
  bridge_width_st: [
    {
      required: false,
      message: "请输入鼻梁宽度",
      trigger: ["blur", "change"],
    },
    {
      message: "宽度格式错误",
      type: "number",
      max: 9999999999.9999,
      min: 0,
      trigger: ["blur", "change"],
    },
  ],
  temple_length_st: [
    {
      required: false,
      message: "请输入镜腿长度",
      trigger: ["blur", "change"],
    },
    {
      message: "长度格式错误",
      type: "number",
      max: 9999999999.9999,
      min: 0,
      trigger: ["blur", "change"],
    },
  ],
};

// 镜架详细参数表单实例
const EyeGlassDetailFormRef = ref();
// 镜架详细参数表单初始化数据
const EyeGlassDetailFormInitState: UnwrapRef<EyeGlassDetailForm> = reactive({
  frame_height: "",
  frame_width: "",
  pile_height_left: "",
  pile_height_right: "",
  frame_top_width: "",
  top_points: "",
  frame_rects: "",
  lens_width_left: "",
  lens_width_right: "",
  lens_height_left: "",
  lens_height_right: "",
  lens_diagonal_left: "",
  lens_diagonal_right: "",
  lens_area_left: "",
  lens_area_right: "",
  bridge_width: "",
  lens_center_points: "",
  lens_top_points: "",
  vertical_angle: "",
  forward_angle: "",
  temple_angle: "",
  drop_length: "",
  face_angle: "",
  sagittal_angle_left: "",
  sagittal_angle_right: "",
  temple_length_left: "",
  temple_length_right: "",
  temporal_width: "",
  spread_angle_left: "",
  spread_angle_right: "",
  pile_distance: "",
});
// 镜架详细参数表单数据
const EyeGlassDetailFormState: UnwrapRef<EyeGlassDetailForm> = reactive({
  frame_height: "",
  frame_width: "",
  pile_height_left: "",
  pile_height_right: "",
  frame_top_width: "",
  top_points: "",
  frame_rects: "",
  lens_width_left: "",
  lens_width_right: "",
  lens_height_left: "",
  lens_height_right: "",
  lens_diagonal_left: "",
  lens_diagonal_right: "",
  lens_area_left: "",
  lens_area_right: "",
  bridge_width: "",
  lens_center_points: "",
  lens_top_points: "",
  vertical_angle: "",
  forward_angle: "",
  temple_angle: "",
  drop_length: "",
  face_angle: "",
  sagittal_angle_left: "",
  sagittal_angle_right: "",
  temple_length_left: "",
  temple_length_right: "",
  temporal_width: "",
  spread_angle_left: "",
  spread_angle_right: "",
  pile_distance: "",
});
// 镜架详细参数表单校验规则
const EyeGlassDetailFormRules: Record<string, Rule[]> = {
  frame_height: [{ required: true, trigger: ["blur", "change"] }],
  frame_width: [{ required: true, trigger: ["blur", "change"] }],
  pile_height_left: [{ required: true, trigger: ["blur", "change"] }],
  pile_height_right: [{ required: true, trigger: ["blur", "change"] }],
  frame_top_width: [{ required: true, trigger: ["blur", "change"] }],
  top_points: [
    {
      required: true,
      trigger: ["blur", "change"],
    },
  ],
  frame_rects: [
    {
      required: true,
      trigger: ["blur", "change"],
    },
  ],
  lens_width_left: [
    {
      required: true,
      trigger: ["blur", "change"],
    },
  ],
  lens_width_right: [
    {
      required: true,
      trigger: ["blur", "change"],
    },
  ],
  lens_height_left: [
    {
      required: true,
      trigger: ["blur", "change"],
    },
  ],
  lens_height_right: [
    {
      required: true,
      trigger: ["blur", "change"],
    },
  ],
  lens_diagonal_left: [
    {
      required: true,
      trigger: ["blur", "change"],
    },
  ],
  lens_diagonal_right: [
    {
      required: true,
      trigger: ["blur", "change"],
    },
  ],
  lens_area_left: [
    {
      required: true,
      trigger: ["blur", "change"],
    },
  ],
  lens_area_right: [
    {
      required: true,
      trigger: ["blur", "change"],
    },
  ],
  bridge_width: [
    {
      required: true,
      trigger: ["blur", "change"],
    },
  ],
  lens_center_points: [
    {
      required: true,
      trigger: ["blur", "change"],
    },
  ],
  lens_top_points: [
    {
      required: true,
      trigger: ["blur", "change"],
    },
  ],
  vertical_angle: [
    {
      required: true,
      trigger: ["blur", "change"],
    },
  ],
  forward_angle: [
    {
      required: true,
      trigger: ["blur", "change"],
    },
  ],
  temple_angle: [
    {
      required: true,
      trigger: ["blur", "change"],
    },
  ],
  drop_length: [
    {
      required: true,
      trigger: ["blur", "change"],
    },
  ],
  face_angle: [
    {
      required: true,
      trigger: ["blur", "change"],
    },
  ],
  sagittal_angle_left: [
    {
      required: true,
      trigger: ["blur", "change"],
    },
  ],
  sagittal_angle_right: [
    {
      required: true,
      trigger: ["blur", "change"],
    },
  ],
  temple_length_left: [
    {
      required: true,
      trigger: ["blur", "change"],
    },
  ],
  temple_length_right: [
    {
      required: true,
      trigger: ["blur", "change"],
    },
  ],
  temporal_width: [
    {
      required: true,
      trigger: ["blur", "change"],
    },
  ],
  spread_angle_left: [
    {
      required: true,
      trigger: ["blur", "change"],
    },
  ],
  spread_angle_right: [
    {
      required: true,
      trigger: ["blur", "change"],
    },
  ],
  pile_distance: [
    {
      required: true,
      trigger: ["blur", "change"],
    },
  ],
};
// 镜架图像参数表单初始化数据
const EyeGlassImagePathFormInitState: UnwrapRef<EyeGlassImagePathForm> =
  reactive({
    frontview: "",
    topview: "",
    sideview: "",
  });
// 镜架图像参数表单数据
const EyeGlassImagePathFormState: UnwrapRef<EyeGlassImagePathForm> = reactive({
  frontview: "",
  topview: "",
  sideview: "",
});

// select和autocompe下拉框选项接口定义
interface Option {
  value: string;
  label: string;
}

// 镜架详情modal相关
const editModalState = reactive<{
  showDetailEditModal: boolean; // 镜架修改弹窗可见状态
  modalId: number | null; // 镜架修改弹窗id
  modalDetailsType: "basic" | "explicit"; // 镜架详情弹窗栏目
  calculate_state: number; // 镜架计算状态
  millimeter_measurement_state: number; // 镜架毫米测量状态
}>({
  showDetailEditModal: false,
  modalId: null,
  modalDetailsType: "basic",
  calculate_state: 2,
  millimeter_measurement_state: 2,
});
// modal的body样式
const modalBodyStyle = reactive({
  padding: "0 60px",
});

// 计算状态model相关
const calculateModelLoading = ref(false); // 计算状态model加载中
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
  calculateModelLoading.value = false;
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

// 功能函数：通过id获取镜架详情
const getEyeglassFrameDetails = async (id: number) => {
  // 通过id获取镜架详情
  await axios
    .get(`/glassmanagement/api/get-eyeglassframe-detail?id=${id}`)
    .then((response) => {
      // 获取成功
      if (response.data.code === 0) {
        // 将获取到的镜架基本信息赋值给镜架基本信息表单
        Object.entries(EyeGlassBasicFormState).forEach(([key]) => {
          if (key in response.data.data)
            EyeGlassBasicFormState[key] = response.data.data[key];
        });
        // 将获取到的镜架风格信息赋值给镜架风格信息表单
        // Object.entries(EyeGlassStyleFormState).forEach(([key]) => {
        //   if (key in response.data.data)
        //     EyeGlassStyleFormState[key] = response.data.data[key];
        // });
        // 将获取到的镜架详细信息赋值给镜架详细信息表单
        Object.entries(EyeGlassDetailFormState).forEach(([key]) => {
          if (key in response.data.data)
            EyeGlassDetailFormState[key] = response.data.data[key];
        });
        // 将获取到的镜架重量信息赋值给镜架重量信息表单
        // Object.entries(EyeGlassWeightFormState).forEach(([key]) => {
        //   if (key in response.data.data)
        //     EyeGlassWeightFormState[key] = response.data.data[key];
        // });
        // 将获取到的镜架图像信息赋值给镜架图像信息表单
        Object.entries(EyeGlassImagePathFormState).forEach(([key]) => {
          if (key in response.data.data)
            EyeGlassImagePathFormState[key] = response.data.data[key];
        });
      } else {
        // 提示获取失败
        message.error(response.data.msg);
      }
    })
    .catch((error) => {
      console.log(error);
    });
  // 转换EyeGlassBasicFormState表单数据类型
  formatEyeGlassFormState();
};

// 功能函数：转换EyeGlassBasicFormState表单数据类型，在getEyeglassFrameDetails函数中调用
const formatEyeGlassFormState = () => {
  // 将EyeGlassBasicFormState表单数据类型转换为对应的类型
  EyeGlassBasicFormState.price = Number(EyeGlassBasicFormState.price);
  EyeGlassBasicFormState.material = Number(EyeGlassBasicFormState.material);
  EyeGlassBasicFormState.color = Number(EyeGlassBasicFormState.color);
  EyeGlassBasicFormState.shape = Number(EyeGlassBasicFormState.shape);
  EyeGlassBasicFormState.isnosepad = EyeGlassBasicFormState.isnosepad ? 1 : 0;
  EyeGlassBasicFormState.is_transparent = Number(
    EyeGlassBasicFormState.is_transparent,
  );
  EyeGlassBasicFormState.frame_type = Number(EyeGlassBasicFormState.frame_type);
  EyeGlassBasicFormState.stock = Number(EyeGlassBasicFormState.stock);
  EyeGlassBasicFormState.lens_radian = Number(
    EyeGlassBasicFormState.lens_radian,
  );
  EyeGlassBasicFormState.lens_width_st = Number(
    EyeGlassBasicFormState.lens_width_st,
  );
  EyeGlassBasicFormState.bridge_width_st = Number(
    EyeGlassBasicFormState.bridge_width_st,
  );
  EyeGlassBasicFormState.temple_length_st = Number(
    EyeGlassBasicFormState.temple_length_st,
  );
  // 将EyeGlassStyleFormState表单数据类型转换为对应的类型
  // EyeGlassStyleFormState.style = EyeGlassStyleFormState.style.map((item) =>
  //   Number(item),
  // );
};

// 功能函数：初始化基础参数表单
const initEyeGlassBasicFormState = () => {
  Object.assign(EyeGlassBasicFormState, EyeGlassBasicFormInitState);
};

// 功能函数：初始化风格参数表单
// const initEyeGlassStyleFormState = () => {
//   Object.assign(EyeGlassStyleFormState, EyeGlassStyleFormInitState);
// };

// 功能函数：初始化详细参数表单
const initEyeGlassDetailFormState = () => {
  Object.assign(EyeGlassDetailFormState, EyeGlassDetailFormInitState);
};

// 功能函数：初始化重量参数表单
// const initEyeGlassWeightFormState = () => {
//   Object.assign(EyeGlassWeightFormState, EyeGlassWeightFormInitState);
// };

// 功能函数：初始化图像参数表单
const initEyeGlassImageFormState = () => {
  Object.assign(EyeGlassImagePathFormState, EyeGlassImagePathFormInitState);
};

// 功能函数：初始化所有表单
const initAllForms = () => {
  // 重置所有表单和状态
  initEyeGlassBasicFormState();
  // initEyeGlassStyleFormState();
  initEyeGlassDetailFormState();
  // initEyeGlassWeightFormState();
  initEyeGlassImageFormState();
};

// 功能函数：提交修改镜架参数至服务器
const saveEditEyeglassFrame = async () => {
  // 验证通过标识符
  let isFormValid = true;
  // 检查镜架基础信息是否完善
  await EyeGlassBasicFormRef.value.validate().catch(() => {
    message.error("请完善镜架基础信息");
    isFormValid = false;
  });
  // 检查镜架风格信息是否完善
  // await EyeGlassStyleFormRef.value.validate().catch(() => {
  //   message.error("请完善镜架风格信息");
  //   isFormValid = false;
  // });
  // 检查镜架详细信息是否完善
  await EyeGlassDetailFormRef.value.validate().catch(() => {
    message.error("请完善镜架详细信息");
    isFormValid = false;
  });
  // 检查镜架重量信息是否完善
  // await EyeGlassWeightFormRef.value.validate().catch(() => {
  //   message.error("请完善镜架重量信息");
  //   isFormValid = false;
  // });
  // 检查镜架采集仓库地址是否完善
  if (!user.warehouse) {
    message.error("请完善镜架采集仓库地址");
    isFormValid = false;
  }
  // 若表单验证不通过，则返回
  if (!isFormValid) {
    return false;
  }
  // 构造post请求表单formdata
  const formData = new FormData();
  // 将镜架id添加到FormData对象
  formData.append(
    "id",
    editModalState.modalId ? editModalState.modalId.toString() : "",
  );
  // 将镜架基础信息添加到FormData对象
  formData.append("sku", EyeGlassBasicFormState.sku);
  formData.append("brand", EyeGlassBasicFormState.brand);
  formData.append("model_type", EyeGlassBasicFormState.model_type);
  formData.append(
    "price",
    EyeGlassBasicFormState.price !== null
      ? EyeGlassBasicFormState.price.toString()
      : "",
  );
  formData.append(
    "material",
    EyeGlassBasicFormState.material !== null
      ? EyeGlassBasicFormState.material.toString()
      : "",
  );
  formData.append(
    "color",
    EyeGlassBasicFormState.color !== null
      ? EyeGlassBasicFormState.color.toString()
      : "",
  );
  formData.append(
    "shape",
    EyeGlassBasicFormState.shape !== null
      ? EyeGlassBasicFormState.shape.toString()
      : "",
  );
  formData.append(
    "isnosepad",
    EyeGlassBasicFormState.isnosepad
      ? EyeGlassBasicFormState.isnosepad.toString()
      : "",
  );
  formData.append(
    "is_transparent",
    EyeGlassBasicFormState.is_transparent !== null
      ? EyeGlassBasicFormState.is_transparent.toString()
      : "",
  );
  formData.append(
    "frame_type",
    EyeGlassBasicFormState.frame_type !== null
      ? EyeGlassBasicFormState.frame_type.toString()
      : "",
  );
  formData.append(
    "stock",
    EyeGlassBasicFormState.stock !== null
      ? EyeGlassBasicFormState.stock.toString()
      : "",
  );
  formData.append(
    "warehouse",
    user.warehouse !== null ? user.warehouse.toString() : "",
  );
  formData.append(
    "lens_radian",
    EyeGlassBasicFormState.lens_radian !== null
      ? EyeGlassBasicFormState.lens_radian.toString()
      : "",
  );
  formData.append(
    "lens_width_st",
    EyeGlassBasicFormState.lens_width_st !== null
      ? EyeGlassBasicFormState.lens_width_st.toString()
      : "",
  );
  formData.append(
    "bridge_width_st",
    EyeGlassBasicFormState.bridge_width_st !== null
      ? EyeGlassBasicFormState.bridge_width_st.toString()
      : "",
  );
  formData.append(
    "temple_length_st",
    EyeGlassBasicFormState.temple_length_st !== null
      ? EyeGlassBasicFormState.temple_length_st.toString()
      : "",
  );
  formData.append("weight", EyeGlassBasicFormState.weight);
  // 将镜架风格信息添加到FormData对象
  // formData.append("style", JSON.stringify(EyeGlassStyleFormState.style));
  // 将镜架详细信息添加到FormData对象
  Object.entries(EyeGlassDetailFormState).forEach(([key, value]) => {
    formData.append(key, value); // 将值转换为字符串后添加
  });
  // 将镜架重量信息添加到FormData对象
  // formData.append("weight", EyeGlassWeightFormState.weight);
  // 提交通过标识符
  let isSaveSuccess: boolean = false;
  // 发送post请求
  await axios
    .post("/glassmanagement/api/save-edit-eyeglassframe", formData)
    .then((response) => {
      // 判断返回的code值，若为-1则提示无镜架信息
      if (response.data.code === -1) {
        message.error(response.data.msg);
        isSaveSuccess = false;
      } else {
        message.success("镜架信息保存成功");
        // 重置所有表单和状态
        initAllForms();
        isSaveSuccess = true;
      }
    })
    .catch((error) => {
      console.log(error);
      isSaveSuccess = false;
    });
  return isSaveSuccess;
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

// table单项修改按钮点击事件
const onClickEditModal = (id: number) => {
  // 通过id获取镜架详情
  getEyeglassFrameDetails(id);
  // 设置镜架详情modal显示
  editModalState.showDetailEditModal = true;
  // 设置镜架详情modal的id
  editModalState.modalId = id;
};

//功能函数：提交修改镜架参数至服务器
const onClickSaveEditModal = () => {
  // 提交修改镜架参数至服务器
  saveEditEyeglassFrame().then((isSaveSuccess) => {
    if (isSaveSuccess) {
      // 设置镜架详情modal隐藏
      editModalState.showDetailEditModal = false;
      // 设置镜架详情modal的id为空
      editModalState.modalId = null;
      // 重新请求Table，定位在当前页
      run({
        page: current.value,
        pageSize: pageSize.value,
        ...searchFormFilter.value,
      });
    }
  });
};

// 镜架详情modal关闭后触发回调
const afterCloseEditModal = () => {
  // 重新获取Options,包括材质、颜色、形状、风格等
  initFormOptions();
};

// 镜架详情modal取消按钮点击事件
const onClickCancelEditModal = () => {
  // 初始化所有表单
  initAllForms();
  // 设置镜架详情modal隐藏
  editModalState.showDetailEditModal = false;
  // 设置镜架详情modal的id为空
  editModalState.modalId = null;
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
// 计算状态相关
// 功能函数：获取计算标签
const getCalculateStateLabel = (state: number) => {
  if (state == 0) {
    return "待计算";
  } else if (state == 1) {
    return "计算中";
  } else if (state == 2) {
    return "计算成功";
  } else if (state == 3) {
    return "计算失败";
  }
};
// 功能函数：获取统一计算状态标签
const getAllCalculateLabel = (id: number) => {
  let item = calculateStates.value.find(
    (item: calculate_state) => item.id === id,
  );
  if (!item) {
    return "无";
  }
  let all_calculate_state = 3;
  if (
    item.pixel_measurement_state == 2 &&
    item.millimeter_measurement_state == 2 &&
    item.calculation_state == 2 &&
    item.coordinate_state == 2 &&
    item.image_mask_state == 2 &&
    item.image_seg_state == 2 &&
    item.image_beautify_state == 2
  ) {
    // 当所有计算都成功时，计算状态为计算成功
    all_calculate_state = 2;
  } else if (
    item.pixel_measurement_state == 1 ||
    item.millimeter_measurement_state == 1 ||
    item.calculation_state == 1 ||
    item.coordinate_state == 1 ||
    item.image_mask_state == 1 ||
    item.image_seg_state == 1 ||
    item.image_beautify_state == 1
  ) {
    // 当有一个为计算中时，计算状态为计算中
    all_calculate_state = 1;
  } else if (
    item.pixel_measurement_state == 0 ||
    item.millimeter_measurement_state == 0 ||
    item.calculation_state == 0 ||
    item.coordinate_state == 0 ||
    item.image_mask_state == 0 ||
    item.image_seg_state == 0 ||
    item.image_beautify_state == 0
  ) {
    // 当有一个为待计算时，计算状态为待计
    all_calculate_state = 0;
  }
  return getCalculateStateLabel(all_calculate_state);
};

// table计算状态点击事件：展开计算状态modal
const onClickCalculationState = async (id: number) => {
  let item = calculateStates.value.find((item) => item.id === id);
  if (!item) {
    return;
  }
  let sku = dataSource.value.find((item) => item.id === id)?.sku || item.id;
  Modal.confirm({
    title: sku + " 计算状态",
    okText: "发送计算任务",
    cancelText: "取消",
    centered: true,
    icon: createVNode(ExclamationCircleOutlined),
    content: h("div", {}, [
      h(
        "p",
        "像素测量数据状态：" +
          getCalculateStateLabel(item.pixel_measurement_state),
      ),
      h(
        "p",
        "毫米测量数据状态：" +
          getCalculateStateLabel(item.millimeter_measurement_state),
      ),
      h("p", "计算数据状态：" + getCalculateStateLabel(item.calculation_state)),
      h("p", "坐标数据状态：" + getCalculateStateLabel(item.coordinate_state)),
      h(
        "p",
        "mask图片数据状态：" + getCalculateStateLabel(item.image_mask_state),
      ),
      h(
        "p",
        "分割图片数据状态：" + getCalculateStateLabel(item.image_seg_state),
      ),
      h(
        "p",
        "美化图片数据状态：" +
          getCalculateStateLabel(item.image_beautify_state),
      ),
    ]),
    onOk: () => {
      sendCalculationTask(id);
    },
    okButtonProps: {
      // disabled: getAllCalculateLabel(id) == "待计算",
      // // getAllCalculateLabel(id) == "计算中",
      // loading: calculateModelLoading.value,
    },
  });
};

// table计算状态发送计算任务事件
const sendCalculationTask = async (id: number) => {
  calculateModelLoading.value = true;
  // 构造post请求表单formdata
  const formData = new FormData();
  // 将待计算的表格项的key存入formdata
  formData.append("id", JSON.stringify(id));
  await axios
    .post("/glassmanagement/api/generate-calculate-task", formData)
    .then((response) => {
      console.log(response);
      // 生成成功
      if (response.data.code === 0) {
        calculateModelLoading.value = false;
        // 修改计算状态
        const item = calculateStates.value.find((item) => item.id === id);
        if (item) {
          item.pixel_measurement_state = 0;
          item.millimeter_measurement_state = 0;
          item.calculation_state = 0;
          item.coordinate_state = 0;
          item.image_mask_state = 0;
          item.image_seg_state = 0;
          item.image_beautify_state = 0;
        }
      } else {
        // 提示生成计算任务失败
        message.error(response.data.msg);
        calculateModelLoading.value = false;
      }
    });
};
// #########################################监视函数#########################################
watch(dataSource, () => {
  // 清空计算状态
  calculateStates.value = [];
  // 遍历dataSource，将计算状态加入calculateStates
  data.value?.data.data.forEach((item) => {
    calculateStates.value.push({
      id: item.id,
      pixel_measurement_state: item.pixel_measurement_state,
      millimeter_measurement_state: item.millimeter_measurement_state,
      calculation_state: item.calculation_state,
      coordinate_state: item.coordinate_state,
      image_mask_state: item.image_mask_state,
      image_seg_state: item.image_seg_state,
      image_beautify_state: item.image_beautify_state,
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
