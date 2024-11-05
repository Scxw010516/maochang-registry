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
          v-model:value="store.state.skuormodeltype"
          placeholder="选择检索类型"
          placement="topLeft"
          style="width: 70px"
          :options="store.state.options.skuormodeltype_options"
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
            <div v-if="store.state.skuormodeltype == 1">
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
            <div v-else-if="store.state.skuormodeltype == 2">
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
              store.state.skuormodeltype === 1
                ? '请输入镜架型号'
                : '请输入镜架SKU'
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
        :label-col="{ span: 7 }"
        :wrapper-col="{ span: 17 }"
        labelAlign="left"
      >
        <a-form-item name="sku">
          <a-input
            class="sku-input"
            v-model:value="EyeGlassBasicFormState.sku"
            disabled
          ></a-input>
        </a-form-item>
        <div style="height: 550px; overflow: auto">
          <a-form-item label="品牌" name="brand" class="basic-item">
            <a-auto-complete
              v-model:value="EyeGlassBasicFormState.brand"
              :options="store.state.options.brand_options"
              :filter-option="filterOptionbyValue"
              @keyup.enter="onClickEnterBasicParams"
            />
          </a-form-item>
          <a-form-item label="型号" name="model_type" class="basic-item">
            <a-auto-complete
              v-model:value="EyeGlassBasicFormState.model_type"
              :options="store.state.options.model_type_options"
              :filter-option="filterOptionbyValue"
              @keyup.enter="onClickEnterBasicParams"
            />
          </a-form-item>
          <a-form-item label="价格" name="price" class="basic-item">
            <a-input-number
              v-model:value="EyeGlassBasicFormState.price"
              :precision="2"
              :controls="false"
              decimalSeparator="."
              @keyup.enter="onClickEnterBasicParams"
            />
          </a-form-item>
          <a-form-item label="材质" name="material" class="basic-item">
            <a-select
              v-model:value="EyeGlassBasicFormState.material"
              placeholder="选择材质（单选）"
              :options="store.state.options.material_options"
              @keyup.enter="onClickEnterBasicParams"
            />
          </a-form-item>
          <a-form-item label="颜色" name="color" class="basic-item">
            <a-select
              v-model:value="EyeGlassBasicFormState.color"
              placeholder="选择颜色（单选）"
              :options="store.state.options.color_options"
              @keyup.enter="onClickEnterBasicParams"
            />
          </a-form-item>
          <a-form-item label="形状" name="shape" class="basic-item">
            <a-select
              v-model:value="EyeGlassBasicFormState.shape"
              placeholder="选择形状（单选）"
              :options="store.state.options.shape_options"
              @keyup.enter="onClickEnterBasicParams"
            />
          </a-form-item>
          <a-form-item label="鼻托" name="isnosepad" class="basic-item">
            <a-radio-group
              v-model:value="EyeGlassBasicFormState.isnosepad"
              @keyup.enter="onClickEnterBasicParams"
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
          <a-form-item label="库存" name="stock" class="basic-item">
            <a-input-number
              v-model:value="EyeGlassBasicFormState.stock"
              min="0"
              :controls="false"
              @keyup.enter="onClickEnterBasicParams"
            />
          </a-form-item>
          <a-form-item label="撑片弧度" name="lens_radian" class="basic-item">
            <a-input-number
              v-model:value="EyeGlassBasicFormState.lens_radian"
              :controls="false"
              @keyup.enter="onClickEnterBasicParams"
            />
          </a-form-item>
          <a-form-item
            v-show="false"
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
          <a-form-item
            v-show="false"
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
          <a-form-item
            v-show="false"
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
        </div>
        <!-- <a-form-item label="风格" name="style" class="basic-item">
                <a-select
                  v-model:value="EyeGlassBasicFormState.style"
                  mode="multiple"
                  placeholder="选择风格（多选）"
                  :max-tag-count="1"
                  :max-tag-text-length="5"
                  :options="store.state.options.style_options"
                  @keyup.enter="onClickEnterBasicParams"
                />
              </a-form-item> -->
      </a-form>
      <a-button
        style="
          margin-top: 6px;
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
          margin-top: 28px;
          width: 400px;
          height: 56px;
          background-color: #ffffff;
          border-radius: 12px;
          text-align: center;
          justify-content: center;
          color: #8675ff;
          font-size: 18px;
        "
        @click="onClickReturnOrRedo"
      >
        返回
      </a-button>
    </a-col>
  </a-row>
  <!-- 拍摄 -->
  <a-row
    v-else-if="
      currentStage.includes('preview') || currentStage.includes('confirm')
    "
    class="registry-preview"
    type="flex"
    align="middle"
    justify="center"
  >
    <img class="registry-preview-image" :src="imgCameraUrl" />
    <!-- 步骤条 逻辑见stepItems定义处-->
    <div class="steps-line" style="position: absolute; bottom: 140px">
      <a-steps label-placement="vertical">
        <a-step
          v-for="(item, index) in stepItems"
          :key="item"
          :title="item.title"
          :status="
            index < 2 &&
            item.status == 'finish' &&
            stepItems[index + 1].status == 'wait'
              ? 'process'
              : item.status
          "
          @click="onClickStep(index)"
        >
          <template #icon>
            <!-- 白色 -->
            <svg
              v-if="currentStage.includes(index.toString())"
              width="37"
              height="37"
              viewBox="0 0 37 37"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <circle
                cx="18.5"
                cy="18.5"
                r="9.25"
                transform="rotate(90 18.5 18.5)"
                fill="white"
              />
              <circle
                cx="18.5"
                cy="18.5"
                r="17.3438"
                transform="rotate(90 18.5 18.5)"
                stroke="white"
                stroke-width="2.3125"
                stroke-dasharray="4.62 4.62"
              />
            </svg>
            <!-- 紫色 -->
            <svg
              v-else-if="item.status === 'finish'"
              width="37"
              height="37"
              viewBox="0 0 37 37"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <circle
                cx="18.5"
                cy="18.5"
                r="9.25"
                transform="rotate(90 18.5 18.5)"
                fill="#8675FF"
              />
              <circle
                cx="18.5"
                cy="18.5"
                r="17.3438"
                transform="rotate(90 18.5 18.5)"
                stroke="#8675FF"
                stroke-width="2.3125"
                stroke-dasharray="4.62 4.62"
              />
            </svg>

            <!-- 灰色 -->
            <svg
              v-else-if="item.status === 'wait'"
              width="37"
              height="37"
              viewBox="0 0 37 37"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <circle
                cx="18.5"
                cy="18.5"
                r="9.25"
                transform="rotate(90 18.5 18.5)"
                fill="#B4B4B4"
              />
              <circle
                cx="18.5"
                cy="18.5"
                r="17.3438"
                transform="rotate(90 18.5 18.5)"
                stroke="#999999"
                stroke-width="2.3125"
                stroke-dasharray="4.62 4.62"
              />
            </svg>
          </template>
        </a-step>
      </a-steps>
    </div>
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
          <img class="registry-preview-sub-image" :src="imgCameraPreview0Url" />
        </a-col>
        <a-col :span="8">
          <img class="registry-preview-sub-image" :src="imgCameraPreview1Url" />
        </a-col>
        <a-col :span="8">
          <img class="registry-preview-sub-image" :src="imgCameraPreview2Url" />
        </a-col>
      </a-row>
      <!-- 信息展示 -->
      <a-row style="margin-top: 18px">
        <!-- 基础信息 -->
        <a-col :span="24">
          <p class="calculate-title">基础信息</p>
          <!-- 录入的基础信息 -->
          <a-form
            ref="EyeGlassBasicFormRef"
            :model="EyeGlassBasicFormState"
            :rules="EyeGlassBasicFormRules"
            hideRequiredMark
            layout="inline"
            autocomplete="off"
          >
            <a-row
              :gutter="[26, 32]"
              style="margin-left: 40px !important; width: calc(100% - 85px)"
            >
              <a-col :span="6">
                <a-form-item
                  class="calculate-item"
                  label="SKU"
                  name="sku"
                  :labelCol="{ span: 6 }"
                  :wrapperCol="{ span: 18 }"
                  labelAlign="left"
                >
                  <a-input
                    v-model:value="EyeGlassBasicFormState.sku"
                    disabled
                  ></a-input>
                </a-form-item>
              </a-col>
              <a-col :span="6">
                <a-form-item
                  class="calculate-item"
                  label="品牌"
                  name="brand"
                  :labelCol="{ span: 6 }"
                  :wrapperCol="{ span: 18 }"
                  labelAlign="left"
                >
                  <a-auto-complete
                    v-model:value="EyeGlassBasicFormState.brand"
                    :options="store.state.options.brand_options"
                    :filter-option="filterOptionbyValue"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="6">
                <a-form-item
                  class="calculate-item"
                  label="型号"
                  name="model_type"
                  :labelCol="{ span: 6 }"
                  :wrapperCol="{ span: 18 }"
                  labelAlign="left"
                >
                  <a-auto-complete
                    v-model:value="EyeGlassBasicFormState.model_type"
                    :options="store.state.options.model_type_options"
                    :filter-option="filterOptionbyValue"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="6">
                <a-form-item
                  class="calculate-item"
                  label="价格"
                  name="price"
                  :labelCol="{ span: 6 }"
                  :wrapperCol="{ span: 18 }"
                  labelAlign="left"
                >
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
                  :labelCol="{ span: 6 }"
                  :wrapperCol="{ span: 18 }"
                  labelAlign="left"
                >
                  <a-select
                    v-model:value="EyeGlassBasicFormState.material"
                    placeholder="选择材质（单选）"
                    :options="store.state.options.material_options"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="6">
                <a-form-item
                  class="calculate-item"
                  label="颜色"
                  name="color"
                  :labelCol="{ span: 6 }"
                  :wrapperCol="{ span: 18 }"
                  labelAlign="left"
                >
                  <a-select
                    v-model:value="EyeGlassBasicFormState.color"
                    placeholder="选择颜色（单选）"
                    :options="store.state.options.color_options"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="6">
                <a-form-item
                  class="calculate-item"
                  label="形状"
                  name="shape"
                  :labelCol="{ span: 6 }"
                  :wrapperCol="{ span: 18 }"
                  labelAlign="left"
                >
                  <a-select
                    v-model:value="EyeGlassBasicFormState.shape"
                    placeholder="选择形状（单选）"
                    :options="store.state.options.shape_options"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="6">
                <a-form-item
                  class="calculate-item"
                  label="鼻托"
                  name="isnosepad"
                  :labelCol="{ span: 6 }"
                  :wrapperCol="{ span: 18 }"
                  labelAlign="left"
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
                  class="calculate-item"
                  label="库存"
                  name="stock"
                  :labelCol="{ span: 6 }"
                  :wrapperCol="{ span: 18 }"
                  labelAlign="left"
                >
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
                  :labelCol="{ span: 6 }"
                  :wrapperCol="{ span: 18 }"
                  labelAlign="left"
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
                  v-show="false"
                  class="calculate-item"
                  label="镜片宽度"
                  name="lens_width_st"
                  :labelCol="{ span: 6 }"
                  :wrapperCol="{ span: 18 }"
                  labelAlign="left"
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
                  v-show="false"
                  class="calculate-item"
                  label="鼻梁宽度"
                  name="bridge_width_st"
                  :labelCol="{ span: 6 }"
                  :wrapperCol="{ span: 18 }"
                  labelAlign="left"
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
                  v-show="false"
                  class="calculate-item"
                  label="镜腿长度"
                  name="temple_length_st"
                  :labelCol="{ span: 6 }"
                  :wrapperCol="{ span: 18 }"
                  labelAlign="left"
                >
                  <a-input-number
                    class="calculate-input"
                    v-model:value="EyeGlassBasicFormState.temple_length_st"
                    :controls="false"
                  />
                </a-form-item>
              </a-col>
              <!-- <a-col :span="6">
                      <a-form-item
                        class="calculate-item"
                        label="风格"
                        name="style"
                        :labelCol="{ span: 6 }"
                        :wrapperCol="{ span: 18 }"
                        labelAlign="left"
                      >
                        <a-select
                          v-model:value="EyeGlassBasicFormState.style"
                          mode="multiple"
                          placeholder="选择风格（多选）"
                          :max-tag-count="1"
                          :max-tag-text-length="5"
                          :options="store.state.options.style_options"
                        />
                      </a-form-item>
                    </a-col> -->
            </a-row>
          </a-form>
          <!-- 计算用参数 | TODO：正式上线不需要展示 -->
          <!-- <a-form layout="inline" autocomplete="off" style="margin: 8px">
                  <a-form-item
                    class="calculate-item"
                    v-for="(value, key) in EyeGlassCalculateParamsLabel"
                    :label="EyeGlassCalculateParamsLabel[key]"
                    :key="key"
                    :name="key"
                  >
                    <a-input
                      class="calculate-input"
                      v-model:value="EyeGlassCalculateParamsState[key]"
                    ></a-input>
                  </a-form-item>
                </a-form> -->
        </a-col>
        <!-- 详细信息 -->
        <a-col>
          <!-- 详细信息及模态窗按钮 -->
          <p class="calculate-title">
            详细信息
            <MenuUnfoldOutlined
              style="margin-left: 5px; font-size: 20px; color: #666666"
              @click="onClickShowDetailModal"
            />
            <a-button style="margin-left: 30px" @click="onClickCalculateParams">
              计算参数和风格
            </a-button>
          </p>
          <a-row
            :gutter="[26, 32]"
            style="
              margin-left: 40px !important;
              width: calc(100% - 85px);
              margin-bottom: 32px;
            "
          >
            <a-col :span="6">
              <!-- 计算参数：镜架重量 -->
              <a-form
                ref="EyeGlassWeightFormRef"
                :model="EyeGlassWeightFormState"
                :rules="EyeGlassWeightFormRules"
                hideRequiredMark
                layout="inline"
                autocomplete="off"
                :labelCol="{ span: 10 }"
                :wrapperCol="{ span: 14 }"
                labelAlign="left"
              >
                <a-form-item
                  class="calculate-item"
                  label="称重结果"
                  name="weight"
                >
                  <a-input
                    v-model:value="EyeGlassWeightFormState.weight"
                    :suffix="EyeGlassWeightFormUnit.weight"
                    disabled
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
            <a-col :span="6">
              <!-- 镜架风格参数 -->
              <a-form
                ref="EyeGlassStyleFormRef"
                :model="EyeGlassStyleFormState"
                :rules="EyeGlassStyleFormRules"
                hideRequiredMark
                layout="inline"
                autocomplete="off"
                :labelCol="{ span: 10 }"
                :wrapperCol="{ span: 14 }"
                labelAlign="left"
              >
                <a-form-item class="calculate-item" label="风格" name="style">
                  <a-select
                    v-model:value="EyeGlassStyleFormState.style"
                    mode="multiple"
                    placeholder="选择风格（多选）"
                    :max-tag-count="1"
                    :maxTagTextLength="2"
                    :options="store.state.options.style_options"
                  />
                </a-form-item>
              </a-form>
            </a-col>
          </a-row>
          <!-- 计算参数：详细信息 -->
          <a-form
            ref="EyeGlassDetailFormRef"
            :model="EyeGlassDetailFormState"
            :rules="EyeGlassDetailFormRules"
            hideRequiredMark
            layout="inline"
            autocomplete="off"
            :labelCol="{ span: 10 }"
            :wrapperCol="{ span: 14 }"
            labelAlign="left"
          >
            <a-row
              :gutter="[26, 32]"
              style="margin-left: 40px !important; width: calc(100% - 85px)"
            >
              <a-col
                :span="6"
                v-for="(value, key) in EyeGlassDetailToviewFormLabel"
                :key="key"
              >
                <a-form-item :label="value" class="calculate-item" :name="key">
                  <a-input
                    v-model:value="EyeGlassDetailFormState[key]"
                    :suffix="EyeGlassDetailFormUnit[key]"
                    disabled
                  ></a-input>
                </a-form-item>
              </a-col>
            </a-row>
          </a-form>
        </a-col>
      </a-row>
      <!-- 详细信息modal -->
      <a-modal
        width="calc(360*3px + 80*2px + 44*2px)"
        v-model:open="showDetailModal"
        :footer="null"
        @cancel="onClickCancelDetailModal"
      >
        <a-row>
          <p style="margin: 0px 15.5px; font-size: 30px; font-weight: bold">
            详细信息
          </p>
        </a-row>
        <a-form
          ref="EyeGlassDetailModelFormRef"
          :model="EyeGlassDetailModelFormState"
          :rules="EyeGlassDetailFormRules"
          hideRequiredMark
          layout="inline"
          autocomplete="off"
          :labelCol="{ span: 10 }"
          :wrapperCol="{ span: 14 }"
          labelAlign="left"
        >
          <a-row :gutter="[80, 20]" style="margin: 24px 20px">
            <a-col
              :span="8"
              v-for="(value, key) in EyeGlassDetailFormLabel"
              :key="key"
            >
              <a-form-item :label="value" class="modal-item" :name="key">
                <a-input
                  class="modal-input"
                  v-model:value="EyeGlassDetailModelFormState[key]"
                  :disabled="isInputEditable !== EyeGlassDetailFormLabel[key]"
                  :suffix="EyeGlassDetailFormUnit[key]"
                >
                  <template #suffix>
                    <FormOutlined
                      style="color: rgba(0, 0, 0, 0.45)"
                      @click="isInputEditable = EyeGlassDetailFormLabel[key]"
                    />
                  </template>
                </a-input>
              </a-form-item>
            </a-col>
          </a-row>
        </a-form>

        <!-- 详细信息modal：保存按钮 -->
        <a-row width="100%" justify="end">
          <a-button
            style="
              margin: 16px 20px 46.9px;
              right: 0;
              border-radius: 12px;
              width: 100px;
              height: 60px;
              background-color: #8675ff;
              color: #ffffff;
              justify-content: center;
              align-items: center;
              font-size: 16px;
            "
            @click="onClickSaveDetailModal"
          >
            保存
          </a-button>
        </a-row>
      </a-modal>
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
    <div v-show="isCaptureStart" style="margin-left: 80px; margin-right: auto">
      <a-button style="margin-right: 40px" @click="onClickLightup">
        增加亮度
      </a-button>
      <a-button @click="onClickLightdown"> 降低亮度 </a-button>
    </div>
    <a-button class="operation-button" @click="onClickReturnOrRedo"
      >{{
        currentStage.startsWith("preview") || currentStage === "input-params"
          ? "返回"
          : "重拍"
      }}
    </a-button>
    <a-button
      class="operation-button-primary"
      @click="onClickCaptureOrConfirm"
      :disabled="currentStage === 'input-params' && !enabledSubmitButton"
    >
      {{ currentStage.startsWith("preview") ? "拍摄" : "确认" }}
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
import { ref, reactive, onMounted, UnwrapRef, computed, watch } from "vue";
// import { useRouter } from "vue-router";
import { useStore } from "../../store";
import { MenuUnfoldOutlined, FormOutlined } from "@ant-design/icons-vue";
import { StepProps, message, Modal } from "ant-design-vue";
import type { Rule } from "ant-design-vue/es/form"; // 引入表单验证规则Rule组件
import axios from "@/config/axios-config"; // 引入axios库，用于http请求
import {
  searchOption, // 镜架检索信息
  EyeGlassBasicForm, // 镜架基础参数接口
  EyeGlassStyleForm, // 镜架风格参数接口
  EyeGlassDetailForm, // 镜架详细参数接口
  EyeGlassDetailFormLabel, // 镜架详细参数标签
  EyeGlassDetailToviewFormLabel, // 镜架详细参数转视图参数标签
  EyeGlassDetailFormUnit, // 镜架详细参数转视图参数单位标签
  EyeGlassWeightForm, // 镜架重量参数接口
  EyeGlassWeightFormUnit, // 镜架重量参数单位标签
  EyeGlassImageForm, // 镜架图像参数接口
  EyeGlassImageBackgroundForm, // 镜架图像背景参数接口
} from "./params";
import { initFormOptions } from "./utils";
import { withDefaults, defineProps } from "vue"; // 组件传递参数

