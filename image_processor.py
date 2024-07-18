import numpy as np
import torch
from PIL import Image


class ImageProcessor:

    def __init__(self, path_to_picture: str):
        self.image = Image.open(path_to_picture)
        self.tensor = self.image_to_tensor()

    def image_to_tensor(self) -> torch.tensor:
        # tensor.shape is [batch = 1, channels = 3, height, width]
        # lr [0, 255] -> [-1, 1]
        return (torch.from_numpy(np.array(self.image)).permute(2, 0, 1).float() / (255 / 2) - 1).unsqueeze(0)

    def tensor_to_image(self, output):
        # sr [-1, 1] -> [0, 255]
        image_array = ((output.permute(1, 2, 0) + 1) * (255 / 2)).numpy().astype(np.uint8)
        self.image = Image.fromarray(image_array)
        return self.image

    def patch_iterator(self, x_step: int, y_step: int):
        _, _, height, width = self.tensor.shape
        for i in range(0, height, x_step):
            for j in range(0, width, y_step):
                x_lim = min(i + x_step, height)
                y_lim = min(j + y_step, width)
                yield self.tensor[:, :, i:x_lim, j:y_lim], (i, j, x_lim, y_lim)

    def process(self, model, scaling_factor, x_step:int = 256, y_step:int = 256):
        _, channels, height, width = self.tensor.shape
        output = torch.zeros((channels, height * scaling_factor, width * scaling_factor))
        for patch, (i, j, height, width) in self.patch_iterator(x_step=x_step, y_step=y_step):
            with torch.no_grad():
                pred = model(patch)

            output[:, i * scaling_factor:height * scaling_factor, j * scaling_factor:width * scaling_factor] = pred[0,:]

        return self.tensor_to_image(output)
