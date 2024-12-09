// 摄像头参数和对象字典
export interface Camera {
  index: number; // 设备索引
  kind: string; // 设备类型，videoinput
  label: string; // 设备名称
  deviceId: string; // 设备ID
  mediaStream: MediaStream | null; // 设备流对象
}
