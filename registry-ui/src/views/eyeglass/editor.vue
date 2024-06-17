<template>
  <div>
    <h4 class="title">遮罩修正工具</h4>
    <input ref="fileInput" type="file" placeholder="" style="display: none" />
    <a-button type="outlined" @click="onClickReturn">返回</a-button>
    <a-button type="primary" @click="onClickSelectFile">选择图片</a-button>
    <a-button
      type="outlined"
      @click="
        () => {
          if (canvas && cursor && mousecursor) {
            canvas.isDrawingMode = !canvas.isDrawingMode;
            if (!canvas.isDrawingMode) {
              cursor.remove(mousecursor);
            } else {
              canvas.discardActiveObject().renderAll();
              cursor.add(mousecursor);
            }
          }
        }
      "
      >{{
        canvas?.isDrawingMode
          ? "当前模式：绘画模式（点击切换）"
          : "当前模式：预览模式（点击切换）"
      }}</a-button
    >
    <a-input
      v-model:value="brushWidth"
      addon-before="画笔大小"
      @change="changeBrushWidth"
    />
    <a-input
      id="color"
      type="color"
      addon-before="画笔颜色"
      v-model:value="brushColor"
      @change="changeBrushColor"
    /><br />
    <a-button type="outlined" :disabled="!isUndoEnabled" @click="onClickUndo"
      >撤销</a-button
    >
    <a-button type="primary" @click="onClickSave">保存</a-button>
    <div id="container" ref="container">
      <canvas id="canvas" width="500" height="500"></canvas>
      <canvas id="cursor" width="500" height="500"></canvas>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref, type Ref } from "vue";
import { useRouter } from "vue-router";
import { fabric } from "fabric";

const router = useRouter();
const fileInput = ref<HTMLInputElement>();
const canvas = ref<fabric.Canvas>();
const cursor = ref<fabric.StaticCanvas>();
const mousecursor = ref<fabric.Circle>();
const brushWidth = ref<string>("4");
const cursorOpacity = ref<number>(0.5);
const brushColor = ref<string>("#7f7f7f");
const isUndoEnabled = ref<boolean>(false);
const container = ref<HTMLDivElement>();

const onFileChange = async (e: Event) => {
  const target = e.target as HTMLInputElement;
  const files = target.files;
  if (
    canvas.value &&
    cursor.value &&
    container.value &&
    files &&
    files.length > 0
  ) {
    const url = URL.createObjectURL(files[0]);
    const image = new Image();
    image.src = url;
    await image.decode();
    // console.log(
    //   `w: ${image.width}, h: ${image.height}, sx: ${(canvas.value?.width ?? 0) / image.width}, sy:${(canvas.value?.height ?? 0) / image.height}`,
    // );
    container.value.style.width = image.width + "px";
    container.value.style.height = image.height + "px";
    canvas.value.setWidth(image.width);
    canvas.value.setHeight(image.height);
    cursor.value.setWidth(image.width);
    cursor.value.setHeight(image.height);
    canvas.value.setBackgroundImage(
      url,
      () => {
        canvas.value?.renderAll();
      },
      {
        scaleX: 1,
        scaleY: 1,
      },
    );
  }
};

const onClickSelectFile = () => {
  fileInput.value?.click();
};

interface MousecursorState {
  left: number;
  top: number;
}

const originalState: Ref<MousecursorState | null> = ref(null);

const onClickReturn = () => {
  router.push("/registry");
};

const changeBrushWidth = () => {
  const width = parseInt(brushWidth.value, 10);
  if (canvas.value && cursor.value && mousecursor.value) {
    canvas.value.freeDrawingBrush.width = width;
    mousecursor.value
      .set({
        left: originalState.value?.left,
        top: originalState.value?.top,
        radius: width / 2,
      })
      .setCoords();
    cursor.value.renderAll();
  }
};

const changeBrushColor = (e: Event) => {
  const target = e.target as HTMLInputElement;
  if (canvas.value && cursor.value && mousecursor.value) {
    canvas.value.freeDrawingBrush.color = target.value;
    var bigint = parseInt(target.value.replace("#", ""), 16);
    var r = (bigint >> 16) & 255;
    var g = (bigint >> 8) & 255;
    var b = bigint & 255;
    mousecursor.value.set({
      fill: "rgba(" + [r, g, b, cursorOpacity.value].join(",") + ")",
    });
  }
};

const onClickUndo = () => {
  if (isUndoEnabled.value && canvas.value) {
    canvas.value.remove(
      canvas.value.getObjects()[canvas.value.getObjects().length - 1],
    );
    isUndoEnabled.value =
      (canvas.value || false) && canvas.value.getObjects().length > 0;
  }
};

const onClickSave = () => {
  canvas.value?.clone((canavsToSave: fabric.Canvas) => {
    canavsToSave.setBackgroundColor("#000000", () => {});
    canavsToSave.setBackgroundImage(new fabric.Image(""), () => {});
    canavsToSave.getObjects().forEach((item) => {
      const path = item as fabric.Path;
      path.set({
        stroke: "#ffffff",
      });
    });
    const x = new XMLHttpRequest();
    x.open("GET", canavsToSave.toDataURL({ format: "image/png" }), true);
    x.responseType = "blob";
    x.onload = () => {
      const url = window.URL.createObjectURL(x.response);
      const a = document.createElement("a");
      a.href = url;
      a.download = "result.png";
      a.click();
    };
    x.send();
  });
};

onMounted(() => {
  fileInput.value?.addEventListener("change", onFileChange);

  canvas.value = new fabric.Canvas("canvas", {
    isDrawingMode: true,
    freeDrawingCursor: "none",
  });
  canvas.value.isDrawingMode = true;
  canvas.value.freeDrawingBrush.color = brushColor.value;

  mousecursor.value = new fabric.Circle({
    left: -100,
    top: -100,
    fill: "rgba(127,127,127," + cursorOpacity.value + ")",
    stroke: "black",
    originX: "center",
    originY: "center",
  });

  cursor.value = new fabric.StaticCanvas("cursor");
  cursor.value.add(mousecursor.value);
  canvas.value.on("mouse:move", (evt) => {
    if (canvas.value && cursor.value && mousecursor.value) {
      const mouse = canvas.value.getPointer(evt.e);
      mousecursor.value
        .set({
          top: mouse.y,
          left: mouse.x,
        })
        .setCoords();
      cursor.value.renderAll();
    }
  });
  canvas.value.on("mouse:out", () => {
    if (canvas.value && cursor.value && mousecursor.value) {
      mousecursor.value
        .set({
          top: originalState.value?.top,
          left: originalState.value?.left,
        })
        .setCoords();
      cursor.value.renderAll();
    }
  });
  canvas.value.on("mouse:up", () => {
    isUndoEnabled.value =
      (canvas.value || false) && canvas.value.getObjects().length > 0;
  });
  changeBrushWidth();
});
</script>

<style scoped>
.title {
  text-align: center;
}

#img {
  width: 100px;
  height: 100px;
}

#container {
  position: relative;
  width: 500px;
  height: 500px;
}

canvas {
  border: 1px solid;
}

#container canvas,
.canvas-container {
  position: absolute !important;
  left: 0 !important;
  top: 0 !important;
  width: 100% !important;
  height: 100% !important;
}

#cursor {
  pointer-events: none !important;
}
</style>
