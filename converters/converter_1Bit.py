from converters.converter_base import BaseConverter
from PIL import Image


class Converter1Bit(BaseConverter):
    name = '1 Bit'

    @staticmethod
    def get_name():
        return Converter1Bit.name

    def get_preview(self):
        pixels = list(self._get_preview_image().getdata())
        result = []
        for pixel in pixels:
            if sum(pixel) // 3 >= self._card.scatter:
                pixel = 255
            else:
                pixel = 0
            result.append((pixel, pixel, pixel))
        img = Image.new('RGB', (self._card.width, self._card.height))
        img.putdata(result)
        return img

    def get_array(self):
        img = self.get_preview()
        pixels = list(img.getdata())
        image_bits = ''.join(['1' if p[0] else '0' for p in pixels])
        return self.format_array(image_bits)
