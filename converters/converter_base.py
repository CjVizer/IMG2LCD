from math import floor
from img_func import image_resize


class BaseConverter:

    def __init__(self, card):
        """
        Need to implement:
            self._name = string
        """

        self._card = card

    def _get_preview_image(self):
        img = self._card.image.copy()
        img = img.convert('RGB')
        return image_resize(img, self._card.width, self._card.height)

    @staticmethod
    def _to_uint(data):
        result = []
        diff = 8 - (len(data) % 8) if len(data) % 8 else 0
        data += '0' * diff
        for idx in range(0, len(data), 8):
            _byte = f"0x{int(data[idx: idx + 8], 2):02X}"
            result.append(_byte)
        return result

    def get_preview(self):
        raise NotImplementedError

    def get_array(self):
        raise NotImplementedError

    def format_array(self, data):
        name = self._card.name
        width = self._card.width
        height = self._card.height

        converter = {'1 Bit': 1,
                     'RGB111': 111,
                     'RGB232': 232,
                     'RGB565': 565,
                     'RGB888': 888}.get(self._card.converter.name, 565)

        bytes_array = self._to_uint(data)
        bytes_array.insert(0, f'0x{converter >> 8:02X}')
        bytes_array.insert(1, f'0x{converter & 0xFF:02X}')
        bytes_array.insert(2, f'0x{width >> 8:02X}')
        bytes_array.insert(3, f'0x{width & 0xFF:02X}')
        bytes_array.insert(4, f'0x{height >> 8:02X}')
        bytes_array.insert(5, f'0x{height & 0xFF:02X}')

        length = len(bytes_array)

        result = f'const char {name}[{length}] = \n'
        result += f'\t{{\n'
        result += f"\t\t{bytes_array[0]}, {bytes_array[1]}, //Type: '{self._card.converter.name}'\n"
        result += f'\t\t{bytes_array[2]}, {bytes_array[3]}, //Image width: {width}\n'
        result += f'\t\t{bytes_array[4]}, {bytes_array[5]}, //Image height: {height}\n'

        lines = ''
        line = f'\t\t{bytes_array[6]}'
        for item in bytes_array[7:]:

            if len(f'{line}, {item}') <= 80:
                line = f'{line}, {item}'
            else:
                lines += f'{line},\n'
                line = f'\t\t{item}'
        lines += f'{line}\n'

        result += lines
        result += f'\t}};\n'

        return result
