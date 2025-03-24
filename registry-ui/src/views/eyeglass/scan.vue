<template>
  <!-- 输入SKU -->
  <a-row
    v-if="currentStage === 'input-sku'"
    style="
      height: 100vh;
      width: 100%;
      background-color: #ffffff;
      border-radius: 12px 0px 0px 12px;
    "
    type="flex"
    align="middle"
    justify="center"
  >
    <a-col class="sku-form-card">
      <a-row
        style="
          width: 100%;
          display: flex;
          align-items: center;
          justify-content: space-between;
        "
      >
        <a-select
          v-model:value="skuormodeltype"
          placeholder="选择检索类型"
          placement="topLeft"
          style="width: 70px"
          :options="options.skuormodeltype_options"
          @change="onChangeSKUorModeltype"
        />
        <a-auto-complete
          v-model:value="searchString"
          :options="searchOptions"
          :dropdownMatchSelectWidth="584"
          style="width: 430px"
          :defaultActiveFirstOption="false"
          @select="onSelectModeltypeOrSKU"
          @search="onSearchModeltypeOrSKU"
        >
          <template #option="item">
            <div v-if="skuormodeltype == 1">
              <a-row :gutter="2">
                <a-col :span="9" class="wrap-content"
                  >型号：{{ item.model_type }}</a-col
                >
                <a-col :span="9" class="wrap-content"
                  >SKU：{{ item.sku }}</a-col
                >
                <a-col :span="6" class="wrap-content"
                  >品牌：{{ item.brand }}</a-col
                >
              </a-row>
            </div>
            <div v-else-if="skuormodeltype == 2">
              <a-row :gutter="2">
                <a-col :span="9" class="wrap-content"
                  >SKU：{{ item.sku }}</a-col
                >
                <a-col :span="9" class="wrap-content"
                  >型号：{{ item.model_type }}</a-col
                >
                <a-col :span="6" class="wrap-content"
                  >品牌：{{ item.brand }}</a-col
                >
              </a-row>
            </div>
          </template>
          <a-input
            v-model:value="searchString"
            allow-clear
            :placeholder="
              skuormodeltype === 1 ? '请输入镜架型号' : '请输入镜架SKU'
            "
            @keyup.enter="onClickEnterSKU"
          />
        </a-auto-complete>
        <a-button
          autofocus
          type="primary"
          @click="onClickEnterSKU"
          @keyup.enter="onClickEnterSKU"
        >
          确认
        </a-button>
      </a-row>
    </a-col>
  </a-row>
  <!-- 输入基础信息 -->
  <a-row
    v-else-if="currentStage === 'input-basic-params'"
    align="middle"
    justify="center"
    style="
      height: 100vh;
      width: 100%;
      background-color: #ffffff;
      border-radius: 12px 0px 0px 12px;
    "
  >
    <a-col class="input-basic-form-card">
      <a-form
        ref="EyeGlassBasicFormRef"
        :model="EyeGlassBasicFormState"
        :rules="EyeGlassBasicFormRules"
        hideRequiredMark
        :label-col="{ span: 6 }"
        :wrapper-col="{ span: 18 }"
        labelAlign="left"
      >
        <a-form-item name="sku">
          <a-input
            class="sku-input"
            v-model:value="EyeGlassBasicFormState.sku"
            disabled
          ></a-input>
        </a-form-item>
        <a-row>
          <a-col :span="12">
            <a-form-item label="品牌" name="brand" class="basic-item">
              <a-auto-complete
                v-model:value="EyeGlassBasicFormState.brand"
                :options="options.brand_options"
                :filter-option="filterOptionbyValue"
                @keyup.enter="onClickEnterBasicParams"
              />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="型号" name="model_type" class="basic-item">
              <a-auto-complete
                v-model:value="EyeGlassBasicFormState.model_type"
                :options="options.model_type_options"
                :filter-option="filterOptionbyValue"
                @keyup.enter="onClickEnterBasicParams"
              />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="价格" name="price" class="basic-item">
              <a-input-number
                v-model:value="EyeGlassBasicFormState.price"
                :precision="2"
                :controls="false"
                decimalSeparator="."
                @keyup.enter="onClickEnterBasicParams"
              />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="材质" name="material" class="basic-item">
              <a-select
                v-model:value="EyeGlassBasicFormState.material"
                placeholder="选择材质（单选）"
                :options="options.material_options"
                @keyup.enter="onClickEnterBasicParams"
              />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="颜色" name="color" class="basic-item">
              <a-select
                v-model:value="EyeGlassBasicFormState.color"
                placeholder="选择颜色（单选）"
                :options="options.color_options"
                @keyup.enter="onClickEnterBasicParams"
              />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="形状" name="shape" class="basic-item">
              <a-select
                v-model:value="EyeGlassBasicFormState.shape"
                placeholder="选择形状（单选）"
                :options="options.shape_options"
                @keyup.enter="onClickEnterBasicParams"
              />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="鼻托" name="isnosepad" class="basic-item">
              <a-radio-group
                v-model:value="EyeGlassBasicFormState.isnosepad"
                @keyup.enter="onClickEnterBasicParams"
              >
                <a-radio-button :value="1">有 </a-radio-button>
                <a-radio-button :value="0">无 </a-radio-button>
              </a-radio-group>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="透明" name="is_transparent" class="basic-item">
              <a-radio-group
                v-model:value="EyeGlassBasicFormState.is_transparent"
                @keyup.enter="onClickEnterBasicParams"
                :options="options.is_transparent_options"
                option-type="button"
              >
              </a-radio-group>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="镜框类型" name="frame_type" class="basic-item">
              <a-radio-group
                v-model:value="EyeGlassBasicFormState.frame_type"
                @keyup.enter="onClickEnterBasicParams"
                :options="options.frame_type_options"
                option-type="button"
              >
              </a-radio-group>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="库存" name="stock" class="basic-item">
              <a-input-number
                v-model:value="EyeGlassBasicFormState.stock"
                min="0"
                :controls="false"
                @keyup.enter="onClickEnterBasicParams"
              />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="撑片弧度" name="lens_radian" class="basic-item">
              <a-input-number
                v-model:value="EyeGlassBasicFormState.lens_radian"
                :controls="false"
                @keyup.enter="onClickEnterBasicParams"
              />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item
              label="镜片宽度"
              name="lens_width_st"
              class="basic-item"
            >
              <a-input-number
                v-model:value="EyeGlassBasicFormState.lens_width_st"
                :controls="false"
                @keyup.enter="onClickEnterBasicParams"
              />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item
              label="鼻梁宽度"
              name="bridge_width_st"
              class="basic-item"
            >
              <a-input-number
                v-model:value="EyeGlassBasicFormState.bridge_width_st"
                :controls="false"
                @keyup.enter="onClickEnterBasicParams"
              />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item
              label="镜腿长度"
              name="temple_length_st"
              class="basic-item"
            >
              <a-input-number
                v-model:value="EyeGlassBasicFormState.temple_length_st"
                :controls="false"
                @keyup.enter="onClickEnterBasicParams"
              />
            </a-form-item>
          </a-col>
        </a-row>
        <!-- <a-form-item label="风格" name="style" class="basic-item">
                <a-select
                  v-model:value="EyeGlassBasicFormState.style"
                  mode="multiple"
                  placeholder="选择风格（多选）"
                  :max-tag-count="1"
                  :max-tag-text-length="5"
                  :options="options.style_options"
                  @keyup.enter="onClickEnterBasicParams"
                />
              </a-form-item> -->
      </a-form>
      <a-button
        style="
          margin: 6px calc(50% - 200px) 0;
          width: 400px;
          height: 56px;
          background-color: #8675ff;
          border-radius: 12px;
          text-align: center;
          justify-content: center;
          color: #ffffff;
          font-size: 18px;
        "
        @click="onClickEnterBasicParams"
        @keyup.enter="onClickEnterBasicParams"
      >
        开始拍摄
      </a-button>
      <a-button
        style="
          margin: 28px calc(50% - 200px) 0;
          width: 400px;
          height: 56px;
          background-color: #ffffff;
          border-radius: 12px;
          text-align: center;
          justify-content: center;
          color: #8675ff;
          font-size: 18px;
        "
        @click="onClickReturn"
      >
        返回
      </a-button>
    </a-col>
  </a-row>
  <!-- 拍摄 -->
  <a-row
    v-if="currentStage == 'preview'"
    class="registry-preview"
    :gutter="[48, 0]"
    justify="center"
    align="middle"
    style="padding: 0 48px"
  >
    <a-col :span="8" class="capture-box">
      <video
        ref="TopVideo"
        class="capture-frame"
        name="TopVideo"
        style="transform: scale(-1, 1)"
      ></video>
    </a-col>
    <a-col :span="8" class="capture-box">
      <video
        ref="FrontVideo"
        class="capture-frame"
        name="FrontVideo"
        style="transform: scale(-1, 1)"
      ></video>
    </a-col>
    <a-col :span="8" class="capture-box">
      <video
        ref="SideVideo"
        class="capture-frame"
        name="SideVideo"
        style="transform: scale(-1, 1)"
      ></video>
    </a-col>
  </a-row>
  <!-- 确认 -->
  <a-row
    v-if="currentStage == 'confirm'"
    class="registry-preview"
    :gutter="[48, 0]"
    justify="center"
    align="middle"
    style="padding: 0 48px"
  >
    <a-col :span="8" class="capture-box">
      <img :src="TopCapture.imgurl" alt="" class="capture-frame" />
    </a-col>
    <a-col :span="8" class="capture-box">
      <img :src="FrontCapture.imgurl" alt="" class="capture-frame" />
    </a-col>
    <a-col :span="8" class="capture-box">
      <img :src="SideCapture.imgurl" alt="" class="capture-frame" />
    </a-col>
  </a-row>
  <!-- 计算参数 -->
  <a-row
    v-else-if="currentStage === 'input-params'"
    class="registry-preview"
    type="flex"
    align="middle"
    justify="center"
  >
    <a-col :span="24" style="height: 100%; overflow: auto">
      <a-row class="calculate-page-title">扫描结果</a-row>
      <!-- 拍摄预览 -->
      <a-row>
        <a-col :span="8">
          <img class="registry-preview-sub-image" :src="TopCapture.imgurl" />
        </a-col>
        <a-col :span="8">
          <img class="registry-preview-sub-image" :src="FrontCapture.imgurl" />
        </a-col>
        <a-col :span="8">
          <img class="registry-preview-sub-image" :src="SideCapture.imgurl" />
        </a-col>
      </a-row>

      <!-- 信息展示 -->
      <a-row style="margin-top: 18px">
        <a-col :span="24">
          <!-- 录入的基础信息 -->
          <a-form
            ref="EyeGlassBasicFormRef"
            :model="EyeGlassBasicFormState"
            :rules="EyeGlassBasicFormRules"
            hideRequiredMark
            layout="inline"
            autocomplete="off"
            :labelCol="{ span: 6 }"
            :wrapperCol="{ span: 18 }"
            labelAlign="left"
          >
            <a-row
              :gutter="[24, 32]"
              style="margin-left: 40px !important; width: calc(100% - 85px)"
            >
              <a-col :span="6">
                <a-form-item class="calculate-item" label="SKU" name="sku">
                  <a-input
                    v-model:value="EyeGlassBasicFormState.sku"
                    disabled
                  ></a-input>
                </a-form-item>
              </a-col>
              <a-col :span="6">
                <a-form-item class="calculate-item" label="品牌" name="brand">
                  <a-auto-complete
                    v-model:value="EyeGlassBasicFormState.brand"
                    :options="options.brand_options"
                    :filter-option="filterOptionbyValue"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="6">
                <a-form-item
                  class="calculate-item"
                  label="型号"
                  name="model_type"
                >
                  <a-auto-complete
                    v-model:value="EyeGlassBasicFormState.model_type"
                    :options="options.model_type_options"
                    :filter-option="filterOptionbyValue"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="6">
                <a-form-item class="calculate-item" label="价格" name="price">
                  <a-input-number
                    v-model:value="EyeGlassBasicFormState.price"
                    :precision="2"
                    :controls="false"
                    decimalSeparator="."
                  />
                </a-form-item>
              </a-col>
              <a-col :span="6">
                <a-form-item
                  class="calculate-item"
                  label="材质"
                  name="material"
                >
                  <a-select
                    v-model:value="EyeGlassBasicFormState.material"
                    placeholder="选择材质（单选）"
                    :options="options.material_options"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="6">
                <a-form-item class="calculate-item" label="颜色" name="color">
                  <a-select
                    v-model:value="EyeGlassBasicFormState.color"
                    placeholder="选择颜色（单选）"
                    :options="options.color_options"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="6">
                <a-form-item class="calculate-item" label="形状" name="shape">
                  <a-select
                    v-model:value="EyeGlassBasicFormState.shape"
                    placeholder="选择形状（单选）"
                    :options="options.shape_options"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="6">
                <a-form-item
                  class="calculate-item"
                  label="鼻托"
                  name="isnosepad"
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
              <a-col :span="6">
                <a-form-item
                  label="透明"
                  name="is_transparent"
                  class="calculate-item"
                >
                  <a-radio-group
                    v-model:value="EyeGlassBasicFormState.is_transparent"
                    @keyup.enter="onClickEnterBasicParams"
                    :options="options.is_transparent_options"
                    option-type="button"
                  >
                  </a-radio-group>
                </a-form-item>
              </a-col>
              <a-col :span="6">
                <a-form-item
                  label="镜框类型"
                  name="frame_type"
                  class="calculate-item"
                >
                  <a-radio-group
                    v-model:value="EyeGlassBasicFormState.frame_type"
                    @keyup.enter="onClickEnterBasicParams"
                    :options="options.frame_type_options"
                    option-type="button"
                  >
                  </a-radio-group>
                </a-form-item>
              </a-col>
              <a-col :span="6">
                <a-form-item class="calculate-item" label="库存" name="stock">
                  <a-input-number
                    class="calculate-input"
                    v-model:value="EyeGlassBasicFormState.stock"
                    min="0"
                    :controls="false"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="6">
                <a-form-item
                  class="calculate-item"
                  label="撑片弧度"
                  name="lens_radian"
                >
                  <a-input-number
                    class="calculate-input"
                    v-model:value="EyeGlassBasicFormState.lens_radian"
                    :controls="false"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="6">
                <a-form-item
                  class="calculate-item"
                  label="镜片宽度"
                  name="lens_width_st"
                >
                  <a-input-number
                    class="calculate-input"
                    v-model:value="EyeGlassBasicFormState.lens_width_st"
                    :controls="false"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="6">
                <a-form-item
                  class="calculate-item"
                  label="鼻梁宽度"
                  name="bridge_width_st"
                >
                  <a-input-number
                    class="calculate-input"
                    v-model:value="EyeGlassBasicFormState.bridge_width_st"
                    :controls="false"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="6">
                <a-form-item
                  class="calculate-item"
                  label="镜腿长度"
                  name="temple_length_st"
                >
                  <a-input-number
                    class="calculate-input"
                    v-model:value="EyeGlassBasicFormState.temple_length_st"
                    :controls="false"
                  />
                </a-form-item>
              </a-col>
            </a-row>
          </a-form>
          <!-- 镜架重量 -->
          <a-row
            :gutter="[26, 32]"
            style="
              margin-left: 40px !important;
              margin-top: 32px;
              width: calc(100% - 85px);
              margin-bottom: 32px;
            "
          >
            <a-col :span="6">
              <a-form
                ref="EyeGlassWeightFormRef"
                :model="EyeGlassWeightFormState"
                :rules="EyeGlassWeightFormRules"
                hideRequiredMark
                layout="inline"
                autocomplete="off"
                :labelCol="{ span: 6 }"
                :wrapperCol="{ span: 18 }"
                labelAlign="left"
              >
                <a-form-item
                  class="calculate-item"
                  label="称重结果"
                  name="weight"
                >
                  <a-input
                    v-model:value="EyeGlassWeightFormState.weight"
                    :suffix="EyeGlassBasicFormUnit.weight"
                  ></a-input>
                </a-form-item>
              </a-form>
            </a-col>
            <a-col :span="6">
              <a-button :disabled="hasWeightLoged" @click="onClickResetWeight">
                去皮
              </a-button>
              <a-button v-if="!hasWeightLoged" @click="onClickLogWeight">
                称重
              </a-button>
              <a-button v-else @click="onClickCancelLogWeight">
                重新称重
              </a-button>
            </a-col>
          </a-row>
        </a-col>
      </a-row>
    </a-col>
  </a-row>
  <!-- 操作按钮 -->
  <a-row
    v-if="
      currentStage.includes('preview') ||
      currentStage.includes('confirm') ||
      currentStage === 'input-params'
    "
    class="registry-operations"
    type="flex"
    align="middle"
    justify="end"
    style="background-color: #ffffff; border-bottom-left-radius: 12px"
  >
    <div
      v-if="currentStage === 'preview'"
      style="margin-left: 80px; margin-right: auto"
    >
      <!-- <a-button style="margin-right: 40px" @click="onClickLightup">
        增加亮度
      </a-button>
      <a-button @click="onClickLightdown"> 降低亮度 </a-button> -->
    </div>
    <a-button
      v-if="currentStage === 'confirm'"
      class="operation-button"
      @click="onClickRedo"
      >重拍
    </a-button>
    <a-button class="operation-button" @click="onClickReturn">返回 </a-button>
    <a-button class="operation-button-primary" @click="onClickCaptureOrConfirm">
      {{ currentStage === "preview" ? "拍摄" : "确认" }}
    </a-button>
  </a-row>
  <!-- 摄像头未启动提示Modal -->
  <a-modal
    v-model:open="showCameraStateErrorModal"
    centered
    title="是否尝试重启摄像头?"
    :okText="'重启'"
    :cancelText="'取消'"
    @ok="onClickCameraStateErrorOk"
    :confirmLoading="cameraStateErrorModalLoading"
    :maskClosable="false"
    :keyboard="false"
  >
    <p>摄像头未能正常启动，请尝试重新插拔设备并重启</p>
  </a-modal>
  <!-- 秤未启动的提示Modal -->
  <a-modal
    v-model:open="showWeightStateErrorModal"
    centered
    title="是否尝试重启电子秤？"
    :okText="'重启'"
    :cancelText="'取消'"
    @ok="onClickWeightStateErrorOk"
    :confirmLoading="weightStateErrorModalLoading"
    :maskClosable="false"
    :keyboard="false"
  >
    <p>电子秤未能正常启动，请尝试重启</p>
  </a-modal>
