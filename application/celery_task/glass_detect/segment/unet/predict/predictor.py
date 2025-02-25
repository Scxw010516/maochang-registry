import itertools
from typing import List, Tuple, Union

import numpy as np
import torch
from torch import nn
from tqdm import tqdm

from .inference import (
    compute_gaussian,
    compute_steps_for_sliding_window,
    convert_predicted_logits_to_segmentation_with_correct_shape,
)
from ..utils.padding import pad_nd_image
from ..utils.utils import empty_cache


class Predictor(object):
    def __init__(
        self,
        network: nn.Module = None,
        patch_size: Tuple[int, ...] = (896, 1792),
        tile_step_size: float = 0.5,
        use_gaussian: bool = True,
        use_mirroring: bool = True,
        perform_everything_on_device: bool = True,
        device: torch.device = torch.device("cuda"),
        allow_tqdm: bool = True,
        allowed_mirroring_axes: Tuple[int, ...] = (0, 1),
        num_segmentation_heads: int = 2,
    ):
        self.network = network
        self.patch_size = patch_size
        self.tile_step_size = tile_step_size
        self.use_gaussian = use_gaussian
        self.use_mirroring = use_mirroring
        self.allow_tqdm = allow_tqdm
        self.allowed_mirroring_axes = torch.tensor(allowed_mirroring_axes)
        self.num_segmentation_heads = num_segmentation_heads
        # print("Using device:", device)
        if device.type == "cuda":
            torch.backends.cudnn.benchmark = True
        else:
            print(
                "perform_everything_on_device=True is only supported for cuda devices! Setting this to False"
            )
            perform_everything_on_device = False
        self.device = device
        self.perform_everything_on_device = perform_everything_on_device

    def predict_single_npy_array(
        self,
        data: torch.Tensor,
        properties: dict,
        save_or_return_probabilities: bool = False,
        return_probabilities: bool = False,
        transpose_forward: Tuple[int] = (0, 1, 2),
        transpose_backward: Tuple[int] = (0, 1, 2),
        spacing: Tuple[float, float, float] = (1, 1, 1),
        has_regions: bool = False,
        regions_class_order: Union[List[int], None] = None,
        num_segmentation_heads: int = 8,
        inference_nonlin=None,
        foreground_labels: List[int] = [2],
    ):
        predicted_logits = self.predict_sliding_window_return_logits(data).to(
            "cpu"
        )  # torch.Size([2, 1, 1600, 3200])

        ret = convert_predicted_logits_to_segmentation_with_correct_shape(
            predicted_logits,
            properties,
            return_probabilities=save_or_return_probabilities,
            transpose_forward=transpose_forward,
            transpose_backward=transpose_backward,
            spacing=spacing,
            has_regions=has_regions,
            regions_class_order=regions_class_order,
            num_segmentation_heads=num_segmentation_heads,
            inference_nonlin=inference_nonlin,
            foreground_labels=foreground_labels,
        )
        if save_or_return_probabilities:
            return ret[0], ret[1]
        else:
            return ret

    def predict_sliding_window_return_logits(
        self, input_image: torch.Tensor
    ) -> Union[np.ndarray, torch.Tensor]:
        assert isinstance(input_image, torch.Tensor)
        self.network = self.network.to(self.device)
        self.network.eval()

        # Autocast can be annoying
        # If the device_type is 'cpu' then it's slow as heck on some CPUs (no auto bfloat16 support detection)
        # and needs to be disabled.
        # If the device_type is 'mps' then it will complain that mps is not implemented, even if enabled=False
        # is set. Whyyyyyyy. (this is why we don't make use of enabled=False)
        # So autocast will only be active if we have a cuda device.
        with torch.no_grad():
            assert (
                input_image.ndim == 4
            ), "input_image must be a 4D np.ndarray or torch.Tensor (c, x, y, z)"

            # if input_image is smaller than tile_size we need to pad it to tile_size.
            # 输入图像较小时需要pad到tile_size(patch_size),slicer_revert_padding记录了pad的参数,用于之后去除padding
            data, slicer_revert_padding = pad_nd_image(
                input_image,
                self.patch_size,
                "constant",
                {"value": 0},
                True,
                None,
            )  # slicer_revert_padding = (slice(0, 3, None), slice(0, 1, None), slice(0, 1600, None), slice(0, 3200, None)) data.shape = torch.Size([3, 1, 1600, 3200])

            slicers = self._internal_get_sliding_window_slicers(
                data.shape[1:]
            )  # [(slice(None, None, None), 0, slice(0, 896, None), slice(0, 1792, None)),...] len(slicers) == 9 [None,dim,height_ax,width_ax]

            if self.perform_everything_on_device and self.device != "cpu":
                # we need to try except here because we can run OOM in which case we need to fall back to CPU as a results device
                # try:
                predicted_logits = self._internal_predict_sliding_window_return_logits(
                    data, slicers, self.perform_everything_on_device
                )
                # except RuntimeError:
                #     print(
                #         "Prediction on device was unsuccessful, probably due to a lack of memory. Moving results arrays to CPU"
                #     )
                #     predicted_logits = (
                #         self._internal_predict_sliding_window_return_logits(
                #             data, slicers, False
                #         )
                #     )
            else:
                predicted_logits = self._internal_predict_sliding_window_return_logits(
                    data, slicers, self.perform_everything_on_device
                )
            # revert padding 去除padding
            predicted_logits = predicted_logits[
                (slice(None), *slicer_revert_padding[1:])
            ]
        return predicted_logits

    def _internal_get_sliding_window_slicers(self, image_size: Tuple[int, ...]):
        slicers = []
        if len(self.patch_size) < len(image_size):
            # 2d
            assert len(self.patch_size) == len(image_size) - 1, (
                "if tile_size has less entries than image_size, "
                "len(tile_size) "
                "must be one shorter than len(image_size) "
                "(only dimension "
                "discrepancy of 1 allowed)."
            )
            steps = compute_steps_for_sliding_window(
                image_size[1:],
                self.patch_size,
                self.tile_step_size,
            )  # [[0, 352, 704], [0, 704, 1408]]
            # print(steps)
            # print(image_size)
            for d in range(image_size[0]):
                for sx in steps[0]:
                    for sy in steps[1]:
                        slicers.append(
                            tuple(
                                [
                                    slice(None),
                                    d,
                                    *[
                                        slice(si, si + ti)
                                        for si, ti in zip(
                                            (sx, sy),
                                            self.patch_size,
                                        )
                                    ],
                                ]
                            )
                        )
        else:
            steps = compute_steps_for_sliding_window(
                image_size, self.patch_size, self.tile_step_size
            )

            for sx in steps[0]:
                for sy in steps[1]:
                    for sz in steps[2]:
                        slicers.append(
                            tuple(
                                [
                                    slice(None),
                                    *[
                                        slice(si, si + ti)
                                        for si, ti in zip(
                                            (sx, sy, sz),
                                            self.patch_size,
                                        )
                                    ],
                                ]
                            )
                        )
        return slicers

    def _internal_predict_sliding_window_return_logits(
        self,
        data: torch.Tensor,
        slicers,
        do_on_device: bool = True,
    ):
        predicted_logits = n_predictions = prediction = gaussian = workon = None
        results_device = self.device if do_on_device else torch.device("cpu")

        try:
            empty_cache(self.device)

            predicted_logits = torch.zeros(
                (self.num_segmentation_heads, *data.shape[1:]),
                dtype=torch.half,
                device=results_device,
            )
            n_predictions = torch.zeros(
                data.shape[1:], dtype=torch.half, device=results_device
            )  # 每个位置的预测次数

            if self.use_gaussian:
                gaussian = compute_gaussian(
                    tuple(self.patch_size),
                    sigma_scale=1.0 / 8,
                    value_scaling_factor=10,
                    device=results_device,
                )
            else:
                gaussian = 1

            loop = tqdm(slicers, disable=not self.allow_tqdm, position=0, leave=True)
            for sl in loop:
                workon = data[sl][None]
                workon = workon.to(self.device)

                prediction = self._internal_maybe_mirror_and_predict(workon)[0].to(
                    results_device
                )

                if self.use_gaussian:
                    prediction *= gaussian
                # MODIFY: 将prediction改为prediction[0],以匹配shape
                predicted_logits[sl] += prediction  # 将所有prediction patches 加在一起
                n_predictions[sl[1:]] += gaussian
            predicted_logits /= n_predictions
            # check for infs
            if torch.any(torch.isinf(predicted_logits)):
                raise RuntimeError(
                    "Encountered inf in predicted array. Aborting... If this problem persists, "
                    "reduce value_scaling_factor in compute_gaussian or increase the dtype of "
                    "predicted_logits to fp32"
                )
            return predicted_logits
        except Exception as e:
            del predicted_logits, n_predictions, prediction, gaussian, workon
            empty_cache(self.device)
            empty_cache(results_device)
            raise e

    def _internal_maybe_mirror_and_predict(self, x: torch.Tensor) -> torch.Tensor:
        mirror_axes = self.allowed_mirroring_axes if self.use_mirroring else None
        prediction = self.network(x)  # 模型推理 s.shape == (1,3,896,1792)
        prediction = prediction[0]
        if mirror_axes is not None:
            # 眼镜中未使用镜像
            # check for invalid numbers in mirror_axes
            # x should be 5d for 3d images and 4d for 2d. so the max value of mirror_axes cannot exceed len(x.shape) - 3
            assert (
                max(mirror_axes) <= x.ndim - 3
            ), "mirror_axes does not match the dimension of the input!"
            # MODIFY: 将prediction改为prediction[0]，以匹配shape
            prediction = prediction
            mirror_axes = [m + 2 for m in mirror_axes]
            axes_combinations = [
                c
                for i in range(len(mirror_axes))
                for c in itertools.combinations(mirror_axes, i + 1)
            ]
            for axes in axes_combinations:
                prediction += torch.flip(self.network(torch.flip(x, axes))[0], axes)
            prediction /= len(axes_combinations) + 1
        return prediction
