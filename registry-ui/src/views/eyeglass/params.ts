// 数据参数接口：镜架检索选项
export interface searchOption {
  sku: string;
  brand: string;
  model_type: string;
  price: number | null;
  stock: number | null;
  lens_width_st: number | null;
  bridge_width_st: number | null;
  temple_length_st: number | null;
  value: string;
  [key: string]: any;
}
// 数据参数接口: 镜架基础参数
export interface EyeGlassBasicForm {
  sku: string;
  brand: string;
  model_type: string;
  price: number | null;
  material: number | null;
  color: number | null;
  shape: number | null;
  isnosepad: number | null;
  stock: number | null;
  lens_radian: number | null;
  lens_width_st: number | null;
  bridge_width_st: number | null;
  temple_length_st: number | null;
  [key: string]: any;
}
export const EyeGlassBasicFormLabel = {
  sku: "SKU",
  brand: "品牌",
  model_type: "型号",
  price: "价格",
  material: "材质",
  color: "颜色",
  shape: "形状",
  isnosepad: "鼻托",
  stock: "库存",
  lens_radian: "撑片弧度",
  lens_width_st: "镜片宽度",
  bridge_width_st: "鼻梁宽度",
  temple_length_st: "镜腿长度",
};
export const EyeGlassBasicFormUnit = {
  sku: "",
  brand: "",
  model_type: "",
  price: "",
  material: "",
  color: "",
  shape: "",
  isnosepad: "",
  stock: "",
  lens_radian: "°",
  lens_width_st: "mm",
  bridge_width_st: "mm",
  temple_length_st: "mm",
};

// 数据参数接口: 镜架风格参数
export interface EyeGlassStyleForm {
  style: number[];
  [key: string]: any;
}
export const EyeGlassStyleFormLabel = {
  style: "风格",
};