</template>

<script lang="ts" setup>
//#####################################第三方库及定义类初始化#####################################
import {
  ref,
  reactive,
  onMounted,
  UnwrapRef,
  computed,
  watch,
  onUpdated,
} from "vue";
// import { useRouter } from "vue-router";
import {
  useOptionStore,
  useStateStore,
  useUserStore,
  useCameraStore,
} from "@/stores/store";
import { MenuUnfoldOutlined, FormOutlined } from "@ant-design/icons-vue";
import { StepProps, message, Modal } from "ant-design-vue";
import type { Rule } from "ant-design-vue/es/form"; // 引入表单验证规则Rule组件
import axios from "@/config/axios-config"; // 引入axios库，用于http请求
import {
  searchOption, // 镜架检索信息
  EyeGlassBasicForm, // 镜架基础参数接口
  // EyeGlassStyleForm, // 镜架风格参数接口
  EyeGlassDetailForm, // 镜架详细参数接口
  EyeGlassDetailFormLabel, // 镜架详细参数标签
  EyeGlassDetailToviewFormLabel, // 镜架详细参数转视图参数标签
  EyeGlassDetailFormUnit, // 镜架详细参数转视图参数单位标签
  // EyeGlassWeightForm, // 镜架重量参数接口
  // EyeGlassWeightFormUnit, // 镜架重量参数单位标签
  EyeGlassImageForm, // 镜架图像参数接口
  EyeGlassImageBackgroundForm,
  EyeGlassBasicFormUnit, // 镜架图像背景参数接口
} from "./params";
import { initFormOptions } from "./utils";

