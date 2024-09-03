import enum

from networks.image_processor import ImageProcessor

srgan_x2_image_processor = ImageProcessor(config_path="/app/networks/srgan_x2.json")
srgan_x4_image_processor = ImageProcessor(config_path="/app/networks/srgan_x4.json")
srgan_x8_image_processor = ImageProcessor(config_path="/app/networks/srgan_x8.json")


class Models(enum.Enum):
    srgan_x2 = srgan_x2_image_processor
    srgan_x4 = srgan_x4_image_processor
    srgan_x8 = srgan_x8_image_processor
