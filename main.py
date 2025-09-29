from tkinter import Tk, LEFT, Y
from tkinter import filedialog
from constants import COLORS, IMAGES
from cards_container import CardsContainer
from setup_container import SetupContainer
from cards.add_card import CardAdd
from cards.card import Card


class App(Tk):

    def __init__(self):
        super(App, self).__init__()
        self.configure(bg=COLORS.MAIN)
        self.title('IMG2LCD')
        self.iconbitmap(IMAGES.ICON)

        self._init_cards_container()
        self._init_setup_container()

        self.update()
        app_w = self.winfo_width()
        app_h = self.winfo_height() + 110
        scr_w = self.winfo_screenwidth()
        scr_h = self.winfo_screenheight()
        x = (scr_w - app_w) // 2
        y = (scr_h - app_h) // 2
        self.geometry(f'{app_w}x{app_h}+{x}+{y}')
        self.resizable(False, False)

        self.bind('<Control-KeyPress>', lambda e: self._select_all_cards(e))

    def _init_cards_container(self):
        self._cards_container = CardsContainer(self)
        self._cards_container.pack(side=LEFT, fill=Y)
        card = CardAdd(self._cards_container.container,
                       command=lambda e: self._open_files())
        self._cards_container.add_card(card)

    def _init_setup_container(self):
        self._setup_container = SetupContainer(self, self._save_files)
        self._setup_container.pack(side=LEFT, fill=Y)

    def _open_files(self):
        filetypes = (
            ('images', '.jpg .png'),
        )
        filenames = filedialog.askopenfiles(title='Load images',
                                            initialdir='/',
                                            filetypes=filetypes)

        for image in filenames:
            card = Card(self._cards_container.container,
                        image_path=image.name,
                        click_cmd=self._card_click,
                        close_cmd=self._card_delete)
            self._cards_container.add_card(card)

    def _save_files(self):
        def h_file_header(name):
            return f'#ifndef __{name.upper()}_H\n' \
                   f'#define __{name.upper()}_H\n\n'

        h_file_footer = '#endif\n\n'
        c_file = ''
        save_path = filedialog.askdirectory()
        separate_files = self._setup_container.separate_files.get()
        data = dict()

        for card in self._cards_container.get_cards():
            data[card.name] = dict()
            data[card.name]['array'] = card.converter.get_array()
            data[card.name]['extern'] = 'extern ' + \
                                        ' '.join(data[card.name]['array'].split('\n')[
                                                     0].split(' ')[1:-2]) + ';'

        if separate_files:
            for f_name, data in data.items():
                f_array = data['array']
                f_extern = data['extern']
                h_file = h_file_header(f_name)
                h_file += f_extern + '\n'
                h_file += h_file_footer
                c_file = f_array
                if save_path:
                    with open(f'{save_path}/{f_name}.h', 'w',
                              encoding='utf-8') as file:
                        file.write(h_file)
                    with open(f'{save_path}/{f_name}.c', 'w',
                              encoding='utf-8') as file:
                        file.write(c_file)
        else:
            file_name = 'images' if len(data.items()) >= 2 else list(data.keys())[0]
            h_file = h_file_header(file_name)
            for f_name, data in data.items():
                f_array = data['array']
                f_extern = data['extern']
                h_file += f_extern + '\n'
                c_file += f_array + '\n'
            h_file += '\n' + h_file_footer
            if save_path:
                with open(f'{save_path}/{file_name}.h', 'w',
                          encoding='utf-8') as file:
                    file.write(h_file)
                with open(f'{save_path}/{file_name}.c', 'w',
                          encoding='utf-8') as file:
                    file.write(c_file)

    def _card_click(self, card, ctrl=False):
        all_cards = self._cards_container.get_cards()
        selected_cards = self._cards_container.get_selected_cards()
        if ctrl and not card.is_checked:
            card.selection(True)
        elif ctrl and card.is_checked:
            card.selection(False)
        if not ctrl and not card.is_checked:
            for item in all_cards:
                item.selection(False)
            card.selection(True)
        elif not ctrl and card.is_checked:
            if len(selected_cards) == 1:
                card.selection(False)
            else:
                for item in all_cards:
                    item.selection(False)
                card.selection(True)
        self._setup_container.customize_cards(
            self._cards_container.get_selected_cards())

    def _select_all_cards(self, event):
        if event.keycode == 65:
            cards = self._cards_container.get_cards()
            selection = True if not all(
                card.is_checked for card in cards) else False
            for card in cards:
                card.selection(selection)
            self._setup_container.customize_cards(
                self._cards_container.get_selected_cards())

    def _card_delete(self, card):
        self._cards_container.delete_card(card)
        self._setup_container.customize_cards(
            self._cards_container.get_selected_cards())


if __name__ == '__main__':
    app = App()
    app.mainloop()
