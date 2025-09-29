from tkinter import Frame, Canvas, Scrollbar
from tkinter import LEFT, RIGHT, BOTTOM, Y
from constants import COLORS
from cards.card import Card


class CardsContainer(Frame):

    def __init__(self, master, *args, **kwargs):
        super(CardsContainer, self).__init__(master, *args, **kwargs)

        self._items = []

        self._create_widget()

    def _create_widget(self):
        self.configure(bg=COLORS.MAIN)

        self._canvas = Canvas(self,
                              bg=COLORS.MAIN,
                              highlightthickness=0,
                              width=240)
        self._scrollbar = Scrollbar(self,
                                    orient="vertical",
                                    command=self._canvas.yview)
        self.container = Frame(self._canvas,
                               bg=COLORS.MAIN)

        self.container.bind("<Configure>", lambda e: self._canvas_conf())
        self.container.bind("<MouseWheel>", self._mouse_scroll)
        self._canvas.create_window((0, 0),
                                   window=self.container,
                                   tags='scrollable_frame')
        self._canvas.configure(yscrollcommand=self._scrollbar.set)
        self._canvas.pack(side=LEFT, fill=Y, padx=10)
        self._scrollbar.pack(side=RIGHT, fill=Y)

    def _canvas_conf(self):
        f_h = self.container.winfo_height()
        c_h = self._canvas.winfo_height()
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))
        if f_h <= c_h:
            self._canvas.yview_moveto(1)

    def _mouse_scroll(self, event):
        if self.container.winfo_height() >= self._canvas.winfo_height():
            self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def add_card(self, card):
        card.pack(side=BOTTOM, pady=5)
        card.bind("<MouseWheel>", self._mouse_scroll)
        card.thumbnail_c.bind("<MouseWheel>", self._mouse_scroll)
        if isinstance(card, Card):
            card.name_c.bind("<MouseWheel>", self._mouse_scroll)
            card.dimensions_c.bind("<MouseWheel>", self._mouse_scroll)
            card.mode_c.bind("<MouseWheel>", self._mouse_scroll)
            card.output_c.bind("<MouseWheel>", self._mouse_scroll)
            self._items.append(card)

    def delete_card(self, card):
        self._items.remove(card)
        card.destroy()

    def get_cards(self):
        return self._items

    def get_selected_cards(self):
        return [item for item in self._items if item.is_checked]
