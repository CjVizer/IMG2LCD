from cards.base_card import BaseCard
from constants import IMAGES
from PIL import Image, ImageTk
from tkinter import Label
from img_func import image_resize


class CardAdd(BaseCard):
    def __init__(self, master=None, command=None, *args, **kwargs):
        super(CardAdd, self).__init__(master, *args, **kwargs)
        self._image = Image.open(IMAGES.ADD)
        self._thumbnail_image = ImageTk.PhotoImage(
            image_resize(self._image, 64, 64))
        self.thumbnail_c = Label(self,
                                 image=self._thumbnail_image,
                                 borderwidth=0)
        self.thumbnail_c.pack(expand=True)
        self._command = command
        self.bind('<Button-1>', self._command)
        self.thumbnail_c.bind('<Button-1>', self._command)
