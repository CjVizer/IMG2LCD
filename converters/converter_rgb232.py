from converters.converter_base import BaseConverter
from PIL import Image


class ConverterRGB232(BaseConverter):
    name = 'RGB232'

    @staticmethod
    def get_name():
        return ConverterRGB232.name

    def get_preview(self):
        pixels = list(self._get_preview_image().getdata())
        result = [(c[0] & 0xc0, c[1] & 0xe0, c[2] & 0xc0) for c in pixels]
        img = Image.new('RGB', (self._card.width, self._card.height))
        img.putdata(result)
        return img

    def get_array(self):
        img = self.get_preview()
        pixels = list(img.getdata())
        image_bits = ''.join([f'{format(p[0], "08b")[:2]}'
                              f'{format(p[1], "08b")[:3]}'
                              f'{format(p[2], "08b")[:2]}' for p in pixels])
        return self.format_array(image_bits)