//#########################################参数初始化###########################################
// const router = useRouter();
const state = useStateStore();
const options = useOptionStore();
const user = useUserStore();
const camera = useCameraStore();
// 父组件传递参数接口
interface scanPageProps {
  goToManage: () => void; //跳转到镜架管理页面
}
// 父组件传递参数实例
const props = withDefaults(defineProps<scanPageProps>(), {
  goToManage: () => {},
});

// 主界面状态
const currentStage = ref<
  "input-sku" | "input-basic-params" | "preview" | "confirm" | "input-params"
>("input-sku");
const hasCaptured = ref(false); // 是否已经拍摄

// 镜架检索信息
const searchString = ref(""); // 镜架检索信
const searchOptions = ref<searchOption[]>([]); // 镜架检索信息
const skuormodeltype = ref<number>(1);

// 镜架拍摄html信息接口
interface CaptureItem {
  videoElement: HTMLVideoElement; //预览时的html视频元素
  imgurl: string; //拍摄结果
  imgBlob: Blob | null; //拍摄结果
}

// 镜架拍摄html信息：0 俯视图；1 正视图；2 侧视图
const TopCapture = ref<CaptureItem>({
  videoElement: document.querySelector(
    "video[name='TopVideo']",
  ) as HTMLVideoElement,
  imgurl: "",
  imgBlob: null,
});
const FrontCapture = ref<CaptureItem>({
  videoElement: document.querySelector(
    "video[name='FrontVideo']",
  ) as HTMLVideoElement,
  imgurl: "",
  imgBlob: null,
});
const SideCapture = ref<CaptureItem>({
  videoElement: document.querySelector(
    "video[name='SideVideo']",
  ) as HTMLVideoElement,
  imgurl: "",
  imgBlob: null,
});

const enabledSubmitButton = ref<boolean>(false); // 是否可以提交，在input-params阶段，只有所有参数都填写了才能提交

// Websocket连接实例键值对
const wsMap = ref<Map<string, WebSocket>>(new Map());

// select和autocompe下拉框选项接口定义
interface Option {
  value: string;
  label: string;
}

//详细信息modal 相关
const showDetailModal = ref<boolean>(false);
const isInputEditable = ref<string>("");

// 设备状态
const cameraState = ref<boolean>(false);

// 摄像头状态错误modal
const showCameraStateErrorModal = ref<boolean>(false);
const cameraStateErrorModalLoading = ref<boolean>(false);

// 秤状态错误modal
const showWeightStateErrorModal = ref<boolean>(false);
const weightStateErrorModalLoading = ref<boolean>(false);

//#########################################参数初始化--表单数据###########################################
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
  stock: null,
  is_transparent: null,
  frame_type: null,
  lens_radian: null,
  lens_width_st: null,
  bridge_width_st: null,
  temple_length_st: null,
  weight: "",
});

// 镜架基础参数表单数据
const EyeGlassBasicFormState: UnwrapRef<EyeGlassBasicForm> = reactive({
  sku: "",
  brand: "",
  model_type: "",
  price: null,
  material: null,
  color: null,
  shape: null,
  isnosepad: null,
  stock: null,
  is_transparent: null,
  frame_type: null,
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
    {
      required: true,
      message: "请输入撑片弧度",
      trigger: ["blur", "change"],
    },
    {
      message: "撑片弧度格式错误",
      type: "number",
      max: 9999999999.9999,
      min: -9999999999.9999,
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
      message: "镜片宽度格式错误",
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
      message: "鼻梁宽度格式错误",
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
      message: "镜腿长度格式错误",
      type: "number",
      max: 9999999999.9999,
      min: 0,
      trigger: ["blur", "change"],
    },
  ],
};

