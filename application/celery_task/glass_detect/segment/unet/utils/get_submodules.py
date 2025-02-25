from torch import nn

from unet.blocks.simple_conv_blocks import ConvDropoutNormReLU


def get_submodules(model, modules, name_prefix=""):
    for name, module in model._modules.items():
        if isinstance(
                module,
                (
                        nn.Conv2d,
                        nn.ConvTranspose2d,
                        nn.LeakyReLU,
                        nn.InstanceNorm2d,
                        ConvDropoutNormReLU,
                ),
        ):
            modules.append([name_prefix + "." + name, module])

        else:
            # print(f"{name} is not a module")
            # print(type(module))
            get_submodules(
                module, modules, name_prefix + "." + name if name_prefix != "" else name
            )

    return modules
