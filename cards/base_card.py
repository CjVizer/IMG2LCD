from tkinter import Frame
from constants import COLORS


class BaseCard(Frame):
    def __init__(self, master=None, *args, **kwargs):
        super(BaseCard, self).__init__(master, *args, **kwargs)
        self.configure(width=240,
                       height=84,
                       bg=COLORS.CARD_BG)
        self.pack_propagate(False)
