from typing import Union, Tuple, List

import numpy as np
import torch
from scipy.ndimage import gaussian_filter

from .resample import resample_data_or_seg_to_shape
from ..utils.utils import bounding_box_to_slice, softmax_helper_dim0


def revert_cropping_on_probabilities(
    predicted_probabilities: Union[torch.Tensor, np.ndarray],
    bbox: List[List[int]],
    original_shape: Union[List[int], Tuple[int, ...]],
    has_regions: bool = False,
):
    """
    ONLY USE THIS WITH PROBABILITIES, DO NOT USE LOGITS AND DO NOT USE FOR SEGMENTATION MAPS!!!

    predicted_probabilities must be (c, x, y(, z))

    Why do we do this here? Well if we pad probabilities we need to make sure that convert_logits_to_segmentation
    correctly returns background in the padded areas. Also, we want to ba able to look at the padded probabilities
    and not have strange artifacts.
    Only LabelManager knows how this needs to be done. So let's let him/her do it, ok?
    """
    # revert cropping
    probs_reverted_cropping = (
        np.zeros(
            (predicted_probabilities.shape[0], *original_shape),
            dtype=predicted_probabilities.dtype,
        )
        if isinstance(predicted_probabilities, np.ndarray)
        else torch.zeros(
            (predicted_probabilities.shape[0], *original_shape),
            dtype=predicted_probabilities.dtype,
        )
    )

    if not has_regions:
        probs_reverted_cropping[0] = 1

    slicer = bounding_box_to_slice(bbox)
    probs_reverted_cropping[tuple([slice(None)] + list(slicer))] = (
        predicted_probabilities
    )
    return probs_reverted_cropping


def apply_inference_nonlin(
    logits: Union[np.ndarray, torch.Tensor],
    has_regions: bool = False,
    inference_nonlin=None,
) -> Union[np.ndarray, torch.Tensor]:
    """
    logits has to have shape (c, x, y(, z)) where c is the number of classes/regions
    """
    if inference_nonlin is None:
        inference_nonlin = torch.sigmoid if has_regions else softmax_helper_dim0
    else:
        inference_nonlin = inference_nonlin

    if isinstance(logits, np.ndarray):
        logits = torch.from_numpy(logits)

    with torch.no_grad():
        # softmax etc. is not implemented for half
        logits = logits.float()
        probabilities = inference_nonlin(logits)

    return probabilities


def convert_probabilities_to_segmentation(
    predicted_probabilities: Union[np.ndarray, torch.Tensor],
    has_regions: bool = False,
    regions_class_order: Union[List[int], None] = None,
    num_segmentation_heads: int = 8,
) -> Union[np.ndarray, torch.Tensor]:
    """
    assumes that inference_nonlinearity was already applied!

    predicted_probabilities has to have shape (c, x, y(, z)) where c is the number of classes/regions
    """
    if not isinstance(predicted_probabilities, (np.ndarray, torch.Tensor)):
        raise RuntimeError(
            f"Unexpected input type. Expected np.ndarray or torch.Tensor,"
            f" got {type(predicted_probabilities)}"
        )

    if has_regions:
        assert regions_class_order is not None, (
            "if region-based training is requested then you need to "
            "define regions_class_order!"
        )
        # check correct number of outputs
    assert predicted_probabilities.shape[0] == num_segmentation_heads, (
        f"unexpected number of channels in predicted_probabilities. Expected {num_segmentation_heads}, "
        f"got {predicted_probabilities.shape[0]}. Remember that predicted_probabilities should have shape "
        f"(c, x, y(, z))."
    )

    if has_regions:
        if isinstance(predicted_probabilities, np.ndarray):
            segmentation = np.zeros(predicted_probabilities.shape[1:], dtype=np.uint16)
        else:
            # no uint16 in torch
            segmentation = torch.zeros(
                predicted_probabilities.shape[1:],
                dtype=torch.int16,
                device=predicted_probabilities.device,
            )
        for i, c in enumerate(regions_class_order):
            segmentation[predicted_probabilities[i] > 0.5] = c
    else:
        segmentation = predicted_probabilities.argmax(0)

    return segmentation


