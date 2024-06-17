# Onnx export code is from [labelme annotation tool](https://github.com/labelmeai/efficient-sam). Huge thanks to Kentaro Wada.

import cv2
import numpy as np
import onnxruntime



def segment_onnx(
    image, input_points, input_labels, onnx_path="efficient_sam_vits.onnx"
):
    try:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    except:
        pass

    image = image.transpose(2, 0, 1)[None].astype(np.float32) / 255.0
    input_points = np.reshape(np.array(input_points), [1, 1, -1, 2]).astype(np.float32)
    input_labels = np.reshape(np.array(input_labels), [1, 1, -1]).astype(np.float32)

    inference_session = onnxruntime.InferenceSession(onnx_path)

    (
        predicted_logits,
        predicted_iou,
        predicted_lowres_logits,
    ) = inference_session.run(
        output_names=None,
        input_feed={
            "batched_images": image,
            "batched_point_coords": input_points,
            "batched_point_labels": input_labels,
        },
    )

    predicted_logits = predicted_logits[0, 0, :, :, :]
    predicted_iou = predicted_iou[0, 0, :]
    sorted_ids = np.argsort(predicted_iou)[::-1]
    predicted_logits = np.take_along_axis(
        predicted_logits, sorted_ids[..., None, None], axis=0
    )
    masks = list(np.logical_not([predicted_logits[i, :, :] >= 0 for i in range(3)]))
    return masks
