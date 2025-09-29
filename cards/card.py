from cards.base_card import BaseCard
from PIL import Image, ImageTk
from img_func import image_resize
from constants import IMAGES, COLORS, FONTS
from converters.converter_rgb565 import ConverterRGB565
from tkinter import Label, PhotoImage


class Card(BaseCard):
    def __init__(self,
                 master,
                 image_path: str,
                 click_cmd=None,
                 close_cmd=None,
                 *args,
                 **kwargs):
        super(Card, self).__init__(master, *args, **kwargs)
        self.image = Image.open(image_path)
        self._thumbnail_image = ImageTk.PhotoImage(
            image_resize(self.image, 64, 64))
        self.name = image_path.split(".")[0].split("/")[-1].lower()
        self.converter = ConverterRGB565(self)
        self.output_type = 'UINT8_T'
        self.scatter = 128
        self.ratio_blocked = True
        self.width = self.image.width
        self.height = self.image.height
        self._click_cmd = click_cmd
        self._close_cmd = close_cmd
        self.is_checked = False

        self._create_widget()

    def _create_widget(self):
        self._close_img = PhotoImage(file=IMAGES.CLOSE)

        self.thumbnail_c = Label(self,
                                 image=self._thumbnail_image,
                                 borderwidth=0)

        self._close_img_c = Label(self,
                                  image=self._close_img,
                                  borderwidth=0,
                                  cursor='hand1')

        self.name_c = Label(self,
                            text=f'Name: {self.name}',
                            bg=COLORS.CARD_BG,
                            fg=COLORS.CARD_TEXT,
                            font=FONTS.CARD)

        self.dimensions_c = Label(self,
                                  text=f'Dimensions:'
                                       f' {self.width}x{self.height}',
                                  bg=COLORS.CARD_BG,
                                  fg=COLORS.CARD_TEXT,
                                  font=FONTS.CARD)

        self.mode_c = Label(self,
                            text=f'Mode: {self.converter.get_name()}',
                            bg=COLORS.CARD_BG,
                            fg=COLORS.CARD_TEXT,
                            font=FONTS.CARD)

        self.output_c = Label(self,
                              text=f'Output: {self.output_type}',
                              bg=COLORS.CARD_BG,
                              fg=COLORS.CARD_TEXT,
                              font=FONTS.CARD)

        self.thumbnail_c.place(x=10, y=10)
        self._close_img_c.place(x=220, y=10)
        self.name_c.place(x=84, y=6)
        self.dimensions_c.place(x=84, y=26)
        self.mode_c.place(x=84, y=42)
        self.output_c.place(x=84, y=58)

        self._bind_config('<Button-1>', lambda e: self._click_cmd(self))
        self._bind_config('<Control-Button-1>',
                          lambda e: self._click_cmd(self, True))
        self._close_img_c.bind('<Button-1>', lambda e: self._close_cmd(self))

    def _bind_config(self, event, func):
        self.bind(event, func)
        self.thumbnail_c.bind(event, func)
        self.name_c.bind(event, func)
        self.dimensions_c.bind(event, func)
        self.mode_c.bind(event, func)
        self.output_c.bind(event, func)

    def selection(self, select=False):
        self.is_checked = select
        color = COLORS.CARD_BG if not select else COLORS.CARD_BG_SELECTED
        self.configure(bg=color)
        self.name_c.configure(bg=color)
        self.dimensions_c.configure(bg=color)
        self.mode_c.configure(bg=color)
        self.output_c.configure(bg=color)

    def set_name(self, name):
        self.name = name
        self.name_c.configure(text=f'Name: {self.name}')

    def set_dimensions(self, width, height):
        self.width = width
        self.height = height
        self.dimensions_c.configure(text=f'Dimensions: '
                                         f'{self.width}x{self.height}')

    def set_converter(self, converter):
        self.converter = converter(self)
        self.mode_c.configure(text=f'Mode: {self.converter.get_name()}')

    def set_output(self, output_type):
        self.output_type = output_type
        self.output_c.configure(text=f'Output: {self.output_type}')
