import string
from tkinter import Frame, LabelFrame, Label, Entry, Scale, Button, Checkbutton
from tkinter import Y, SUNKEN, RIGHT, DISABLED, END, NORMAL, HORIZONTAL
from tkinter import BooleanVar
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
from img_func import image_fit_to
from constants import CONVERTERS, PATHS, COLORS, FONTS, IMAGES
from converters.converter_1Bit import Converter1Bit


class SetupContainer(Frame):
    def __init__(self, master, save_cmd=None, *args, **kwargs):
        super(SetupContainer, self).__init__(master, *args, **kwargs)

        self._original_img = None
        self._preview_img = None
        self._selected_cards = list()
        self._temp_names = [f'image_{idx}' for idx in range(1, 100)]
        self._save_cmd = save_cmd
        self.separate_files = BooleanVar()

        self._create_widget()

    def _create_widget(self):
        self.configure(width=542, bg=COLORS.MAIN)
        self._ratio_img = Image.open(IMAGES.RATIO_UNBLOCKED)
        self._ratio_img = ImageTk.PhotoImage(self._ratio_img)

        self._original_c = LabelFrame(self,
                                      text='Original',
                                      width=256,
                                      height=256,
                                      bg=COLORS.MAIN,
                                      fg=COLORS.CARD_TEXT,
                                      relief=SUNKEN
                                      )
        self._preview_c = LabelFrame(self,
                                     text='Preview',
                                     width=256,
                                     height=256,
                                     bg=COLORS.MAIN,
                                     fg=COLORS.CARD_TEXT,
                                     relief=SUNKEN
                                     )

        self._original_lbl = Label(self._original_c,
                                   text='Original',
                                   bg=COLORS.MAIN,
                                   fg=COLORS.CARD_BG,
                                   font='Inter 16 bold')

        name_validate = (self.register(self._name_validate), '%P')

        self._name_lbl = Label(self,
                               text='Name:',
                               font=FONTS.CARD,
                               bg=COLORS.MAIN,
                               fg=COLORS.CARD_TEXT,
                               state=DISABLED)

        self._name_entry = Entry(self,
                                 width=20,
                                 justify=RIGHT,
                                 state=DISABLED,
                                 disabledbackground=COLORS.DISABLED_ENTRY,
                                 validate='key',
                                 validatecommand=name_validate
                                 )

        self._mode_lbl = Label(self,
                               text='Mode:',
                               font=FONTS.CARD,
                               bg=COLORS.MAIN,
                               fg=COLORS.CARD_TEXT,
                               state=DISABLED)

        self._mode_entry = Combobox(self,
                                    values=[cnv.name for cnv in CONVERTERS],
                                    state=DISABLED,
                                    width=17)

        self._scatter_lbl = Label(self,
                                  text='Scatter:',
                                  font=FONTS.CARD,
                                  bg=COLORS.MAIN,
                                  fg=COLORS.CARD_TEXT,
                                  state=DISABLED)

        self._scatter_entry = Scale(self,
                                    from_=0,
                                    to=255,
                                    orient=HORIZONTAL,
                                    length=124,
                                    bg=COLORS.MAIN,
                                    highlightthickness=0,
                                    fg='gray',
                                    state=DISABLED,
                                    command=lambda e: self._scatter_event())

        w_h_validate = (self.register(self._w_h_validate), '%P')

        self._width_lbl = Label(self,
                                text='Width:',
                                font=FONTS.CARD,
                                bg=COLORS.MAIN,
                                fg=COLORS.CARD_TEXT,
                                state=DISABLED)

        self._width_entry = Entry(self,
                                  width=6,
                                  justify=RIGHT,
                                  state=DISABLED,
                                  disabledbackground=COLORS.DISABLED_ENTRY,
                                  validate='key',
                                  validatecommand=w_h_validate)

        self._height_lbl = Label(self,
                                 text='Height:',
                                 font=FONTS.CARD,
                                 bg=COLORS.MAIN,
                                 fg=COLORS.CARD_TEXT,
                                 state=DISABLED)

        self._height_entry = Entry(self,
                                   width=6,
                                   justify=RIGHT,
                                   state=DISABLED,
                                   disabledbackground=COLORS.DISABLED_ENTRY,
                                   validate='key',
                                   validatecommand=w_h_validate)

        self._ratio_entry = Label(self,
                                  image=self._ratio_img,
                                  border=0,
                                  bg=COLORS.MAIN)

        self._separate_lbl = Label(self,
                                   text='Separate files',
                                   bg=COLORS.MAIN,
                                   fg=COLORS.CARD_TEXT)

        self.separate_entry = Checkbutton(self,
                                          bg=COLORS.MAIN,
                                          activebackground=COLORS.MAIN,
                                          variable=self.separate_files)

        self._save_button = Button(self,
                                   text='Save',
                                   width=6,
                                   command=self._save_cmd)

        def s_w():
            return self._width_entry.get()

        def s_h():
            return self._height_entry.get()

        self._width_entry.bind('<KeyRelease>',
                               lambda e: self._w_h_typing(e, 'w', s_w()))
        self._height_entry.bind('<KeyRelease>',
                                lambda e: self._w_h_typing(e, 'h', s_h()))
        self._name_entry.bind('<KeyRelease>',
                              lambda e: self._name_typing())
        self._mode_entry.bind('<<ComboboxSelected>>',
                              lambda e: self._mode_selection())
        self._ratio_entry.bind('<Button-1>', lambda e: self._ratio_event())
        self._width_entry.bind('<MouseWheel>',
                               lambda e: self._w_h_wheel(e,
                                                         self._width_entry,
                                                         'w'))
        self._height_entry.bind('<MouseWheel>',
                                lambda e: self._w_h_wheel(e,
                                                          self._height_entry,
                                                          'h'))

        self._original_c.pack_propagate(False)
        self._preview_c.pack_propagate(False)
        self._original_lbl.pack(expand=True)

        self._original_c.place(x=10, y=10)
        self._preview_c.place(x=276, y=10)
        self._name_lbl.place(x=10, y=276)
        self._name_entry.place(x=74, y=276)
        self._mode_lbl.place(x=10, y=312)
        self._mode_entry.place(x=74, y=312)
        self._scatter_lbl.place(x=10, y=348)
        self._scatter_entry.place(x=74, y=330)
        self._width_lbl.place(x=276, y=276)
        self._width_entry.place(x=340, y=276)
        self._height_lbl.place(x=276, y=312)
        self._height_entry.place(x=340, y=312)
        self._ratio_entry.place(x=386, y=288)
        self._separate_lbl.place(x=405, y=348)
        self.separate_entry.place(x=380, y=348)
        self._save_button.place(x=485, y=348)

        self._show_preview(text='Preview')

    def customize_cards(self, cards: list):
        self._selected_cards = cards
        self.focus_force()
        for item in self._original_c.winfo_children():
            item.pack_forget()

        if not self._selected_cards:
            self._original_lbl.configure(text='Original')
            self._original_lbl.pack(expand=True)
            self._show_preview(text='Preview', clear=True)
        elif len(self._selected_cards) == 1:
            self._show_original(self._selected_cards[0])
            self._show_preview(self._selected_cards[0], clear=True)
        else:
            self._original_lbl.configure(text='Multiple selection')
            self._original_lbl.pack(expand=True)
            self._show_preview(text='Multiple selection', clear=True)

        self._show_parameters()

    def _show_original(self, card):
        self._original_img = card.image
        self._original_img_pi = ImageTk.PhotoImage(
            image_fit_to(card.image, 224, 224))
        self._original_img_c = Label(self._original_c,
                                     image=self._original_img_pi,
                                     border=0)
        self._original_img_c.pack(expand=True)

    def _show_preview(self, card=None, text='', clear=False):
        if clear:
            for item in self._preview_c.winfo_children():
                item.destroy()
        if card:
            img = card.converter.get_preview()
            img = image_fit_to(img, 224, 224)
            self._preview_img = ImageTk.PhotoImage(img)
            if clear:
                self._preview_img_c = Label(self._preview_c,
                                            image=self._preview_img,
                                            border=0)
                self._preview_img_c.pack(expand=True)
            else:
                self._preview_img_c.configure(image=self._preview_img)
        if text:
            self._preview_lbl = Label(self._preview_c,
                                      text=text,
                                      bg=COLORS.MAIN,
                                      fg=COLORS.CARD_BG,
                                      font='Inter 16 bold')
            self._preview_lbl.pack(expand=True)

    def _show_parameters(self):
        cards = self._selected_cards

        if len(cards) == 1:
            self._name_state(enable=True)
            self._mode_state(enable=True)
            self._scatter_state(enable=True)
            self._width_state(enable=True)
            self._height_state(enable=True)
            self._ratio_state(enable=True)
        elif len(cards) > 1:
            self._name_state(enable=False)
            self._mode_state(enable=True)
            self._scatter_state(enable=False)
            self._width_state(enable=True)
            self._height_state(enable=True)
            self._ratio_state(enable=True)
        else:
            self._name_state(enable=False)
            self._mode_state(enable=False)
            self._scatter_state(enable=False)
            self._width_state(enable=False)
            self._height_state(enable=False)
            self._ratio_state(enable=False)

    def _name_state(self, enable=False):
        self._name_entry.delete(0, END)
        if enable:
            self._name_lbl.configure(state=NORMAL)
            self._name_entry.configure(state=NORMAL)
            self._name_entry.insert(0, self._selected_cards[0].name)
        else:
            self._name_lbl.configure(state=DISABLED)
            self._name_entry.configure(state=DISABLED)

    def _mode_state(self, enable=False):
        self._mode_entry.set('')
        if enable:
            self._mode_lbl.configure(state=NORMAL)
            self._mode_entry.configure(state='readonly')
            if len(self._selected_cards) == 1:
                self._mode_entry.current(
                    [cnv.name for cnv in CONVERTERS].index(
                        self._selected_cards[0].converter.get_name()))
            else:
                e_md = self._selected_cards[0].converter.get_name()
                for card in self._selected_cards:
                    e_md = e_md if card.converter.get_name() == e_md else None
                if e_md:
                    self._mode_entry.current(
                        [cnv.name for cnv in CONVERTERS].index(
                            self._selected_cards[0].converter.get_name()))
        else:
            self._mode_lbl.configure(state=DISABLED)
            self._mode_entry.configure(state=DISABLED)

    def _scatter_state(self, enable=False):
        self._scatter_entry.set(0)
        if enable:
            if isinstance(self._selected_cards[0].converter, Converter1Bit):
                self._scatter_lbl.configure(state=NORMAL)
                self._scatter_entry.configure(state=NORMAL, fg=COLORS.CARD_TEXT)
                self._scatter_entry.set(self._selected_cards[0].scatter)
            else:
                self._scatter_lbl.configure(state=DISABLED)
                self._scatter_entry.configure(state=DISABLED, fg='gray')
        else:
            self._scatter_lbl.configure(state=DISABLED)
            self._scatter_entry.configure(state=DISABLED, fg='gray')

    def _width_state(self, enable=False):
        self._width_entry.delete(0, END)
        if enable:
            self._width_lbl.configure(state=NORMAL)
            self._width_entry.configure(state=NORMAL)
            if len(self._selected_cards) == 1:
                self._width_entry.insert(0, self._selected_cards[0].width)
            else:
                e_width = self._selected_cards[0].width
                for card in self._selected_cards:
                    e_width = e_width if card.width == e_width else None
                if e_width:
                    self._width_entry.insert(0, e_width)
        else:
            self._width_lbl.configure(state=DISABLED)
            self._width_entry.configure(state=DISABLED)

    def _height_state(self, enable=False):
        self._height_entry.delete(0, END)
        if enable:
            self._height_lbl.configure(state=NORMAL)
            self._height_entry.configure(state=NORMAL)
            if len(self._selected_cards) == 1:
                self._height_entry.insert(0, self._selected_cards[0].height)
            else:
                e_height = self._selected_cards[0].height
                for card in self._selected_cards:
                    e_height = e_height if card.height == e_height else None
                if e_height:
                    self._height_entry.insert(0, e_height)
        else:
            self._height_lbl.configure(state=DISABLED)
            self._height_entry.configure(state=DISABLED)

    def _ratio_state(self, enable=False):
        if enable:
            self._ratio_entry.configure(cursor='sb_v_double_arrow')
            if len(self._selected_cards) == 1:
                if self._selected_cards[0].ratio_blocked:
                    self._ratio_img = Image.open(
                        IMAGES.RATIO_BLOCKED)
                else:
                    self._ratio_img = Image.open(
                        IMAGES.RATIO_UNBLOCKED)
            else:
                e_rt = self._selected_cards[0].ratio_blocked
                for card in self._selected_cards:
                    e_rt = e_rt if card.ratio_blocked == e_rt else None
                if e_rt:
                    self._ratio_img = Image.open(
                        IMAGES.RATIO_BLOCKED)
                else:
                    self._ratio_img = Image.open(
                        IMAGES.RATIO_UNBLOCKED)
        else:
            self._ratio_entry.configure(cursor='arrow')
            self._ratio_img = Image.open(
                IMAGES.RATIO_UNBLOCKED)

        self._ratio_img = ImageTk.PhotoImage(self._ratio_img)
        self._ratio_entry.configure(image=self._ratio_img)

    @staticmethod
    def _w_h_validate(value):
        if value:
            try:
                int(value)
                if value.isdigit():
                    return True
                else:
                    return False
            except ValueError:
                return False
        else:
            return True

    def _w_h_typing(self, event, side, value):
        if event.char in (str(num) for num in range(10)) or \
                event.keycode in (8,):

            value = int(value) if value else 0
            w_val = int(
                self._width_entry.get()) if self._width_entry.get() else 0
            h_val = int(
                self._height_entry.get()) if self._height_entry.get() else 0

            for card in self._selected_cards:
                o_w, o_h = card.image.size
                aspect_ratio = o_w / o_h
                w, h = '', ''

                if card.ratio_blocked:
                    if value and side == 'w':
                        w = value
                        h = round(value / aspect_ratio)
                    elif value and side == 'h':
                        w = round(value * aspect_ratio)
                        h = value
                else:
                    if value and side == 'w':
                        w = value
                        h = h_val
                    elif value and side == 'h':
                        w = w_val
                        h = value

                card.set_dimensions(w if w else 1,
                                    h if h else 1)

                if len(self._selected_cards) == 1:
                    self._show_preview(self._selected_cards[0])
                    self._width_entry.delete(0, END)
                    self._height_entry.delete(0, END)
                    self._width_entry.insert(0, str(w))
                    self._height_entry.insert(0, str(h))
                elif len(self._selected_cards) > 1 and side == 'w':
                    self._width_entry.delete(0, END)
                    self._height_entry.delete(0, END)
                    self._width_entry.insert(0, str(w))
                elif len(self._selected_cards) > 1 and side == 'h':
                    self._width_entry.delete(0, END)
                    self._height_entry.delete(0, END)
                    self._height_entry.insert(0, str(h))

    def _w_h_wheel(self, event, entry, side):
        class Event:
            char = '1'
            keycode = 8

        value = -1 if event.delta < 0 else 1
        if len(self._selected_cards) == 1:
            num = int(entry.get()) if entry.get() else 0
            num += value
            if num:
                self._w_h_typing(Event, side, num)

    @staticmethod
    def _name_validate(value):
        if value and value[0] in string.ascii_lowercase:
            for letter in value:
                if letter in string.ascii_lowercase + string.digits + '_':
                    continue
                else:
                    return False
            return True
        elif not value:
            return True
        else:
            return False

    def _name_typing(self):
        if len(self._selected_cards) == 1:
            new_name = self._name_entry.get()
            if not new_name:
                new_name = self._temp_names.pop(0)
                self._temp_names.append(new_name)
            self._selected_cards[0].set_name(new_name)

    def _mode_selection(self):
        for card in self._selected_cards:
            card.set_converter(CONVERTERS[self._mode_entry.current()])
        if len(self._selected_cards) == 1:
            self._show_preview(self._selected_cards[0])
            self._show_parameters()
        self.focus_force()

    def _scatter_event(self):
        if len(self._selected_cards) == 1:
            card = self._selected_cards[0]
            if isinstance(card.converter, Converter1Bit):
                card.scatter = self._scatter_entry.get()
                self._show_preview(card)

    def _ratio_event(self):
        if len(self._selected_cards) == 1:
            self._selected_cards[0].ratio_blocked = not self._selected_cards[
                0].ratio_blocked
        elif len(self._selected_cards) > 1:
            e_ratio = self._selected_cards[0].ratio_blocked
            for card in self._selected_cards:
                e_ratio = e_ratio if card.ratio_blocked == e_ratio else None
            if e_ratio:
                e_ratio = False
            else:
                e_ratio = True
            for card in self._selected_cards:
                card.ratio_blocked = e_ratio

        self._show_parameters()
