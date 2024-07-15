import json
from .srresnet import SRResNet


with open('config.json') as f:
    data = json.load(f)
    large_kernel_size = data['large_kernel_size']
    small_kernel_size = data['small_kernel_size']
    n_channels = data['n_channels']
    n_blocks = data['n_blocks']
    scaling_factor = data['scaling_factor']

    srresnet_mini_x2 = SRResNet(large_kernel_size=large_kernel_size,
                                small_kernel_size=small_kernel_size,
                                n_channels=n_channels, n_blocks=n_blocks,
                                scaling_factor=scaling_factor)

    # TODO загрузить веса


__all__ = [srresnet_mini_x2]
