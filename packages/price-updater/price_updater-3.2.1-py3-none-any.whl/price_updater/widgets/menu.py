from typing import Any
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from price_updater.widgets.add_menu import AddMenu
from price_updater.widgets.scroll_app import ScrollApp
from price_updater.lib.button import TooltipMDIconButton
from price_updater.lib.language import language, Text
from price_updater.lib.button import ButtonC
from price_updater.lib.config import VERSION
from price_updater.lib.config import (
    color_top_bar_button,
    color_orange_theme,
    color_behind_window,
    color_window,
    font_config,
)


class Menu(MDRelativeLayout):
    def __init__(self, scrollapp: ScrollApp, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.scrollapp: ScrollApp = scrollapp
        self.button_add = TooltipMDIconButton(
            tooltip_text=language.get_text(Text.ADD_NEW_COIN.value),
            icon="pen-plus",
            on_release=self.add_new_coin,
            md_bg_color=color_top_bar_button,
            theme_icon_color="Custom",
            icon_color=color_orange_theme,
            icon_size="40sp",
        )
        self.button_add.pos_hint = {
            "center_x": 3.12,
            "center_y": 0.11,
        }
        self.info = Label(
            text=VERSION, font_name="standard", font_size=13, color=color_orange_theme
        )
        self.info.pos_hint = {"center_x": 0.24, "center_y": 0.023}
        self.add_widget(self.button_add)
        self.add_widget(self.info)

    def add_new_coin(self, instance: ButtonC) -> None:
        add_coin_menu = Popup(
            title_color=color_orange_theme,
            overlay_color=color_behind_window,
            separator_color=color_orange_theme,
            size_hint=(None, None),
            size=(400, 400),
            auto_dismiss=True,
            title=language.get_text(Text.ADD_NEW_COIN.value),
            background_color=color_window,
            title_font=font_config,
        )
        add_menu = AddMenu(self.scrollapp, add_coin_menu)
        add_coin_menu.content = add_menu
        add_coin_menu.open(animation=True)
