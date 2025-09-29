import sys
from converters.converter_1Bit import Converter1Bit
from converters.converter_rgb111 import ConverterRGB111
from converters.converter_rgb232 import ConverterRGB232
from converters.converter_rgb565 import ConverterRGB565
from converters.converter_rgb888 import ConverterRGB888

CONVERTERS = [
    Converter1Bit,
    ConverterRGB111,
    ConverterRGB232,
    ConverterRGB565,
    ConverterRGB888
]


class PATHS:
    if getattr(sys, 'frozen', False):
        BASE = sys._MEIPASS + '\\'
    else:
        BASE = __file__.rsplit('\\', 1)[0] + '\\'

    IMAGES = BASE + 'images' + '\\'


class IMAGES:
    ICON = PATHS.IMAGES + 'icon.ico'
    ADD = PATHS.IMAGES + 'add_img.png'
    CLOSE = PATHS.IMAGES + 'close.png'
    RATIO_BLOCKED = PATHS.IMAGES + 'ratio_blocked.png'
    RATIO_UNBLOCKED = PATHS.IMAGES + 'ratio_unblocked.png'


class COLORS:
    MAIN = '#333333'
    CARD_BG = '#464646'
    CARD_BG_SELECTED = '#4F3939'
    CARD_TEXT = '#E9E9E9'
    CODE_TEXT = '#AB8D41'
    SEPARATOR = '#EFEFEF'
    DISABLED_ENTRY = '#777777'


class FONTS:
    CARD = 'INTER 8'