//#########################################参数初始化###########################################
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
  | "input-sku"
  | "input-basic-params"
  | "preview-0"
  | "preview-1"
  | "preview-2"
  | "confirm-0"
  | "confirm-1"
  | "confirm-2"
  | "input-params"
>("input-sku");

// const router = useRouter();
const store = useStore();

// 镜架检索信息
const searchString = ref(""); // 镜架检索信
const searchOptions = ref<searchOption[]>([]); // 镜架检索信息

const imgCameraUrl = ref<string>(""); // 拍摄过程中的当前页面的图像缓存
const imgCameraPreview0Url = ref<string>(""); // 最后一次性获取的图像,要存储
const imgCameraPreview1Url = ref<string>(""); // 最后一次性获取的图像,要存储
const imgCameraPreview2Url = ref<string>(""); // 最后一次性获取的图像,要存储

const enabledSubmitButton = ref<boolean>(false); // 是否可以提交，在input-params阶段，只有所有参数都填写了才能提交

// Websocket连接实例键值对
const wsMap = ref<Map<string, WebSocket>>(new Map());

// 步骤条相关
// status：存储的步骤状态，与实际渲染的状态不同，仅使用finish(已拍摄)和wait(未拍摄)
// icon：currentStage处于当前步骤为白色；finish为紫色 ，wait为灰色
// tail由 实际渲染步骤状态 控制:
// 此步骤状态 | 下一步骤状态 | 实际渲染状态 | tail颜色
// finish    | finish      | finish      | 紫色
// finish    | wait        | process     | 白色
// wait      | wait        | wait        | 灰色
const stepItems = ref<StepProps[]>([
  {
    title: "俯视图",
    status: "wait",
  },
  {
    title: "正视图",
    status: "wait",
  },
  {
    title: "侧视图",
    status: "wait",
  },
]);

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
  lens_radian: null,
  lens_width_st: null,
  bridge_width_st: null,
  temple_length_st: null,
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
  lens_radian: null,
  lens_width_st: null,
  bridge_width_st: null,
  temple_length_st: null,
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

