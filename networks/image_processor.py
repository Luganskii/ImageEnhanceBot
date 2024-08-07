import json
from datetime import datetime

import torch
from PIL import Image
from torchvision import transforms

from networks.srresnet import SRResNet


class ImageProcessor:

    def __init__(self, config_path: str):
        with open(config_path) as f:
            config_data = json.load(f)
            scaling_factor = config_data['scaling_factor']
            in_channels = config_data['in_channels']
            out_channels = config_data['out_channels']
            channels = config_data['channels']
            num_rcb = config_data['num_rcb']
            weights_path = config_data['weights_path']

            self.model = SRResNet(upscale=scaling_factor,
                                  in_channels=in_channels,
                                  out_channels=out_channels,
                                  channels=channels,
                                  num_rcb=num_rcb)

            self.model.load_state_dict(torch.load(weights_path, map_location=torch.device('cpu')))
            self.scaling_factor = scaling_factor

        self.transform_to_tensor = transforms.Compose([
            transforms.ToTensor(),
            transforms.Lambda(lambda x: x.unsqueeze(0))])

        self.transform_to_picture = transforms.Compose([
            transforms.Lambda(lambda x: x.squeeze(0)),
            transforms.ToPILImage()])

    def __image_to_tensor(self, image) -> torch.tensor:
        return self.transform_to_tensor(image)

    def __tensor_to_image(self, output):
        return self.transform_to_picture(output)

    def __patch_iterator(self, x_step: int, y_step: int, tensor: torch.tensor):
        _, _, height, width = tensor.shape
        for i in range(0, height, x_step):
            for j in range(0, width, y_step):
                x_lim = min(i + x_step, height)
                y_lim = min(j + y_step, width)
                yield tensor[:, :, i:x_lim, j:y_lim], (i, j, x_lim, y_lim)

    def update(self, path_to_picture, x_step:int = 512, y_step:int = 512):

        image = Image.open(path_to_picture)
        tensor = self.__image_to_tensor(image)

        _, channels, height, width = tensor.shape
        output = torch.zeros((channels, height * self.scaling_factor, width * self.scaling_factor))
        for patch, (i, j, height, width) in self.__patch_iterator(x_step=x_step, y_step=y_step, tensor=tensor):
            with torch.no_grad():
                pred = self.model(patch)

            output[:, i * self.scaling_factor:height * self.scaling_factor, j * self.scaling_factor:width * self.scaling_factor] = pred[0,:]

        sr_picture = self.__tensor_to_image(output)
        now = datetime.now()
        path_to_sr_picture = f'/app/media/{now.strftime("%d-%H-%M-%S.png")}.png'
        sr_picture.save(path_to_sr_picture)

        return path_to_sr_picture
