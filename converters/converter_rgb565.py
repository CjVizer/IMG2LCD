from converters.converter_base import BaseConverter
from PIL import Image


class ConverterRGB565(BaseConverter):
    name = 'RGB565'

    @staticmethod
    def get_name():
        return ConverterRGB565.name

    def get_preview(self):
        pixels = list(self._get_preview_image().getdata())
        result = [(c[0] & 0xf8, c[1] & 0xfc, c[2] & 0xf8) for c in pixels]
        img = Image.new('RGB', (self._card.width, self._card.height))
        img.putdata(result)
        return img

    def get_array(self):
        img = self.get_preview()
        pixels = list(img.getdata())
        image_bits = ''.join([f'{format(p[0], "08b")[:5]}'
                              f'{format(p[1], "08b")[:6]}'
                              f'{format(p[2], "08b")[:5]}' for p in pixels])
        return self.format_array(image_bits)