// 数据参数接口: 镜架详细参数
export interface EyeGlassDetailForm {
  frame_height: string;
  frame_width: string;
  pile_height_left: string;
  pile_height_right: string;
  frame_top_width: string;
  top_points: string;
  frame_rects: string;
  lens_width_left: string;
  lens_width_right: string;
  lens_height_left: string;
  lens_height_right: string;
  lens_diagonal_left: string;
  lens_diagonal_right: string;
  lens_area_left: string;
  lens_area_right: string;
  bridge_width: string;
  lens_center_points: string;
  lens_top_points: string;
  vertical_angle: string;
  forward_angle: string;
  temple_angle: string;
  drop_length: string;
  face_angle: string;
  sagittal_angle_left: string;
  sagittal_angle_right: string;
  temple_length_left: string;
  temple_length_right: string;
  temporal_width: string;
  spread_angle_left: string;
  spread_angle_right: string;
  pile_distance: string;
  [key: string]: any;
}
// 镜架详细参数Label
export const EyeGlassDetailFormLabel = {
  frame_height: "镜框高度",
  frame_width: "镜框宽度",
  pile_height_left: "左桩头高度",
  pile_height_right: "右桩头高度",
  frame_top_width: "镜框顶部宽度",
  top_points: "镜框顶点坐标",
  frame_rects: "镜框矩形坐标",
  lens_width_left: "左镜圈宽度",
  lens_width_right: "右镜圈宽度",
  lens_height_left: "左镜圈高度",
  lens_height_right: "右镜圈高度",
  lens_diagonal_left: "左镜圈对角线长度",
  lens_diagonal_right: "右镜圈对角线长度",
  lens_area_left: "左镜圈面积",
  lens_area_right: "右镜圈面积",
  bridge_width: "鼻梁宽度",
  lens_center_points: "镜圈中心点坐标",
  lens_top_points: "镜圈顶点坐标",
  vertical_angle: "垂俯角",
  forward_angle: "前倾角",
  temple_angle: "镜腿角度",
  drop_length: "垂长",
  face_angle: "面弯",
  sagittal_angle_left: "左垂内角",
  sagittal_angle_right: "右垂内角",
  temple_length_left: "左镜腿长度",
  temple_length_right: "右镜腿长度",
  temporal_width: "颞距",
  spread_angle_left: "左镜腿外张角",
  spread_angle_right: "右镜腿外张角",
  pile_distance: "桩头距离",
};
// 镜架详细参数Unit
export const EyeGlassDetailFormUnit = {
  frame_height: "mm",
  frame_width: "mm",
  pile_height_left: "mm",
  pile_height_right: "mm",
  frame_top_width: "mm",
  top_points: "",
  frame_rects: "",
  lens_width_left: "mm",
  lens_width_right: "mm",
  lens_height_left: "mm",
  lens_height_right: "mm",
  lens_diagonal_left: "mm",
  lens_diagonal_right: "mm",
  lens_area_left: "mm²",
  lens_area_right: "mm²",
  bridge_width: "mm",
  lens_center_points: "",
  lens_top_points: "",
  vertical_angle: "°",
  forward_angle: "°",
  temple_angle: "°",
  drop_length: "mm",
  face_angle: "°",
  sagittal_angle_left: "°",
  sagittal_angle_right: "°",
  temple_length_left: "mm",
  temple_length_right: "mm",
  temporal_width: "mm",
  spread_angle_left: "°",
  spread_angle_right: "°",
  pile_distance: "mm",
};
// 参数接口: 镜架详细参数（展示）
export const EyeGlassDetailToviewFormLabel = {
  frame_height: "镜框高度",
  frame_width: "镜框宽度",
  pile_height_left: "左桩头高度",
  pile_height_right: "右桩头高度",
  frame_top_width: "镜框顶部宽度",
  lens_width_left: "左镜圈宽度",
  lens_width_right: "右镜圈宽度",
  lens_height_left: "左镜圈高度",
  lens_height_right: "右镜圈高度",
  lens_diagonal_left: "左镜圈对角线长度",
  lens_diagonal_right: "右镜圈对角线长度",
  lens_area_left: "左镜圈面积",
  lens_area_right: "右镜圈面积",
  bridge_width: "鼻梁宽度",
  vertical_angle: "垂俯角",
  forward_angle: "前倾角",
  temple_angle: "镜腿角度",
  drop_length: "垂长",
  face_angle: "面弯",
  sagittal_angle_left: "左垂内角",
  sagittal_angle_right: "右垂内角",
  temple_length_left: "左镜腿长度",
  temple_length_right: "右镜腿长度",
  temporal_width: "颞距",
  spread_angle_left: "左镜腿外张角",
  spread_angle_right: "右镜腿外张角",
  pile_distance: "桩头距离",
};

// 数据参数接口: 镜架重量参数
export interface EyeGlassWeightForm {
  weight: string;
  [key: string]: any;
}
export const EyeGlassWeightFormLabel = {
  weight: "重量",
};
export const EyeGlassWeightFormUnit = {
  weight: "g",
};

// 数据参数接口: 镜架图片参数
export interface EyeGlassImageForm {
  frontview: File | null;
  sideview: File | null;
  topview: File | null;
  [key: string]: any;
}
export const EyeGlassImageFormLabel = {
  frontview: "正视图",
  sideview: "侧视图",
  topview: "俯视图",
};
// 数据参数接口: 镜架图片path参数
export interface EyeGlassImagePathForm {
  frontview: string;
  sideview: string;
  topview: string;
  [key: string]: any;
}
// 数据参数接口：镜架图片背景参数
export interface EyeGlassImageBackgroundForm {
  frontview_bg: File | null;
  sideview_bg: File | null;
  topview_bg: File | null;
}

// 数据参数接口: 镜架图片处理参数定义（工控机端计算参数用）
export interface EyeGlassCalculateParams {
  num_iter_0: string;
  num_iter_1: string;
  num_iter_2: string;
  num_method: string;
}
export const EyeGlassCalculateParamsLabel = {
  num_iter_0: "形态学处理次数(轮廓)",
  num_iter_1: "形态学处理次数(挡板)",
  num_iter_2: "形态学处理次数(镜腿)",
  num_method: "处理方法",
};
export const EyeGlassCalculateParamsExample: EyeGlassCalculateParams = {
  num_iter_0: "8",
  num_iter_1: "4",
  num_iter_2: "200",
  num_method: "1",
};