def compute_gaussian(
    tile_size: Union[Tuple[int, ...], List[int]],
    sigma_scale: float = 1.0 / 8,
    value_scaling_factor: float = 1,
    dtype=torch.float16,
    device=torch.device("cuda", 0),
) -> torch.Tensor:
    tmp = np.zeros(tile_size)
    center_coords = [i // 2 for i in tile_size]
    sigmas = [i * sigma_scale for i in tile_size]
    tmp[tuple(center_coords)] = 1
    gaussian_importance_map = gaussian_filter(tmp, sigmas, 0, mode="constant", cval=0)

    gaussian_importance_map = torch.from_numpy(gaussian_importance_map)

    gaussian_importance_map /= torch.max(gaussian_importance_map) / value_scaling_factor
    gaussian_importance_map = gaussian_importance_map.to(device=device, dtype=dtype)
    # gaussian_importance_map cannot be 0, otherwise we may end up with nans!
    mask = gaussian_importance_map == 0
    gaussian_importance_map[mask] = torch.min(gaussian_importance_map[~mask])
    return gaussian_importance_map


def compute_steps_for_sliding_window(
    image_size: Tuple[int, ...], tile_size: Tuple[int, ...], tile_step_size: float
) -> List[List[int]]:
    assert [
        i >= j for i, j in zip(image_size, tile_size)
    ], "image size must be as large or larger than patch_size"
    assert (
        0 < tile_step_size <= 1
    ), "step_size must be larger than 0 and smaller or equal to 1"

    # our step width is patch_size*step_size at most, but can be narrower. For example if we have image size of
    # 110, patch size of 64 and step_size of 0.5, then we want to make 3 steps starting at coordinate 0, 23, 46
    target_step_sizes_in_voxels = [i * tile_step_size for i in tile_size]

    num_steps = [
        int(np.ceil((i - k) / j)) + 1
        for i, j, k in zip(image_size, target_step_sizes_in_voxels, tile_size)
    ]

    steps = []
    for dim in range(len(tile_size)):
        # the highest step value for this dimension is
        max_step_value = image_size[dim] - tile_size[dim]
        if num_steps[dim] > 1:
            actual_step_size = max_step_value / (num_steps[dim] - 1)
        else:
            actual_step_size = (
                99999999999  # does not matter because there is only one step at 0
            )

        steps_here = [
            int(np.round(actual_step_size * i)) for i in range(num_steps[dim])
        ]

        steps.append(steps_here)

    return steps


def convert_predicted_logits_to_segmentation_with_correct_shape(
    predicted_logits: Union[torch.Tensor, np.ndarray],
    properties_dict: dict,
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
    # resample to original shape
    spacing_transposed = [properties_dict["spacing"][i] for i in transpose_forward]
    current_spacing = (
        spacing
        if len(spacing)
        == len(properties_dict["shape_after_cropping_and_before_resampling"])
        else [spacing_transposed[0], *spacing]
    )
    predicted_logits = resample_data_or_seg_to_shape(
        predicted_logits,
        properties_dict["shape_after_cropping_and_before_resampling"],
        current_spacing,
        [properties_dict["spacing"][i] for i in transpose_forward],
    )
    # return value of resampling_fn_probabilities can be ndarray or Tensor but that does not matter because
    # apply_inference_nonlin will convert to torch
    predicted_probabilities = apply_inference_nonlin(
        predicted_logits, has_regions=has_regions, inference_nonlin=inference_nonlin
    )
    del predicted_logits
    segmentation = convert_probabilities_to_segmentation(
        predicted_probabilities,
        has_regions=has_regions,
        num_segmentation_heads=num_segmentation_heads,
        regions_class_order=regions_class_order,
    )

    # segmentation may be torch.Tensor but we continue with numpy
    if isinstance(segmentation, torch.Tensor):
        segmentation = segmentation.cpu().numpy()

    # put segmentation in bbox (revert cropping)
    segmentation_reverted_cropping = np.zeros(
        properties_dict["shape_before_cropping"],
        dtype=np.uint8 if len(foreground_labels) < 255 else np.uint16,
    )
    slicer = bounding_box_to_slice(properties_dict["bbox_used_for_cropping"])
    segmentation_reverted_cropping[slicer] = segmentation
    del segmentation

    # revert transpose
    segmentation_reverted_cropping = segmentation_reverted_cropping.transpose(
        transpose_backward
    )
    if return_probabilities:
        # revert cropping
        predicted_probabilities = revert_cropping_on_probabilities(
            predicted_probabilities,
            properties_dict["bbox_used_for_cropping"],
            properties_dict["shape_before_cropping"],
            has_regions=has_regions,
        )
        predicted_probabilities = predicted_probabilities.cpu().numpy()
        # revert transpose
        predicted_probabilities = predicted_probabilities.transpose(
            [0] + [i + 1 for i in transpose_backward]
        )
        return segmentation_reverted_cropping, predicted_probabilities
    else:
        return segmentation_reverted_cropping
