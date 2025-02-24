from typing import Any
import sys
import subprocess
import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.clock import Clock
from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException

from price_updater.widgets.menu import Menu
from price_updater.widgets.scroll_app import ScrollApp
from price_updater.widgets.change_xlsx_menu import ChangeXlsxMenu
from price_updater.lib.button import ButtonC, TooltipMDIconButton
from price_updater.lib.language import language, Text
from price_updater.lib.settings import settings, Languages
from price_updater.lib.update import Update
from price_updater.lib.config import (
    color_orange_theme,
    color_behind_window,
    color_window,
    color_behind_info,
    color_success_info,
    color_error_info,
    color_top_bar_button,
    color_background_input,
    color_top_bar,
    font_config,
)


class TopBar(BoxLayout):
    def __init__(self, scrollapp: ScrollApp, right_side: Menu, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.scrollapp = scrollapp
        self.right_side = right_side

        self.create_gui()

        self.add_widget(self.change_loc_button)
        self.add_widget(BoxLayout(size_hint=(0.002, 1)))
        self.add_widget(self.update_button)
        self.add_widget(BoxLayout(size_hint=(0.002, 1)))
        self.add_widget(self.refresh_button)
        self.add_widget(BoxLayout(size_hint=(0.002, 1)))
        if platform.system() == "Windows":
            self.add_widget(self.open_xlsx)
        self.add_widget(BoxLayout(size_hint=(1, 1)))
        self.add_widget(self.api_button)
        self.add_widget(self.language_button)

    def create_gui(self) -> None:
        self.height = 35
        self.change_loc_button = TooltipMDIconButton(
            tooltip_text=language.get_text(Text.CHANGE_XLSX_WORKBOOK.value),
            icon="application-cog",
            md_bg_color=color_top_bar_button,
            theme_icon_color="Custom",
            icon_color=color_orange_theme,
            icon_size="28sp",
            size_hint=(0.12, 1),
        )
        self.update_button = TooltipMDIconButton(
            tooltip_text=language.get_text(Text.UPDATE.value),
            icon="file-download",
            md_bg_color=color_top_bar_button,
            theme_icon_color="Custom",
            icon_color=color_orange_theme,
            icon_size="28sp",
            size_hint=(0.12, 1),
        )
        self.refresh_button = TooltipMDIconButton(
            tooltip_text=language.get_text(Text.REFRESH_DATA.value),
            icon="web-refresh",
            md_bg_color=color_top_bar_button,
            theme_icon_color="Custom",
            icon_color=color_orange_theme,
            icon_size="28sp",
            size_hint=(0.12, 1),
        )
        self.refresh_button.bind(on_release=self.scrollapp.refresh_assets)
        self.open_xlsx = TooltipMDIconButton(
            tooltip_text=language.get_text(Text.OPEN_XLSX.value),
            icon="microsoft-excel",
            md_bg_color=color_top_bar_button,
            theme_icon_color="Custom",
            icon_color=color_orange_theme,
            icon_size="28sp",
            size_hint=(0.12, 1),
        )
        self.open_xlsx.bind(on_release=self.open_xlsx_file)
        self.language_list_buttons = DropDown()
        self.btn_en = ButtonC(
            text=Languages.EN.value,
            size_hint=(1, None),
            height=40,
        )
        self.btn_en.md_bg_color = color_top_bar
        self.btn_pl = ButtonC(
            text=Languages.PL.value,
            size_hint=(1, None),
            height=40,
        )
        self.btn_pl.md_bg_color = color_top_bar
        self.btn_de = ButtonC(
            text=Languages.DE.value,
            size_hint=(1, None),
            height=40,
        )
        self.btn_de.md_bg_color = color_top_bar
        self.btn_en.bind(on_release=self.change_language)
        self.btn_pl.bind(on_release=self.change_language)
        self.btn_de.bind(on_release=self.change_language)
        self.language_list_buttons.add_widget(self.btn_en)
        self.language_list_buttons.add_widget(self.btn_pl)
        self.language_list_buttons.add_widget(self.btn_de)
        self.api_button = TooltipMDIconButton(
            tooltip_text=language.get_text(Text.CHANGE_API.value),
            icon=language.get_text(Text.CHANGE_API.value),
            md_bg_color=color_top_bar_button,
            theme_icon_color="Custom",
            icon_color=(
                color_orange_theme
                if settings.get_api_status() == "api-on"
                else color_background_input
            ),
            icon_size="28sp",
            size_hint=(0.12, 1),
            pos=(350, 300),
        )
        self.api_button.bind(on_release=self.change_api_status)
        self.language_button = TooltipMDIconButton(
            tooltip_text=language.get_text(Text.CHANGE_LANGUAGE.value),
            icon="translate",
            md_bg_color=color_top_bar_button,
            theme_icon_color="Custom",
            icon_color=color_orange_theme,
            icon_size="28sp",
            size_hint=(0.12, 1),
            pos=(350, 300),
        )
        self.language_button.bind(on_release=self.language_list_buttons.open)
        self.language_list_buttons.bind(
            on_select=lambda instance, x: setattr(
                self.language_button, "text_language", x
            )
        )

        self.change_loc_button.bind(on_release=self.change_loc)
        self.update_button.bind(on_release=self.update)

    def change_api_status(self, instance: ButtonC) -> None:
        if settings.get_api_status() == "api-off":
            settings.change_api_status("api-on")
            self.api_button.icon_color = color_orange_theme
        else:
            settings.change_api_status("api-off")
            self.api_button.icon_color = color_background_input

    def update(self, instance: ButtonC) -> None:
        response: bool = Update().update(self.scrollapp.coins_tab)
        update_info = Popup(
            title_color=color_orange_theme,
            overlay_color=color_behind_info,
            separator_color=color_behind_info,
            size_hint=(None, None),
            size=(260, 60),
            auto_dismiss=True,
            title="",
            background_color=color_success_info,
            title_font=font_config,
        )
        update_info.pos_hint = {
            "center_x": 0.5,
            "center_y": 0.1,
        }
        if response:
            update_info.title = language.get_text(Text.DATA_SAVING_SUCCESSFUL.value)
            update_success = Label(
                text="",
                font_name=font_config,
                color=color_orange_theme,
            )
            update_info.content = update_success
            update_info.open(animation=True)
            Clock.schedule_once(update_info.dismiss, 2.5)
        else:
            update_info.background_color = color_error_info
            update_info.title = language.get_text(Text.DATA_SAVING_FAILED.value)
            update_fail = Label(
                text="",
                font_name=font_config,
                color=color_orange_theme,
            )
            update_info.content = update_fail
            update_info.open(animation=True)
            Clock.schedule_once(update_info.dismiss, 2.5)

    def change_loc(self, instance: ButtonC) -> None:
        change_xlsx_menu = Popup(
            title_color=color_orange_theme,
            overlay_color=color_behind_window,
            separator_color=color_orange_theme,
            size_hint=(None, None),
            size=(500, 150),
            auto_dismiss=True,
            title=language.get_text(Text.CHANGE_XLSX_WORKBOOK.value),
            background_color=color_window,
            title_font=font_config,
        )
        add_menu = ChangeXlsxMenu(self.scrollapp, change_xlsx_menu)
        change_xlsx_menu.content = add_menu
        change_xlsx_menu.open(animation=True)

    def change_language(self, instance: ButtonC) -> None:
        self.language_list_buttons.dismiss()
        settings.change_language(Languages(instance.text))
        self.scrollapp.empty_list.text = language.get_text(Text.EMPTY_LIST_TEXT.value)
        self.refresh_button.tooltip_text = language.get_text(Text.REFRESH_DATA.value)
        self.open_xlsx.tooltip_text = language.get_text(Text.OPEN_XLSX.value)
        self.api_button.tooltip_text = language.get_text(Text.CHANGE_API.value)
        self.change_loc_button.tooltip_text = language.get_text(
            Text.CHANGE_XLSX_WORKBOOK.value
        )
        self.update_button.tooltip_text = language.get_text(Text.UPDATE.value)
        self.language_button.tooltip_text = language.get_text(
            Text.CHANGE_LANGUAGE.value
        )

    def open_xlsx_file(self, instance: ButtonC) -> None:
        source = settings.get_xlsx_file_path()
        try:
            workbook = load_workbook(source)
            if workbook is not None:
                subprocess.run(["start", source], shell=True, check=False)
                sys.exit()
        except (InvalidFileException, FileNotFoundError):
            print("we need xlsx file!")