// 镜架风格参数表单实例
const EyeGlassStyleFormRef = ref();
// 镜架风格参数表单初始化数据
const EyeGlassStyleFormInitState: UnwrapRef<EyeGlassStyleForm> = reactive({
  style: [],
});
// 镜架风格参数表单数据
const EyeGlassStyleFormState: UnwrapRef<EyeGlassStyleForm> = reactive({
  style: [],
});
// 镜架风格参数表单校验规则
const EyeGlassStyleFormRules: Record<string, Rule[]> = {
  style: [
    { required: true, message: "请选择镜框风格", trigger: ["blur", "change"] },
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
const EyeGlassWeightFormInitState: UnwrapRef<EyeGlassWeightForm> = reactive({
  weight: "",
});
// 镜架重量参数表单数据
const EyeGlassWeightFormState: UnwrapRef<EyeGlassWeightForm> = reactive({
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
});
// ##############################################监视函数############################################
watch(currentStage, (currentStage) => {
  if (currentStage !== "input-sku") {
    store.state.allowMenuSwitch = "scaning"; //正在录入，则不允许切换菜单
  } else {
    store.state.allowMenuSwitch = "allow";
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

// 功能函数：初始化摄像头
const initCamera = () => {
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
  // 监听错误事件
  ws.addEventListener("error", () => {
    message.error("摄像头启动失败，请检查设备连接", 10);
    ws.close();
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
  await EyeGlassStyleFormRef.value.validate().catch(() => {
    message.error("请完善镜架风格信息");
    isFormValid = false;
  });
  // 检查镜架详细信息是否完善
  await EyeGlassDetailFormRef.value.validate().catch(() => {
    message.error("请完善镜架详细信息");
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
  if (!store.state.warehouse) {
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
    store.state.warehouse !== null ? store.state.warehouse.toString() : "",
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
  formData.append("style", JSON.stringify(EyeGlassStyleFormState.style));
  // 将镜架详细信息添加到FormData对象
  Object.entries(EyeGlassDetailFormState).forEach(([key, value]) => {
    formData.append(key, value); // 将值转换为字符串后添加
  });
  // 将镜架重量信息添加到FormData对象
  formData.append("weight", EyeGlassWeightFormState.weight);
  // 将镜架图片信息添加到FormData对象
  formData.append("frontview", EyeGlassImageFormState.frontview as File);
  formData.append("sideview", EyeGlassImageFormState.sideview as File);
  formData.append("topview", EyeGlassImageFormState.topview as File);
  // 将镜架图片背景信息添加到FormData对象
  formData.append(
    "frontview_bg",
    EyeGlassImageBackgroundFormState.frontview_bg as File,
  );
  formData.append(
    "sideview_bg",
    EyeGlassImageBackgroundFormState.sideview_bg as File,
  );
  formData.append(
    "topview_bg",
    EyeGlassImageBackgroundFormState.topview_bg as File,
  );
  // 提交通过标识符
  let isSaveSuccess: boolean = false;
  // 发送请求
  await axios
    .post("/glassmanagement/api/save-new-eyeglassframe", formData)
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
const calculateParamsAndStyles = () => {
  // 计算参数loading提示
  const calculatingmessage = message.loading("正在计算参数和风格", 0);
  // 访问WebSocket，计算镜架参数
  const ws = new WebSocket(`ws://localhost:8765/calc-frame`);
  // 监听WebSocket消息
  ws.addEventListener("message", (event) => {
    // 解析返回的参数
    const result = JSON.parse(event.data as string);
    if (result.code == "-1") {
      // 显示相机状态错误Modal提示
      showCameraStateErrorModal.value = true;
      // 将相机状态置为false
      cameraState.value = false;
      // 移除计算参数loading提示
      calculatingmessage();
    } else {
      const calculated_params = result.data;
      // 判断计算结果flag，若为false则提示计算失败
      if (calculated_params["flag"] === 0) {
        // 将计算参数赋值给EyeGlassDetailFormState表单
        Object.entries(EyeGlassDetailFormState).forEach(([key]) => {
          if (key in calculated_params) {
            EyeGlassDetailFormState[key] = calculated_params[key];
          }
        });
        // 将提交按钮置为可用
        enabledSubmitButton.value = true;
        // 移除计算参数loading提示
        calculatingmessage();
        // 提示计算失败
        message.success("计算镜架参数成功", 5);
      } else {
        // 将计算参数赋值给EyeGlassDetailFormState表单
        Object.entries(EyeGlassDetailFormState).forEach(([key]) => {
          if (key in calculated_params) {
            EyeGlassDetailFormState[key] = calculated_params[key];
          }
        });
        // 将提交按钮置为可用
        enabledSubmitButton.value = true;
        // 移除计算参数loading提示
        calculatingmessage();
        message.success("计算镜架参数成功", 5);
      }
      // 获取拍摄三视图背景图片
      captureResultAllBackground();
    }
    ws.close();
  });
  // 监听错误事件
  ws.addEventListener("error", () => {
    message.error("参数计算失败，请检查设备连接", 10);
    ws.close();
  });

  // 计算镜架风格，todo：未来要用websocket或http请求去计算
  EyeGlassStyleFormState.style = [1];
};

// 功能函数：访问WebSocket，开始拍摄预览
const captureStart = (camId: number) => {
  const ws = new WebSocket(`ws://localhost:8765/camera-usb/${camId}`);
  ws.addEventListener("message", (event) => {
    // 判断返回的event.data是string还是bytes
    if (typeof event.data === "string") {
      // 显示相机状态错误Modal提示
      showCameraStateErrorModal.value = true;
      // 将相机状态置为false
      cameraState.value = false;
      ws.close();
    } else {
      // 将相机状态置为true
      cameraState.value = true;
      // 将拍摄的图像赋值给imgCameraUrl
      imgCameraUrl.value = URL.createObjectURL(event.data as Blob);
    }
  });
  // 监听错误事件
  ws.addEventListener("error", () => {
    message.error("摄像头启动失败，请检查设备连接", 10);
    ws.close();
  });
  // 将WebSocket实例存入wsMap
  wsMap.value.set(camId.toString(), ws);
};

// 功能函数：访问WebSocket，拍摄
const capture = (camId: number) => {
  const ws = new WebSocket(`ws://localhost:8765/capture-usb/${camId}`);
  ws.addEventListener("message", (event) => {
    if (typeof event.data === "string") {
      // 显示相机状态错误Modal提示
      showCameraStateErrorModal.value = true;
      // 将相机状态置为false
      cameraState.value = false;
    } else {
      // 将拍摄的图像赋值给imgCameraUrl
      imgCameraUrl.value = URL.createObjectURL(event.data as Blob);
      // 将拍摄的图像赋值给imgCameraPreviewUrl
      if (camId == 0) {
        // 拍摄成功提示
        message.success("俯视图拍摄成功", 5);
        // 将拍摄的俯视图赋值给URL
        imgCameraPreview0Url.value = URL.createObjectURL(event.data as Blob);
        // 将拍摄的俯视图赋值给EyeGlassImageFormState
        EyeGlassImageFormState.topview = new File(
          [event.data as Blob],
          "0.jpg",
        );
      } else if (camId == 1) {
        // 拍摄成功提示
        message.success("正视图拍摄成功", 5);
        // 将拍摄的正视图赋值给URL
        imgCameraPreview1Url.value = URL.createObjectURL(event.data as Blob);
        // 将拍摄的正视图赋值给EyeGlassImageFormState
        EyeGlassImageFormState.frontview = new File(
          [event.data as Blob],
          "1.jpg",
        );
      } else if (camId == 2) {
        // 拍摄成功提示
        message.success("侧视图拍摄成功", 5);
        // 将拍摄的侧视图赋值给URL
        imgCameraPreview2Url.value = URL.createObjectURL(event.data as Blob);
        // 将拍摄的侧视图赋值给EyeGlassImageFormState
        EyeGlassImageFormState.sideview = new File(
          [event.data as Blob],
          "2.jpg",
        );
      }
      // 将相机状态置为true
      cameraState.value = true;
    }
    // 收到拍摄完成消息后，关闭WebSocket
    ws.close();
    // 拍摄完成后，清除摄像头缓存
    clearCameraCache();
  });
  // 监听错误事件
  ws.addEventListener("error", () => {
    message.error("拍摄失败，请检查设备连接", 10);
    ws.close();
  });
};

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

// 功能函数：访问WebSocket，读取拍摄图像
const captureResult = (camId: number) => {
  // 读取拍摄图像
  if (camId == 0) {
    imgCameraUrl.value = imgCameraPreview0Url.value;
  } else if (camId == 1) {
    imgCameraUrl.value = imgCameraPreview1Url.value;
  } else if (camId == 2) {
    imgCameraUrl.value = imgCameraPreview2Url.value;
  }
};

//功能函数：关闭webSocket
const captureClose = () => {
  //关闭当前页面的WebSocket
  const current = currentStage.value.includes("0")
    ? "0"
    : currentStage.value.includes("1")
      ? "1"
      : "2";
  wsMap.value.get(current)?.close();
  console.log("current:", current);
};

// 功能函数：在拍摄结束、进入计算参数界面后，访问WebSocket，读取三视图图像背景
const captureResultAllBackground = () => {
  const ws0 = new WebSocket(`ws://localhost:8765/load-background/0`);
  ws0.addEventListener("message", (event) => {
    EyeGlassImageBackgroundFormState.topview_bg = new File(
      [event.data as Blob],
      "0_bg.jpg",
    );
    ws0.close();
  });
  const ws1 = new WebSocket(`ws://localhost:8765/load-background/1`);
  ws1.addEventListener("message", (event) => {
    EyeGlassImageBackgroundFormState.frontview_bg = new File(
      [event.data as Blob],
      "1_bg.jpg",
    );
    ws1.close();
  });
  const ws2 = new WebSocket(`ws://localhost:8765/load-background/2`);
  ws2.addEventListener("message", (event) => {
    EyeGlassImageBackgroundFormState.sideview_bg = new File(
      [event.data as Blob],
      "2_bg.jpg",
    );
    ws2.close();
  });
};

// 功能函数：初始化基础参数表单
const initEyeGlassBasicFormState = () => {
  Object.assign(EyeGlassBasicFormState, EyeGlassBasicFormInitState);
};

// 功能函数：初始化风格参数表单
const initEyeGlassStyleFormState = () => {
  Object.assign(EyeGlassStyleFormState, EyeGlassStyleFormInitState);
};

// 功能函数：初始化详细参数表单
const initEyeGlassDetailFormState = () => {
  Object.assign(EyeGlassDetailFormState, EyeGlassDetailFormInitState);
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

// 功能函数：初始化图像URL变量
const initEyeGlassImageUrlState = () => {
  imgCameraUrl.value = "";
  imgCameraPreview0Url.value = "";
  imgCameraPreview1Url.value = "";
  imgCameraPreview2Url.value = "";
};

// 功能函数：初始化所有表单和状态
const initAll = () => {
  initEyeGlassBasicFormState();
  initEyeGlassStyleFormState();
  initEyeGlassDetailFormState();
  initEyeGlassWeightFormState();
  initEyeGlassImageFormState();
  initEyeGlassImageUrlState();
  hasWeightLoged.value = false;
  stepItems.value.map((item) => {
    item.status = "wait";
  });
  wsMap.value.forEach((ws) => {
    ws?.close();
  });
};

// 功能函数：计算参数，校验界面是否处于拍摄预览
const isCaptureStart = computed(() => {
  if (
    currentStage.value == "preview-0" ||
    currentStage.value == "preview-1" ||
    currentStage.value == "preview-2"
  ) {
    return true;
  } else {
    return false;
  }
});

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
  if (store.state.skuormodeltype == 1) {
    if (value == "") {
      message.warning("请输入镜框型号");
      return;
    }
    EyeGlassBasicFormState.model_type = value;
  } else if (store.state.skuormodeltype == 2) {
    if (value == "") {
      message.warning("请输入镜框SKU");
      return;
    }
    EyeGlassBasicFormState.sku = value;
  }
  // 若不为空，则进行FormData构造，并请求检索
  const formData = new FormData();
  formData.append("skuormodeltype", String(store.state.skuormodeltype));
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
  if (store.state.skuormodeltype == 2) {
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
                store.state.searchSku = EyeGlassBasicFormState.sku;
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
    if (stepItems.value[0].status == "finish") {
      currentStage.value = "confirm-0";
      captureResult(0);
    } else {
      currentStage.value = "preview-0";
      captureStart(0);
    }
  });
};

// 拍摄或确认按钮点击事件
const onClickCaptureOrConfirm = () => {
  console.log("enableSubmitButton:", enabledSubmitButton.value);
  switch (currentStage.value) {
    case "preview-0": // 俯视图预览
      // 关闭上一个WebSocket
      wsMap.value.get("0")?.close();
      capture(0);
      // 如果摄像头开启，则进入确认状态
      currentStage.value = "confirm-0";
      break;
    case "confirm-0": // 俯视图确认
      if (stepItems.value[1].status == "finish") {
        captureResult(1);
        currentStage.value = "confirm-1";
      } else {
        captureStart(1);
        currentStage.value = "preview-1";
      }
      stepItems.value[0].status = "finish";
      break;
    case "preview-1": // 正视图预览
      // 关闭上一个WebSocket
      wsMap.value.get("1")?.close();
      capture(1);
      currentStage.value = "confirm-1";
      break;
    case "confirm-1": // 正视图确认
      if (stepItems.value[2].status == "finish") {
        captureResult(2);
        currentStage.value = "confirm-2";
      } else {
        captureStart(2);
        currentStage.value = "preview-2";
      }
      stepItems.value[1].status = "finish";
      break;
    case "preview-2": // 侧视图预览
      // 关闭上一个WebSocket
      wsMap.value.get("2")?.close();
      capture(2);
      currentStage.value = "confirm-2";
      break;
    case "confirm-2": // 侧视图确认
      // captureResultAll();
      stepItems.value[2].status = "finish";
      currentStage.value = "input-params";
      if (!hasWeightLoged.value) {
        readWeight();
      }
      break;
    case "input-params": // 计算参数
      // 保存镜框信息成功后进入SKU输入阶段
      saveNewEyeglassFrame().then((result) => {
        if (result) {
          // 重置提交按钮
          enabledSubmitButton.value = false;
          // 页面跳转至SKU输入阶段
          currentStage.value = "input-sku";
          // 初始化表单Options
          initFormOptions();
          // 初始化镜架检索类型和搜索字符串
          store.state.skuormodeltype = 1;
          searchString.value = "";
        }
      });
      break;
  }
};

// 返回或重拍按钮点击事件
const onClickReturnOrRedo = () => {
  switch (currentStage.value) {
    case "input-basic-params":
      currentStage.value = "input-sku";
      // 初始化表单Options
      initFormOptions();
      // 重置表单
      initEyeGlassBasicFormState();
      break;
    case "preview-0":
      // 关闭上一个WebSocket
      wsMap.value.get("0")?.close();
      currentStage.value = "input-basic-params";
      break;
    case "confirm-0":
      captureStart(0);
      currentStage.value = "preview-0";
      break;
    case "confirm-1":
      captureStart(1);
      currentStage.value = "preview-1";
      break;
    case "confirm-2":
      captureStart(2);
      currentStage.value = "preview-2";
      break;
    case "preview-1":
      // 关闭上一个WebSocket
      wsMap.value.get("1")?.close();
      captureResult(0);
      currentStage.value = "confirm-0";
      break;
    case "preview-2":
      // 关闭上一个WebSocket
      wsMap.value.get("2")?.close();
      captureResult(1);
      currentStage.value = "confirm-1";
      break;
    case "input-params":
      captureResult(2);
      // 关闭read-weight的WebSocket
      wsMap.value.get("weight")?.close(1000, "客户端关闭read-weight");
      currentStage.value = "confirm-2";
      break;
  }
};

// 步骤条点击事件
const onClickStep = (clickStep: number) => {
  if (stepItems.value[clickStep].status == "finish") {
    //关闭原来的WebSocket
    captureClose();
    // 跳转至已完成的步骤
    captureResult(clickStep);
    currentStage.value =
      clickStep == 0 ? "confirm-0" : clickStep == 1 ? "confirm-1" : "confirm-2";
  } else if (stepItems.value[clickStep - 1].status == "finish") {
    //关闭原来的WebSocket
    captureClose();
    // 跳转至即将进行的步骤
    captureStart(clickStep);
    currentStage.value =
      clickStep == 0 ? "preview-0" : clickStep == 1 ? "preview-1" : "preview-2";
  }
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

// 计算参数按钮点击事件
const onClickCalculateParams = () => {
  // 计算参数
  calculateParamsAndStyles();
};

// 详细信息模态窗按钮点击事件
const onClickShowDetailModal = () => {
  isInputEditable.value = "";
  showDetailModal.value = true;
  Object.entries(EyeGlassDetailFormState).forEach(([key, value]) => {
    EyeGlassDetailModelFormState[key] = value;
  });
};

// 详细信息模态窗保存按钮点击事件
const onClickSaveDetailModal = () => {
  EyeGlassDetailModelFormRef.value
    .validate()
    .then(() => {
      Object.entries(EyeGlassDetailModelFormState).forEach(([key, value]) => {
        EyeGlassDetailFormState[key] = value;
      });
      initEyeGlassDetailModelFormState();
      showDetailModal.value = false;
    })
    .catch(() => {
      message.error("请完善镜架详细信息");
    });
};

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
  let cam_id = 0;
  switch (currentStage.value) {
    case "preview-0":
      cam_id = 0;
      break;
    case "preview-1":
      cam_id = 1;
      break;
    case "preview-2":
      cam_id = 2;
      break;
    default:
      return;
  }
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
};
// 降低亮度
const onClickLightdown = () => {
  let cam_id = 0;
  switch (currentStage.value) {
    case "preview-0":
      cam_id = 0;
      break;
    case "preview-1":
      cam_id = 1;
      break;
    case "preview-2":
      cam_id = 2;
      break;
    default:
      return;
  }
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
};
</script>

<style scoped>
.full-height-row {
  height: 100vh;
  background-color: #8675ff;
}

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
  width: 520px;
  border: 3px solid #8675ff;
  border-radius: 20px;
  padding: 49px 60px;
}

.basic-item {
  height: 32px;
  padding: 0 16px;
  margin: 24px;
}

.basic-item >>> label {
  font-size: 18px !important;
}

.basic-item >>> .ant-select-selector,
.ant-input,
.ant-input-number {
  padding-left: 11px;
  width: 100%;
  height: 32px;
  border-radius: 9px;
  font-size: 16px;
}

/* 输入基础信息：消除input-number的重复padding */
.basic-item >>> .ant-input-number-input {
  padding: 0;
}

/* 输入基础信息：风格选择标签 */
/* .basic-item >>> .ant-select-selection-item {
  border-radius: 9px;
} */

/* 输入基础信息：表单验证提示信息 */
.basic-item >>> .ant-form-item-explain-connected {
  position: absolute;
  top: 32px;
}

/* 拍摄 预览图片 */
.registry-preview-image {
  margin-top: 48px;
  height: calc(100% - 48px);
  width: calc(100% - 96px);
  background-color: #ababab;
  border: none;
  border-radius: 12px;
  object-fit: contain;
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

.calculate-item >>> label {
  color: #666666;
}

.calculate-item >>> .ant-select-selector,
.ant-input {
  padding-left: 11px;
  height: 35px;
  border-radius: 9px;
  font-size: 16px;
  color: #999999;
}

/* 计算参数 基础信息 消除input-number的重复padding */
.calculate-item >>> .ant-input-number-input {
  padding: 0;
  color: #999999;
}

/* 计算参数 基础信息 风格选择标签 */
.calculate-item >>> .ant-select-selection-item {
  border-radius: 9px;
}

/* 计算参数 取消表单验证提示信息 */
.calculate-item >>> .ant-form-item-explain-connected {
  display: none;
}

/* 拍摄 步骤条 */
.steps-line {
  width: 603px;
}

.ant-steps-item-finish >>> .ant-steps-item-tail:after {
  background-color: transparent !important;
  width: 100%;
  height: 2px;
  background-image: linear-gradient(to right, #8675ff 50%, transparent 50%);
  background-size: 12px 2px;
  background-repeat: repeat-x;
}

.ant-steps-item-process >>> .ant-steps-item-tail:after {
  background-color: transparent;
  width: 100%;
  height: 2px;
  background-image: linear-gradient(to right, #eeeeee 50%, transparent 50%);
  background-size: 12px 2px;
  background-repeat: repeat-x;
}

.ant-steps-item-wait >>> .ant-steps-item-tail:after {
  background-color: transparent;
  width: 100%;
  height: 2px;
  background-image: linear-gradient(to right, #999999 50%, transparent 50%);
  background-size: 12px 2px;
  background-repeat: repeat-x;
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
