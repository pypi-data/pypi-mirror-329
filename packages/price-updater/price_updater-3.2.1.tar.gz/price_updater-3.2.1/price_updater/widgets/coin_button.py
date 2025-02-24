from typing import Any
from kivymd.uix.button import MDRaisedButton
from kivymd.font_definitions import theme_font_styles
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.popup import Popup
from kivy.uix.image import AsyncImage
from kivy.uix.behaviors import ButtonBehavior

from price_updater.widgets.modify_coin import ModifyCoin
from price_updater.lib.asset import Asset
from price_updater.lib.language import language, Text
from price_updater.lib.currency import Currency
from price_updater.lib.config import (
    color_button,
    color_orange_theme,
    color_behind_window,
    color_window,
    font_config,
)


class CoinButton(MDRaisedButton):
    def __init__(self, scrollapp: Any, coin: Asset) -> None:
        super().__init__()
        self.spacing: int = 2
        self.coin_height: int = 40
        self.currency_logo: str = ""
        self.coin_price: str = ""
        match coin.chosen_currency:
            case Currency.USD:
                self.currency_logo = "$"
                self.coin_price = coin.price_usd
            case Currency.PLN:
                self.currency_logo = "zł"
                self.coin_price = coin.price_pln
            case Currency.GBP:
                self.currency_logo = "£"
                self.coin_price = coin.price_gbp
            case Currency.EUR:
                self.currency_logo = "€"
                self.coin_price = coin.price_eur
        self.size_hint: tuple[int, int] = (1, self.coin_height)
        self.coin: Asset = coin
        self.asset_round_logo: str | None = self.coin.asset_logo
        self.scrollapp: Any = scrollapp
        self.font_size: int = 18
        self.text_size: tuple[None, None] = (None, None)
        self.worksheet: str = self.coin.worksheet
        self.halign: str = "left"
        self.cell: str = self.coin.cell
        self.font_name: str = font_config
        self.height: int = self.coin_height
        self.md_bg_color: list[float] = color_button

        self.coin_frame = MDBoxLayout(orientation="horizontal")
        self.logo_async = AsyncImage(source=self.asset_round_logo, fit_mode="fill")
        self.logo: MDLabel | ImageButton = (
            MDLabel(size_hint=(0.06, 1))
            if self.asset_round_logo == ""
            else ImageButton(source=self.asset_round_logo, size_hint=(0.06, 1))
        )
        self.name_label = MDLabel(
            size_hint=(1, 1),
            text=f"  {self.coin.name}",
            halign="left",
            theme_text_color="Secondary" if self.coin_price != "0,0" else "Error",
            font_style=theme_font_styles[5],
        )
        self.price_label = MDLabel(
            text=f"{self.currency_logo} {self.coin_price}",
            halign="right",
            theme_text_color="Secondary" if self.coin_price != "0,0" else "Error",
            font_style=theme_font_styles[5],
        )
        self.coin_frame.add_widget(self.logo)
        self.coin_frame.add_widget(self.name_label)
        self.coin_frame.add_widget(self.price_label)
        self.add_widget(self.coin_frame)

    def on_press(self) -> None:
        modify_coin_menu = Popup(
            title_color=color_orange_theme,
            overlay_color=color_behind_window,
            separator_color=color_orange_theme,
            size_hint=(None, None),
            size=(400, 400),
            auto_dismiss=True,
            title=f"{language.get_text(Text.EDIT_COIN.value)} {self.coin.name}",
            background_color=color_window,
            title_font=font_config,
        )
        add_menu = ModifyCoin(
            scrollapp=self.scrollapp, popup=modify_coin_menu, coin=self.coin
        )
        modify_coin_menu.content = add_menu
        modify_coin_menu.open(animation=True)


class ImageButton(ButtonBehavior, AsyncImage):
    pass
