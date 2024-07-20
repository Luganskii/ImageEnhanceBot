import json
import torch
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

    srresnet_mini_x2.load_state_dict(torch.load(data['weights_path'], map_location=torch.device('cpu')))


__all__ = [srresnet_mini_x2]