// // 镜架风格参数表单实例
// const EyeGlassStyleFormRef = ref();
// // 镜架风格参数表单初始化数据
// const EyeGlassStyleFormInitState: UnwrapRef<EyeGlassStyleForm> = reactive({
//   style: [1],
// });
// // 镜架风格参数表单数据
// const EyeGlassStyleFormState: UnwrapRef<EyeGlassStyleForm> = reactive({
//   style: [1],
// });
// // 镜架风格参数表单校验规则
// const EyeGlassStyleFormRules: Record<string, Rule[]> = {
//   style: [
//     { required: true, message: "请选择镜框风格", trigger: ["blur", "change"] },
//   ],
// };
// modal展示的镜架详细参数表单实例
const EyeGlassDetailModelFormRef = ref();
// modal展示的镜架详细参数表单初始化数据
const EyeGlassDetailModelFormInitState: UnwrapRef<EyeGlassDetailForm> =
  reactive({
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
// modal展示的镜架详细参数表单数据，用于弃用和保存修改
const EyeGlassDetailModelFormState: UnwrapRef<EyeGlassDetailForm> = reactive({
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

// 镜架重量参数标识符
const hasWeightLoged = ref<boolean>(false);
// 镜架重量参数表单实例
const EyeGlassWeightFormRef = ref();
// 镜架重量参数表单初始化数据
const EyeGlassWeightFormInitState = reactive({
  weight: "",
});
// 镜架重量参数表单数据
const EyeGlassWeightFormState = reactive({
  weight: "",
});
// 镜架重量参数表单校验规则
const EyeGlassWeightFormRules: Record<string, Rule[]> = {
  weight: [
    { required: true, message: "请记录镜框重量", trigger: ["blur", "change"] },
  ],
};

// 镜架图像参数表单初始化数据
const EyeGlassImageFormInitState: UnwrapRef<EyeGlassImageForm> = reactive({
  frontview: null,
  topview: null,
  sideview: null,
});
// 镜架图像参数表单数据
const EyeGlassImageFormState: UnwrapRef<EyeGlassImageForm> = reactive({
  frontview: null,
  topview: null,
  sideview: null,
});
// 镜架图像背景表单数据
const EyeGlassImageBackgroundFormState: UnwrapRef<EyeGlassImageBackgroundForm> =
  reactive({
    frontview_bg: null,
    topview_bg: null,
    sideview_bg: null,
  });

// #########################################生命周期函数############################################
// 生命周期钩子：组件挂载完成后执行
onMounted(() => {
  // 初始化表单Options
  initFormOptions();
  // 初始化摄像头模组
  initCamera();
  // 初始化识别秤串口
  initWeight();
  // 初始化摄像头
  (TopCapture.value.videoElement = document.querySelector(
    "video[name='TopVideo']",
  ) as HTMLVideoElement),
    (FrontCapture.value.videoElement = document.querySelector(
      "video[name='FrontVideo']",
    ) as HTMLVideoElement);
  SideCapture.value.videoElement = document.querySelector(
    "video[name='SideVideo']",
  ) as HTMLVideoElement;
});

// 生命周期钩子：组件因为响应式状态变更而更新其 DOM 树之后调用
onUpdated(() => {
  // 在preview页面获取元素
  if (currentStage.value === "preview") {
    // 初始化摄像头
    TopCapture.value.videoElement = document.querySelector(
      "video[name='TopVideo']",
    ) as HTMLVideoElement;
    FrontCapture.value.videoElement = document.querySelector(
      "video[name='FrontVideo']",
    ) as HTMLVideoElement;
    SideCapture.value.videoElement = document.querySelector(
      "video[name='SideVideo']",
    ) as HTMLVideoElement;
  }
});
// ##############################################监视函数############################################
watch(currentStage, (currentStage) => {
  if (currentStage !== "input-sku") {
    state.allowMenuSwitch = "scaning"; //正在录入，则不允许切换菜单
  } else {
    state.allowMenuSwitch = "allow";
  }
});

// #########################################静态功能函数定义############################################
// 功能函数：selct和auto-complete的输入框和option不区分大小写
const filterOptionbyValue = (input: string, option: Option) => {
  // 判断option中是否为空
  if (!option.value) {
    return false;
  } else {
    return option.value.toUpperCase().indexOf(input.toUpperCase()) >= 0;
  }
};

/// 功能函数：发送websocket请求，设置摄像头参数；前端读取摄像头配置，并初始化摄像头
async function initCamera(): Promise<boolean> {
  // 发送初始化摄像头请求
  const ws = new WebSocket(`ws://localhost:8765/init-camera-usb`);
  // 监听返回消息
  ws.addEventListener("message", (event) => {
    const result = JSON.parse(event.data as string);
    // 判断返回的code值，若为-1则提示摄像头启动失败
    if (result.code == "-1") {
      // 设置摄像头状态为false
      cameraState.value = false;
      cameraStateErrorModalLoading.value = false;
      message.error("摄像头启动失败，请检查设备连接", 10);
    } else {
      // 设置摄像头状态为true
      cameraState.value = true;
      // 关闭摄像头状态错误提示框
      showCameraStateErrorModal.value = false;
      // 关闭摄像头状态错误提示框的Loading
      cameraStateErrorModalLoading.value = false;
      // 提示摄像头启动成功
      message.success("摄像头启动成功", 5);
    }
    ws.close();
  });
  // 监听错误事件;
  ws.addEventListener("error", () => {
    message.error("摄像头启动失败，请检查设备连接", 10);
    ws.close();
    return false;
  });
  // 清空设备列表
  await initCameraDeviceState();
  // 检查可用的媒体输入和输出设备的列表
  if (!navigator.mediaDevices || !navigator.mediaDevices.enumerateDevices) {
    // 报告检查错误
    console.log("浏览器不支持mediaDevices");
    return false;
  }
  // navigator.mediaDevices.getUserMedia({ video: true });
  // 获取设备列表
  await navigator.mediaDevices
    .enumerateDevices()
    .then(function (devices) {
      console.log("设备列表", devices);
      // 解析设备列表
      devices.forEach(function (device) {
        // 判断设备类型是否为videoinput，并且设备label拥有相同的设备名和VID
        if (
          device.kind === "videoinput" &&
          device.label.includes("16MP USB Camera (32e4:0009)")
        ) {
          // 添加设备到设备列表
          camera.cameraState.cameraList.push({
            index: 0,
            kind: device.kind,
            label: device.label,
            deviceId: device.deviceId,
            mediaStream: null, // 设备流对象
          });
        } else if (
          device.kind === "videoinput" &&
          device.label.includes("16MP USB Camera (32e4:0001)")
        ) {
          // 添加设备到设备列表
          camera.cameraState.cameraList.push({
            index: 1,
            kind: device.kind,
            label: device.label,
            deviceId: device.deviceId,
            mediaStream: null, // 设备流对象
          });
        } else if (
          device.kind === "videoinput" &&
          device.label.includes("16MP USB Camera (32e4:0002)")
        ) {
          // 添加设备到设备列表
          camera.cameraState.cameraList.push({
            index: 2,
            kind: device.kind,
            label: device.label,
            deviceId: device.deviceId,
            mediaStream: null, // 设备流对象
          });
        }
      });
    })
    .catch(function (err) {
      // 报告错误
      console.log(err.name + ": " + err.message);
      // 若遇到错误，则重置设备列表
      initCameraDeviceState();
      // 返回初始化失败
      // 设置摄像头状态为true
      // cameraState.value = true;
      // 关闭摄像头状态错误提示框
      showCameraStateErrorModal.value = false;
      // 关闭摄像头状态错误提示框的Loading
      cameraStateErrorModalLoading.value = false;
      // 提示摄像头启动成功
      message.success("摄像头启动成功", 5);
      return false;
    });
  // 判断设备列表是否为空
  if (camera.cameraState.cameraList.length === 0) {
    // 报告错误
    console.log("未找到可用摄像头设备");
    // 重置设备列表
    initCameraDeviceState();
    // message.error("未找到可用摄像头设备");
    return false;
  }
  // 判断设备不足
  if (camera.cameraState.cameraList.length < 3) {
    // 报告错误
    console.log("摄像头设备不足");
    // 重置设备列表
    initCameraDeviceState();
    return false;
  }
  // 设置摄像头设备初始化状态
  camera.cameraState.cameraInitState = true;
  // 返回初始化成功
  return true;
}

// 功能函数，初始化摄像头设备
async function initCameraDeviceState(): Promise<void> {
  // 重置摄像头设备初始化状态
  camera.cameraState.cameraInitState = false;
  // 重置摄像头设备列表
  camera.cameraState.cameraList = [];
}

// 功能函数：开始拍摄预览
async function startCameraStream(): Promise<void> {
  // 遍历摄像头列表，获取摄像头流
  camera.cameraState.cameraList.forEach((camera) => {
    console.log(camera);
    navigator.mediaDevices
      .getUserMedia({
        // 设置摄像头参数
        // todo:测试参数
        video: {
          deviceId: camera.deviceId,
          // width: { min: 3500, ideal: 3570, max: 3600 },
          // height: { min: 3400, ideal: 3496, max: 3500 },
          // frameRate: { ideal: 25 },
        },
      })
      .then(function (stream) {
        // 将流对象存入摄像头对象
        camera.mediaStream = stream;
        // 根据摄像头索引，将流对象赋值给对应的video元素
        if (camera.index == 0) {
          if (TopCapture.value.videoElement) {
            // 将流对象赋值给video元素
            TopCapture.value.videoElement.srcObject = stream;
            // 监听视频流元数据加载完成后，播放视频
            TopCapture.value.videoElement.onloadedmetadata = function () {
              TopCapture.value.videoElement.play();
            };
          }
        } else if (camera.index == 1) {
          if (FrontCapture.value.videoElement) {
            // 将流对象赋值给video元素
            FrontCapture.value.videoElement.srcObject = stream;
            // 监听视频流元数据加载完成后，播放视频
            FrontCapture.value.videoElement.onloadedmetadata = function () {
              FrontCapture.value.videoElement.play();
            };
          }
        } else if (camera.index == 2) {
          if (SideCapture.value.videoElement) {
            // 将流对象赋值给video元素
            SideCapture.value.videoElement.srcObject = stream;
            // 监听视频流元数据加载完成后，播放视频
            SideCapture.value.videoElement.onloadedmetadata = function () {
              SideCapture.value.videoElement.play();
            };
          }
        }
      })
      .catch(function (err) {
        console.log(err.name + ": " + err.message);
      });
  });
}

// 功能函数：进行拍摄，结果存入url,blob和 EyeGlassImageFormState 中；关闭视频流
async function CameraCapture(): Promise<void> {
  // 遍历摄像头列表，关闭视频流
  const promises = camera.cameraState.cameraList.map(async (camera) => {
    // 判断是否有视频流
    if (camera.mediaStream) {
      // 开启拍摄
      const canvas = document.createElement("canvas");
      // todo:调整图像大小（和摄像头参数一致）
      canvas.width = 4656;
      canvas.height = 3496;
      const ctx = canvas.getContext("2d");
      ctx?.scale(-1, 1);
      ctx?.translate(-canvas.width, 0);
      try {
        let blob: Blob | null = null;
        if (camera.index === 0) {
          ctx?.drawImage(
            TopCapture.value.videoElement,
            0,
            0,
            canvas.width,
            canvas.height,
          );
          // 将canvas内容转换为Blob
          blob = await new Promise<Blob | null>((resolve) =>
            canvas.toBlob(resolve, "image/jpeg", 0.8),
          );
          if (!blob) {
            console.error("截取视频帧失败");
            throw new Error("截取视频帧失败");
          } else {
            // 将Blob转化为URL，赋值给imgFrontCameraUrl
            TopCapture.value.imgurl = URL.createObjectURL(blob);
            // 存储blob在imgFrontCameraBlob中
            TopCapture.value.imgBlob = blob;
            // 将Blob转换为File对象
            EyeGlassImageFormState.topview = new File([blob], "0.jpg");
          }
        } else if (camera.index === 1) {
          ctx?.drawImage(
            FrontCapture.value.videoElement,
            0,
            0,
            canvas.width,
            canvas.height,
          );
          // 将canvas内容转换为Blob
          blob = await new Promise<Blob | null>((resolve) =>
            canvas.toBlob(resolve, "image/jpeg", 0.8),
          );
          if (!blob) {
            console.error("截取视频帧失败");
            throw new Error("截取视频帧失败");
          } else {
            // 将Blob转化为URL，赋值给imgFrontCameraUrl
            FrontCapture.value.imgurl = URL.createObjectURL(blob);
            // 存储blob在imgFrontCameraBlob中
            FrontCapture.value.imgBlob = blob;
            // 将Blob转换为File对象
            EyeGlassImageFormState.frontview = new File([blob], "0.jpg");
          }
        } else if (camera.index === 2) {
          ctx?.drawImage(
            SideCapture.value.videoElement,
            0,
            0,
            canvas.width,
            canvas.height,
          );
          // 将canvas内容转换为Blob
          blob = await new Promise<Blob | null>((resolve) =>
            canvas.toBlob(resolve, "image/jpeg", 0.8),
          );
          if (!blob) {
            console.error("截取视频帧失败");
            throw new Error("截取视频帧失败");
          } else {
            // 将Blob转化为URL，赋值给imgFrontCameraUrl
            SideCapture.value.imgurl = URL.createObjectURL(blob);
            // 存储blob在imgFrontCameraBlob中
            SideCapture.value.imgBlob = blob;
            // 将Blob转换为File对象
            EyeGlassImageFormState.sideview = new File([blob], "0.jpg");
          }
        }
      } catch (error) {
        // 捕获异常
        console.log(error);
        throw new Error("截取视频帧失败");
      } finally {
        // 清除创建的canvas
        canvas.remove();
      }
    } else {
      throw new Error("未获取到视频流");
    }
  });
  // 等待所有摄像头拍摄完成
  await Promise.all(promises)
    .then(() => {
      // 确认拍摄标识符
      hasCaptured.value = true;
      // 关闭所有视频流
      stopCameraStream();
    })
    .catch((error) => {
      // 一旦发生异常，则清空已经存储的图片
      TopCapture.value.imgurl = "";
      TopCapture.value.imgBlob = null;
      FrontCapture.value.imgurl = "";
      FrontCapture.value.imgBlob = null;
      SideCapture.value.imgurl = "";
      SideCapture.value.imgBlob = null;
      // 清空store中的图片
      EyeGlassImageFormState.frontview = null;
      EyeGlassImageFormState.leftview = null;
      EyeGlassImageFormState.rightview = null;
      // 抛出异常
      console.log(error);
      throw new Error("拍摄失败");
    });
}

// 功能函数：关闭所有摄像头视频流
const stopCameraStream = () => {
  // 关闭所有视频流
  camera.cameraState.cameraList.forEach((camera) => {
    if (camera.mediaStream) {
      camera.mediaStream.getTracks().forEach((track) => {
        track.stop();
      });
      console.log("关闭视频流");
      camera.mediaStream = null;
    }
  });
};

// 功能函数：初始化电子秤
const initWeight = () => {
  // 发送初始化称重请求
  const ws = new WebSocket(`ws://localhost:8765/init-weight`);
  // 监听返回消息
  ws.addEventListener("message", (event) => {
    const result = JSON.parse(event.data as string);
    // 重置秤状态错误Modal提示Loading
    weightStateErrorModalLoading.value = false;
    // 判断返回的code值，若为-1则提示称重启动失败
    if (result.code == "-1") {
      message.error("电子秤启动失败，请检查设备连接", 5);
    } else {
      message.success("电子秤启动成功", 5);
      // 显示秤状态错误Modal提示
      showWeightStateErrorModal.value = false;
    }
    ws.close();
  });
  // 监听错误事件
  ws.addEventListener("error", () => {
    message.error("电子秤启动失败，请检查设备连接", 10);
    ws.close();
  });
};

const uploadNewEyeglassFrame = async () => {
  // 验证通过标识符
  let isFormValid = true;
  // 检查镜架基础信息是否完善
  await EyeGlassBasicFormRef.value.validate().catch(() => {
    message.error("请完善镜架基础信息");
    isFormValid = false;
  });
  // 检查镜架重量信息是否完善
  await EyeGlassWeightFormRef.value.validate().catch(() => {
    message.error("请完善镜架重量信息");
    isFormValid = false;
  });
  // 检查镜架图片信息是否完善
  if (!Object.values(EyeGlassImageFormState).every((image) => image !== null)) {
    message.error("镜架三视图信息错误");
    isFormValid = false;
  }
  // 检查镜架采集仓库地址是否完善
  if (!user.warehouse) {
    message.error("请完善镜架采集仓库地址");
    isFormValid = false;
  }
  if (!isFormValid) {
    return false;
  }
  // 构建FormData对象
  const formData = new FormData();
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
  // 数据库字段isnosepad为BooleanField类型，当isnosepad!==null时，后端会同意验证为True。因此，此处做特殊处理
  formData.append(
    "isnosepad",
    EyeGlassBasicFormState.isnosepad
      ? EyeGlassBasicFormState.isnosepad.toString()
      : "",
  );
  console.log(EyeGlassBasicFormState.is_transparent);
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
  // 将镜架重量信息添加到FormData对象
  formData.append("weight", EyeGlassWeightFormState.weight);
  // 将镜架图片信息添加到FormData对象
  formData.append("frontview", EyeGlassImageFormState.frontview as File);
  formData.append("sideview", EyeGlassImageFormState.sideview as File);
  formData.append("topview", EyeGlassImageFormState.topview as File);
  // 提交通过标识符
  let isSaveSuccess: boolean = false;
  await axios
    .post("/glassmanagement/api/upload-new-eyeglassframe", formData)
    .then((response) => {
      console.log(response);
    });
  return isSaveSuccess;
};

// 功能函数：发送图片、基础参数和详细参数到服务器
const saveNewEyeglassFrame = async () => {
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
  // await EyeGlassDetailFormRef.value.validate().catch(() => {
  //   message.error("请完善镜架详细信息");
  //   isFormValid = false;
  // });
  // 检查镜架重量信息是否完善
  await EyeGlassWeightFormRef.value.validate().catch(() => {
    message.error("请完善镜架重量信息");
    isFormValid = false;
  });
  // 检查镜架图片信息是否完善
  // if (!Object.values(EyeGlassImageFormState).every((image) => image !== null)) {
  //   message.error("镜架三视图信息错误");
  //   isFormValid = false;
  // }
  // 检查镜架图片背景信息是否完善
  if (
    !Object.values(EyeGlassImageBackgroundFormState).every(
      (image) => image !== null,
    )
  ) {
    message.error("镜架三视图背景信息错误");
    isFormValid = false;
  }
  // 检查镜架采集仓库地址是否完善
  if (!user.warehouse) {
    message.error("请完善镜架采集仓库地址");
    isFormValid = false;
  }
  if (!isFormValid) {
    return false;
  }
  // 构建FormData对象
  const formData = new FormData();
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
  // 数据库字段isnosepad为BooleanField类型，当isnosepad!==null时，后端会同意验证为True。因此，此处做特殊处理
  formData.append(
    "isnosepad",
    EyeGlassBasicFormState.isnosepad
      ? EyeGlassBasicFormState.isnosepad.toString()
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
  // 将镜架风格信息添加到FormData对象
  // formData.append("style", JSON.stringify(EyeGlassStyleFormState.style));
  // 将镜架详细信息添加到FormData对象
  // Object.entries(EyeGlassDetailFormState).forEach(([key, value]) => {
  //   formData.append(key, value); // 将值转换为字符串后添加
  // });
  // 将镜架重量信息添加到FormData对象
  formData.append("weight", EyeGlassWeightFormState.weight);
  // 将镜架图片信息添加到FormData对象
  // formData.append("frontview", EyeGlassImageFormState.frontview as File);
  // formData.append("sideview", EyeGlassImageFormState.sideview as File);
  // formData.append("topview", EyeGlassImageFormState.topview as File);
  // 将镜架图片背景信息添加到FormData对象
  // formData.append(
  //   "frontview_bg",
  //   EyeGlassImageBackgroundFormState.frontview_bg as File,
  // );
  // formData.append(
  //   "sideview_bg",
  //   EyeGlassImageBackgroundFormState.sideview_bg as File,
  // );
  // formData.append(
  //   "topview_bg",
  //   EyeGlassImageBackgroundFormState.topview_bg as File,
  // );
  // 提交通过标识符
  let isSaveSuccess: boolean = false;
  // 发送请求
  await axios
    .post("/glassmanagement/api/generate-calculate-task", formData)
    .then((response) => {
      // 判断返回的code值，若为-1则提示无镜架信息
      if (response.data.code === -1) {
        message.error("镜架保存失败");
        isSaveSuccess = false;
      } else {
        message.success("镜架信息保存成功");
        // 重置所有表单和状态
        initAll();
        isSaveSuccess = true;
      }
    })
    .catch((error) => {
      console.log(error);
      isSaveSuccess = false;
    });
  return isSaveSuccess;
};

// 功能函数：访问WebSocket，读取称重结果
const readWeight = () => {
  const ws = new WebSocket(`ws://localhost:8765/read-weight`);
  ws.addEventListener("message", (event) => {
    const result = JSON.parse(event.data as string);
    if (result.code == "-1") {
      // 显示秤状态错误Modal提示
      showWeightStateErrorModal.value = true;
      // 将称重状态置为true
      hasWeightLoged.value = true;
      ws.close();
    } else {
      // 显示秤状态错误Modal提示
      showWeightStateErrorModal.value = false;
      EyeGlassWeightFormState.weight = result.data as string;
    }
  });
  // 监听错误事件
  ws.addEventListener("error", () => {
    message.error("读取称重结果失败，请检查设备连接", 10);
    ws.close();
  });
  wsMap.value.set("weight", ws);
};

// 功能函数：访问WebSocket，计算镜架参数
// const calculateParamsAndStyles = () => {
//   // 计算参数loading提示
//   const calculatingmessage = message.loading("正在计算参数和风格", 0);
//   // 访问WebSocket，计算镜架参数
//   const ws = new WebSocket(`ws://localhost:8765/calc-frame`);
//   // 监听WebSocket消息
//   ws.addEventListener("message", (event) => {
//     // 解析返回的参数
//     const result = JSON.parse(event.data as string);
//     if (result.code == "-1") {
//       // 显示相机状态错误Modal提示
//       showCameraStateErrorModal.value = true;
//       // 将相机状态置为false
//       cameraState.value = false;
//       // 移除计算参数loading提示
//       calculatingmessage();
//     } else {
//       const calculated_params = result.data;
//       // 判断计算结果flag，若为false则提示计算失败
//       if (calculated_params["flag"] === 0) {
//         // 将计算参数赋值给EyeGlassDetailFormState表单
//         Object.entries(EyeGlassDetailFormState).forEach(([key]) => {
//           if (key in calculated_params) {
//             EyeGlassDetailFormState[key] = calculated_params[key];
//           }
//         });
//         // 将提交按钮置为可用
//         enabledSubmitButton.value = true;
//         // 移除计算参数loading提示
//         calculatingmessage();
//         // 提示计算失败
//         message.success("计算镜架参数成功", 5);
//       } else {
//         // 将计算参数赋值给EyeGlassDetailFormState表单
//         Object.entries(EyeGlassDetailFormState).forEach(([key]) => {
//           if (key in calculated_params) {
//             EyeGlassDetailFormState[key] = calculated_params[key];
//           }
//         });
//         // 将提交按钮置为可用
//         enabledSubmitButton.value = true;
//         // 移除计算参数loading提示
//         calculatingmessage();
//         message.success("计算镜架参数成功", 5);
//       }
//     }
//     ws.close();
//   });
//   // 监听错误事件
//   ws.addEventListener("error", () => {
//     message.error("参数计算失败，请检查设备连接", 10);
//     ws.close();
//   });

//   // 计算镜架风格，todo：未来要用websocket或http请求去计算
//   // EyeGlassStyleFormState.style = [1];
// };

// 功能函数：清楚摄像头缓存
const clearCameraCache = async () => {
  // 发送清除缓存的请求
  const ws = new WebSocket(`ws://localhost:8765/clear-camera-cache`);
  // 监听返回消息
  ws.addEventListener("message", () => {
    ws.close();
  });
  // 监听错误事件
  ws.addEventListener("error", () => {
    ws.close();
  });
};

// 功能函数：初始化基础参数表单
const initEyeGlassBasicFormState = () => {
  Object.assign(EyeGlassBasicFormState, EyeGlassBasicFormInitState);
};

// 功能函数：初始化详细参数模态框表单
const initEyeGlassDetailModelFormState = () => {
  Object.assign(EyeGlassDetailModelFormState, EyeGlassDetailModelFormInitState);
};

// 功能函数：初始化重量参数表单
const initEyeGlassWeightFormState = () => {
  Object.assign(EyeGlassWeightFormState, EyeGlassWeightFormInitState);
};

// 功能函数：初始化图像参数表单
const initEyeGlassImageFormState = () => {
  Object.assign(EyeGlassImageFormState, EyeGlassImageFormInitState);
};

// 功能函数：初始化Capture
const initCapture = () => {
  TopCapture.value.imgBlob = null;
  TopCapture.value.imgurl = "";
  FrontCapture.value.imgBlob = null;
  FrontCapture.value.imgurl = "";
  SideCapture.value.imgBlob = null;
  SideCapture.value.imgurl = "";
  hasCaptured.value = false;
};

// 功能函数：初始化所有表单和状态
const initAll = () => {
  initEyeGlassBasicFormState();
  // initEyeGlassStyleFormState();
  // initEyeGlassDetailFormState();
  initEyeGlassWeightFormState();
  initEyeGlassImageFormState();
  initCapture();
  // initEyeGlassImageUrlState();
  hasWeightLoged.value = false;
  wsMap.value.forEach((ws) => {
    ws?.close();
  });
};

// 功能函数：计算参数，校验界面是否处于拍摄预览
// const isCaptureStart = computed(() => {
//   if (
//     currentStage.value == "preview-0" ||
//     currentStage.value == "preview-1" ||
//     currentStage.value == "preview-2"
//   ) {
//     return true;
//   } else {
//     return false;
//   }
// });

// #########################################OnClick点击事件函数定义#########################################

// 镜架信息检索类型选择点击事件
const onChangeSKUorModeltype = () => {
  // 在切换检索类型时，清空searchString和searchOptions
  searchString.value = "";
  searchOptions.value = [];
  // 同时清空镜架信息表单
  initEyeGlassBasicFormState();
};

// 镜架信息检索搜索按钮点击事件
const onSearchModeltypeOrSKU = async (value: string) => {
  // 清空searchOptions
  searchOptions.value = [];
  // 判断检索类型，并判断输入参数是否为空
  if (skuormodeltype.value == 1) {
    if (value == "") {
      message.warning("请输入镜框型号");
      return;
    }
    EyeGlassBasicFormState.model_type = value;
  } else if (skuormodeltype.value == 2) {
    if (value == "") {
      message.warning("请输入镜框SKU");
      return;
    }
    EyeGlassBasicFormState.sku = value;
  }
  // 若不为空，则进行FormData构造，并请求检索
  const formData = new FormData();
  formData.append("skuormodeltype", String(skuormodeltype.value));
  formData.append("searchString", value);
  await axios
    .post(`/glassmanagement/api/search-modeltype-sku`, formData)
    .then((response) => {
      // 判断返回的code值,若为-1则提示参数为空
      if (response.data["code"] == 0) {
        if (response.data["data"]) {
          // 将查询到的信息赋值给searchOptions
          searchOptions.value = response.data["data"];
        } else {
          // 重置searchOptions
          searchOptions.value = [];
        }
      }
    })
    .catch((error) => {
      console.log(error);
    });
};

// 镜架信息检索选择点击事件
const onSelectModeltypeOrSKU = (value: string, option: searchOption) => {
  // 将选择的型号或SKU赋值给searchString
  searchString.value = value;
  // 将选择的镜架信息赋值给EyeGlassBasicFormState
  EyeGlassBasicFormState.sku = option.sku;
  EyeGlassBasicFormState.model_type = option.model_type;
  // 清空searchOptions
  searchOptions.value = [];
  onClickEnterSKU();
};

// 输入SKU确认按钮点击事件
const onClickEnterSKU = async () => {
  // 判断检索类型是否为SKU
  if (skuormodeltype.value == 2) {
    EyeGlassBasicFormState.sku = searchString.value;
  }
  // 判断输入参数是否为空
  if (EyeGlassBasicFormState.sku == "") {
    message.warning("请输入镜架SKU或选择镜架条目");
    return;
  }
  // 若输入参数不为空，则发送查询请求
  else {
    await axios
      .get(`/glassmanagement/api/search-sku?sku=${EyeGlassBasicFormState.sku}`)
      .then((response) => {
        // 判断返回的code值,若为-1则提示参数为空
        if (response.data["code"] == -1) {
          // 判断data状态，若返回data，表示镜架已入库
          if (response.data["data"]) {
            Modal.confirm({
              title: "镜架已入库",
              okText: "重新输入SKU",
              cancelText: "查看",
              centered: true,
              content: "该SKU对应镜架已入库，请选择下一步操作",
              onOk: () => {
                // 清空当前sku表单信息
                EyeGlassBasicFormState.sku = "";
              },
              onCancel: () => {
                // 将sku保存在状态管理store中
                // provide("searchSku", EyeGlassBasicFormState.sku);
                state.searchSku = EyeGlassBasicFormState.sku;
                // 清空当前sku表单信息
                EyeGlassBasicFormState.sku = "";
                // 进入镜架查看环节
                props.goToManage();
              },
            });
          } else {
            // 提示输入镜架sku
            message.warning(response.data["msg"]);
          }
        }
        // 若为0则表示镜架未入库
        else {
          // 判断data状态
          if (response.data["data"]) {
            // 提示表单载入成功
            message.success(response.data["msg"]);
            // 将返回的镜架信息赋值给表单
            Object.entries(response.data["data"]).forEach(([key, value]) => {
              if (
                key == "price" ||
                key == "stock" ||
                key == "lens_radian" ||
                key == "lens_width_st" ||
                key == "bridge_width_st" ||
                key == "temple_length_st"
              ) {
                EyeGlassBasicFormState[key] = Number(value);
              } else EyeGlassBasicFormState[key] = value;
            });
            // 进入新镜架入库环节
            currentStage.value = "input-basic-params";
            // 初始化表单Options
            initFormOptions();
          } else {
            // 提示表单载入失败
            message.warning(response.data["msg"]);
            // 进入新镜架入库环节
            currentStage.value = "input-basic-params";
            // 初始化表单Options
            initFormOptions();
          }
        }
      })
      .catch((error) => {
        console.log(error);
      });
  }
};

// 输入基础信息确认按钮点击事件
const onClickEnterBasicParams = () => {
  EyeGlassBasicFormRef.value.validate().then(() => {
    if (hasCaptured.value) {
      currentStage.value = "confirm";
    } else {
      currentStage.value = "preview";
      startCameraStream();
    }
  });
};

// 拍摄或确认按钮点击事件
const onClickCaptureOrConfirm = () => {
  console.log("enableSubmitButton:", enabledSubmitButton.value);
  switch (currentStage.value) {
    case "preview": //预览
      if (camera.cameraState.cameraInitState) {
        // 开启取流，进行预览
        CameraCapture()
          .then(() => {
            currentStage.value = "confirm";
          })
          .catch((error) => {
            // 打开模态窗，展示错误
            showCameraStateErrorModal.value = true;
            cameraStateErrorModalLoading.value = false;
            console.log(error);
          });
      } else {
        // 摄像头未初始化，弹出提示框
        showCameraStateErrorModal.value = true;
      }
      // currentStage.value = "input-params";
      break;
    case "confirm":
      currentStage.value = "input-params";
      if (!hasWeightLoged.value) {
        readWeight();
      }
      break;
    case "input-params": // 计算参数
      // 保存镜框信息成功后进入SKU输入阶段
      uploadNewEyeglassFrame().then((result) => {
        if (result) {
          // 重置提交按钮
          enabledSubmitButton.value = false;
          // 页面跳转至SKU输入阶段
          currentStage.value = "input-sku";
          // 初始化表单Options
          initFormOptions();
          // 初始化镜架检索类型和搜索字符串
          skuormodeltype.value = 1;
          searchString.value = "";
        }
      });
      break;
  }
};

// 返回按钮点击事件
const onClickReturn = () => {
  switch (currentStage.value) {
    case "input-basic-params":
      currentStage.value = "input-sku";
      // 初始化表单Options
      initFormOptions();
      // 重置表单
      initEyeGlassBasicFormState();
      break;
    case "preview":
      // 关闭视频流
      stopCameraStream();
      currentStage.value = "input-basic-params";
      break;
    case "confirm":
      currentStage.value = "input-basic-params";
      break;
    case "input-params":
      // 关闭read-weight的WebSocket
      wsMap.value.get("weight")?.close(1000, "客户端关闭read-weight");
      currentStage.value = "confirm";
      break;
  }
};
// 重拍按钮点击事件
const onClickRedo = () => {
  startCameraStream();
  currentStage.value = "preview";
};

// 功能函数：记录称重结果
const onClickLogWeight = () => {
  const ws = new WebSocket(`ws://localhost:8765/log-weight`);
  ws.addEventListener("message", (event) => {
    const result = JSON.parse(event.data as string);
    if (result.code == "-1") {
      message.error("电子秤未启动", 5);
    }
    ws.close();
  });
  // 监听错误事件
  ws.addEventListener("error", () => {
    message.error("锁定重量失败，请检查设备连接", 10);
    ws.close();
  });
  // 关闭read-weight的WebSocket
  wsMap.value.get("weight")?.close(1000, "客户端关闭read-weight");
  hasWeightLoged.value = true;
};

// 功能函数：取消记录称重结果
const onClickCancelLogWeight = () => {
  // 关闭read-weight的WebSocket
  wsMap.value.get("weight")?.close(1000, "客户端关闭read-weight");
  console.log("取消记录称重结果");
  // 重新读取加载称重结果
  readWeight();
  // 重置hasWeightLoged
  hasWeightLoged.value = false;
};

// 功能函数：清零称重结果
const onClickResetWeight = () => {
  // 使用WebSocket请求清零称重，即去皮
  const ws = new WebSocket(`ws://localhost:8765/reset-weight`);
  ws.addEventListener("message", (event) => {
    const result = JSON.parse(event.data as string);
    if (result.code == "-1") {
      message.error("电子秤未启动", 5);
    }
    ws.close();
  });
  // 监听错误事件
  ws.addEventListener("error", () => {
    message.error("去皮失败，请检查设备连接", 10);
    ws.close();
  });
  // 重置hasWeightLoged
  hasWeightLoged.value = false;
};

// 详细信息模态窗按钮点击事件
// const onClickShowDetailModal = () => {
//   isInputEditable.value = "";
//   showDetailModal.value = true;
//   Object.entries(EyeGlassDetailFormState).forEach(([key, value]) => {
//     EyeGlassDetailModelFormState[key] = value;
//   });
// };

// 详细信息模态窗保存按钮点击事件
// const onClickSaveDetailModal = () => {
//   EyeGlassDetailModelFormRef.value
//     .validate()
//     .then(() => {
//       Object.entries(EyeGlassDetailModelFormState).forEach(([key, value]) => {
//         EyeGlassDetailFormState[key] = value;
//       });
//       initEyeGlassDetailModelFormState();
//       showDetailModal.value = false;
//     })
//     .catch(() => {
//       message.error("请完善镜架详细信息");
//     });
// };

// 详细信息模态窗取消按钮或关闭按钮点击事件
const onClickCancelDetailModal = () => {
  initEyeGlassDetailModelFormState();
  showDetailModal.value = false;
};

// 摄像头状态错误模态窗确定按钮点击事件
const onClickCameraStateErrorOk = () => {
  // 摄像头状态错误modal loading
  cameraStateErrorModalLoading.value = true;
  // 重新初始化摄像头
  initCamera();
};

// 称重状态错误模态窗确定按钮点击事件
const onClickWeightStateErrorOk = () => {
  // 称重状态错误modal loading
  weightStateErrorModalLoading.value = true;
  // 初始化电子秤串口
  initWeight();
};

// 增加亮度
const onClickLightup = () => {
  for (var cam_id = 0; cam_id < 3; cam_id++) {
    // 使用WebSocket请求增加亮度
    const ws = new WebSocket(`ws://localhost:8765/light-up/${cam_id}`);
    ws.addEventListener("message", (event) => {
      const result = JSON.parse(event.data as string);
      if (result.code == "0") {
        message.success("亮度调节完成", 3);
      }
      ws.close();
    });
    // 监听错误事件
    ws.addEventListener("error", () => {
      message.error("亮度未能正常调节，请检查设备连接", 10);
      ws.close();
    });
  }
};
// 降低亮度
const onClickLightdown = () => {
  for (var cam_id = 0; cam_id < 3; cam_id++) {
    // 使用WebSocket请求清零称重，即去皮
    const ws = new WebSocket(`ws://localhost:8765/light-down/${cam_id}`);
    ws.addEventListener("message", (event) => {
      const result = JSON.parse(event.data as string);
      if (result.code == "0") {
        console.log("亮度调节提示");
        message.success("亮度调节完成", 3);
      }
      ws.close();
    });
    // 监听错误事件
    ws.addEventListener("error", () => {
      message.error("亮度未能正常调节，请检查设备连接", 10);
      ws.close();
    });
  }
};
</script>

<style scoped>
.full-height-row {
  height: 100vh;
  background-color: #8675ff;
}
/* 消除所有a-col的padding */
/* a-col */

/* 输入sku */
.sku-form-card {
  width: 790px;
  background-color: #ffffff;
  padding: 120px 100px;
  border-radius: 20px;
  border: 3px solid;
  border-color: #8675ff;
}

.sku-input {
  /* !important：基础信息录入页的sku-input会被calculate-item和basic-item覆盖（原因未知） */
  border-radius: 30px !important;
  border-color: #8675ff !important;
  width: 400px !important;
  height: 58px !important;
  font-size: 14px !important;
  padding: 6.5px 28px !important;
}

.sku-button {
  border-radius: 12px;
  height: 48px;
  width: 400px;
  color: white;
  background-color: #8675ff;
  border: none;
  font-size: 20px;
  margin-top: 48px;
}

/* 镜架检索下拉框 */
.wrap-content {
  white-space: normal;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

/* 输入基础信息 */
.input-basic-form-card {
  width: 980px;
  border: 3px solid #8675ff;
  border-radius: 20px;
  padding: 49px 60px;
  /* display: flex;
  flex-direction: column;
  justify-items: center; */
}

.basic-item {
  min-height: 32px;
  height: fit-content;
  padding: 0 16px;
  margin: 12px;
}

.basic-item :deep(label) {
  font-size: 18px !important;
}

.basic-item :deep(.ant-select-selector),
.ant-input,
.ant-input-number {
  padding-left: 11px;
  width: 100%;
  height: 32px;
  border-radius: 9px;
  font-size: 16px;
}

/* 输入基础信息：消除input-number的重复padding */
.basic-item :deep(.ant-input-number-input) {
  padding: 0;
}

/* 输入基础信息：表单验证提示信息 */
.basic-item :deep(.ant-form-item-explain-connected) {
  position: absolute;
  top: 32px;
}

/* 拍摄 确认 */
.capture-box {
  height: calc(100% - 48px);
  border: none;
  border-radius: 12px;
}

.capture-frame {
  object-fit: contain;
  width: 100%;
  height: 100%;
}
/* 计算参数 */
.registry-preview {
  height: calc(100% - 120px);
  background-color: #ffffff;
}

/* 计算参数 图片预览 */
.registry-preview-sub-image {
  margin: 16px;
  height: calc(100% - 32px);
  width: calc(100% - 32px);
  background-color: #ababab;
  border: none;
  border-radius: 12px;
  object-fit: contain;
}

.calculate-page-title {
  margin: 40px 39.5px 24px;
  font-weight: 700;
  font-size: 40px;
  color: #333333;
}

/* 计算参数：参数栏目 */
.calculate-title {
  font-size: 24px;
  margin: 30px 0 30px 32px;
  color: #666666;
}

.calculate-item {
  margin: 0;
  color: #666666;
  font-size: 20p;
  width: 100%;
}

.calculate-item :deep(label) {
  color: #666666;
}

.calculate-item :deep(.ant-select-selector),
.ant-input {
  padding-left: 11px;
  height: 35px;
  border-radius: 9px;
  font-size: 16px;
  color: #999999;
}

/* 计算参数 基础信息 消除input-number的重复padding */
.calculate-item :deep(.ant-input-number-input) {
  padding: 0;
  color: #999999;
}

/* 计算参数 基础信息 减小radio选项框的大小 */
.calculate-item :deep(.ant-radio-button-wrapper) {
  padding: 0 11px;
}

/* 计算参数 取消表单验证提示信息 */
.calculate-item :deep(.ant-form-item-explain-connected) {
  display: none;
}

/* 操作按钮 */
.registry-operations {
  height: 120px;
}

.operation-button {
  width: 144px;
  height: 60px;
  margin-right: 32px;
  border-radius: 12px;
  background-color: #ababab;
  color: white;
  border: none;
  font-size: 20px;
}

.operation-button-primary {
  width: 144px;
  height: 60px;
  margin-right: 45px;
  border-radius: 12px;
  background-color: #8675ff;
  color: white;
  border: none;
  font-size: 20px;
}

/* 详细信息modal */
.modal-item {
  margin: 0;
  height: 30px;
  font-size: 20px !important;
}

.modal-input {
  height: 30px;
  border-radius: 9px;
  padding-right: 11px;
}
</style>
