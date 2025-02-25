import os
from typing import Optional, Any

import torchvision
from torch import nn
from torchvision.models import (
    ResNet50_Weights,
    ResNet101_Weights,
    resnet101,
    resnet50,
)
from torchvision.models._utils import _ovewrite_value_param
from torchvision.models.detection import KeypointRCNN, KeypointRCNN_ResNet50_FPN_Weights
from torchvision.models.detection._utils import overwrite_eps
from torchvision.models.detection.backbone_utils import (
    _validate_trainable_layers,
    _resnet_fpn_extractor,
)
from torchvision.models.detection.rpn import AnchorGenerator
from torchvision.ops import misc as misc_nn_ops

os.environ["CUDA_LAUNCH_BLOCKING"] = "1"


def get_model(
    num_keypoints, model="resnet50", anchor_sizes=None, anchor_ratios=None, **kwargs
):
    if anchor_sizes is None:
        anchor_sizes = (32, 64, 128, 256, 512)
    if anchor_ratios is None:
        anchor_ratios = (0.8, 0.9, 1.0, 1.1, 1.2)
    anchor_generator = AnchorGenerator(
        sizes=(32, 64, 128, 256, 512), aspect_ratios=(0.8, 0.9, 1.0, 1.1, 1.2)
    )
    if model == "resnet50":
        model = torchvision.models.detection.keypointrcnn_resnet50_fpn(
            weights=None,
            weights_backbone=ResNet50_Weights.DEFAULT,
            num_keypoints=num_keypoints,
            num_classes=2,
            # Background is the first class, object is the second class
            rpn_anchor_generator=anchor_generator,
            **kwargs,
        )
    elif model == "resnet101":
        model = keypointrcnn_resnet101_fpn(
            weights=None,
            weights_backbone=ResNet101_Weights.DEFAULT,
            num_keypoints=num_keypoints,
            num_classes=2,
            # Background is the first class, object is the second class
            rpn_anchor_generator=anchor_generator,
            **kwargs,
        )
    else:
        raise ValueError(
            f"Unknown model {model}, model must be `resnet50` or `resnet101`."
        )

    return model


def keypointrcnn_resnet101_fpn(
    *,
    progress: bool = True,
    num_classes: Optional[int] = None,
    num_keypoints: Optional[int] = None,
    weights_backbone: Optional[ResNet101_Weights] = ResNet101_Weights.IMAGENET1K_V1,
    trainable_backbone_layers: Optional[int] = None,
    **kwargs: Any,
) -> KeypointRCNN:
    weights_backbone = ResNet101_Weights.verify(weights_backbone)

    if num_classes is None:
        num_classes = 2
    if num_keypoints is None:
        num_keypoints = 17

    is_trained = weights_backbone is not None
    trainable_backbone_layers = _validate_trainable_layers(
        is_trained, trainable_backbone_layers, 5, 3
    )
    norm_layer = misc_nn_ops.FrozenBatchNorm2d if is_trained else nn.BatchNorm2d

    backbone = resnet101(
        weights=weights_backbone, progress=progress, norm_layer=norm_layer
    )
    backbone = _resnet_fpn_extractor(backbone, trainable_backbone_layers)
    model = KeypointRCNN(backbone, num_classes, num_keypoints=num_keypoints, **kwargs)

    return model


def keypointrcnn_resnet50_fpn(
    *,
    weights: Optional[KeypointRCNN_ResNet50_FPN_Weights] = None,
    progress: bool = True,
    num_classes: Optional[int] = None,
    num_keypoints: Optional[int] = None,
    weights_backbone: Optional[ResNet50_Weights] = ResNet50_Weights.IMAGENET1K_V1,
    trainable_backbone_layers: Optional[int] = None,
    **kwargs: Any,
) -> KeypointRCNN:
    weights = KeypointRCNN_ResNet50_FPN_Weights.verify(weights)
    weights_backbone = ResNet50_Weights.verify(weights_backbone)

    if weights is not None:
        weights_backbone = None
        num_classes = _ovewrite_value_param(
            "num_classes", num_classes, len(weights.meta["categories"])
        )
        num_keypoints = _ovewrite_value_param(
            "num_keypoints", num_keypoints, len(weights.meta["keypoint_names"])
        )
    else:
        if num_classes is None:
            num_classes = 2
        if num_keypoints is None:
            num_keypoints = 17

    is_trained = weights is not None or weights_backbone is not None
    trainable_backbone_layers = _validate_trainable_layers(
        is_trained, trainable_backbone_layers, 5, 3
    )
    norm_layer = misc_nn_ops.FrozenBatchNorm2d if is_trained else nn.BatchNorm2d

    backbone = resnet50(
        weights=weights_backbone, progress=progress, norm_layer=norm_layer
    )
    backbone = _resnet_fpn_extractor(backbone, trainable_backbone_layers)
    model = KeypointRCNN(backbone, num_classes, num_keypoints=num_keypoints, **kwargs)

    if weights is not None:
        model.load_state_dict(weights.get_state_dict(progress=progress))
        if weights == KeypointRCNN_ResNet50_FPN_Weights.COCO_V1:
            overwrite_eps(model, 0.0)

    return model
