from torch import nn

from ..network.unet import PlainConvUNet


def create_unet(**kwargs):
    default_config = {
        "input_channels": 3,
        "n_stages": 9,
        "features_per_stage": (32, 64, 128, 256, 512, 512, 512, 512, 512),
        "conv_op": nn.Conv2d,
        "kernel_sizes": 3,
        "strides": [
            [1, 1],
            [2, 2],
            [2, 2],
            [2, 2],
            [2, 2],
            [2, 2],
            [2, 2],
            [2, 2],
            [1, 2],
        ],
        "n_conv_per_stage": (2, 2, 2, 2, 2, 2, 2, 2, 2),
        "num_classes": 2,
        "n_conv_per_stage_decoder": (2, 2, 2, 2, 2, 2, 2, 2),
        "conv_bias": True,
        "norm_op": nn.InstanceNorm2d,
        "norm_op_kwargs": {"eps": 1e-05, "affine": True},
        "dropout_op": None,
        "dropout_op_kwargs": None,
        "nonlin": nn.LeakyReLU,
        "nonlin_kwargs": {"inplace": True},
        "deep_supervision": True,
        "nonlin_first": False,
    }

    # assert all(k in default_config.keys() for k in kwargs.keys())
    for key in kwargs.keys():
        assert key in default_config.keys(), f"{key} is not a valid key"
    config = {**default_config, **kwargs}

    model = PlainConvUNet(**config)

    return model
