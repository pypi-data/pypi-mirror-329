from typing import Any
from tkinter.filedialog import askopenfilename
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException

from price_updater.widgets.scroll_app import ScrollApp
from price_updater.lib.language import language, Text
from price_updater.lib.settings import settings
from price_updater.lib.text_input import TextInputC
from price_updater.lib.button import ButtonC


class ChangeXlsxMenu(BoxLayout):
    def __init__(self, scrollApp: ScrollApp, popup: Popup, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.scrollapp: ScrollApp = scrollApp
        self.popup: Popup = popup
        self.orientation: str = "vertical"
        self.opacity: float = 0.8
        self.input_and_ask_open_file = BoxLayout(orientation="horizontal")
        self.add_widget(self.input_and_ask_open_file)
        self.path_xlsx_input = TextInputC(text=self.load_current_path())
        self.path_xlsx_input.focus = True
        self.path_xlsx_input.size_hint = (0.85, 0.75)
        self.input_and_ask_open_file.add_widget(self.path_xlsx_input)
        self.open_file_button = ButtonC(
            text=language.get_text(Text.SEARCH.value),
            on_release=self.choose_path,
            size_hint=(0.15, 0.75),
        )
        self.input_and_ask_open_file.add_widget(self.open_file_button)
        buttons = BoxLayout(orientation="horizontal")
        self.add_widget(buttons)
        buttons.add_widget(
            ButtonC(
                text=language.get_text(Text.MODIFY.value),
                on_release=self.add_path,
                size_hint=(0.4, 0.9),
            )
        )

    def add_path(self, instance: ButtonC) -> None:
        if self.path_xlsx_input.text != self.load_current_path():
            try:
                workbook = load_workbook(self.path_xlsx_input.text)
                if workbook is not None:
                    settings.change_xlsx_file_path(self.path_xlsx_input.text)
                    self.popup.dismiss()
                    Clock.schedule_once(self._load_assets, 0.7)
            except InvalidFileException:
                self.path_xlsx_input.text_error()
                print("we need xlsx file!")
            except KeyError:
                self.path_xlsx_input.text_error()
                print("please check xlsx format file!")
            except FileNotFoundError:
                self.path_xlsx_input.text_error()
                print("file missing :D")
        else:
            self.popup.dismiss()

    def _load_assets(self, instance: Any) -> None:
        self.scrollapp.coins_tab = self.scrollapp.get_coins_from_xlsx()
        self.scrollapp.initialize_coins(check_fetch=True)

    def load_current_path(self) -> str:
        path: str = settings.get_xlsx_file_path()
        if path == "":
            return language.get_text(Text.PATH_TO_XLSX.value)
        return settings.get_xlsx_file_path()

    def choose_path(self, instance: ButtonC) -> None:
        path: str = askopenfilename(title=language.get_text(Text.PATH_TO_XLSX.value))
        if path != "" and not isinstance(path, tuple):
            self.path_xlsx_input.text = path
