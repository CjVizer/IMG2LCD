from converters.converter_base import BaseConverter
from PIL import Image


class ConverterRGB111(BaseConverter):
    name = 'RGB111'

    @staticmethod
    def get_name():
        return ConverterRGB111.name

    def get_preview(self):
        pixels = list(self._get_preview_image().getdata())
        result = [(c[0] & 0x80, c[1] & 0x80, c[2] & 0x80) for c in pixels]
        img = Image.new('RGB', (self._card.width, self._card.height))
        img.putdata(result)
        return img

    def get_array(self):
        img = self.get_preview()
        pixels = list(img.getdata())
        image_bits = ''.join([f'{format(p[0], "08b")[:1]}'
                              f'{format(p[1], "08b")[:1]}'
                              f'{format(p[2], "08b")[:1]}' for p in pixels])
        return self.format_array(image_bits)
