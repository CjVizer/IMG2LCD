from converters.converter_base import BaseConverter


class ConverterRGB888(BaseConverter):
    name = 'RGB888'

    @staticmethod
    def get_name():
        return ConverterRGB888.name

    def get_preview(self):
        return self._get_preview_image()

    def get_array(self):
        img = self.get_preview()
        pixels = list(img.getdata())
        image_bits = ''.join([f'{format(p[0], "08b")}'
                              f'{format(p[1], "08b")}'
                              f'{format(p[2], "08b")}' for p in pixels])
        return self.format_array(image_bits)
