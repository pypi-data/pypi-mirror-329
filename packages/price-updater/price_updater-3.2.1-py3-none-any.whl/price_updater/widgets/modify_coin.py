from dataclasses import dataclass
import re
from typing import Dict, Any
from kivymd.uix.button import MDRaisedButton
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

from price_updater.coins_list import assets_list
from price_updater.lib.on_check_box_active import OnCheckBoxActive
from price_updater.lib.asset import Asset
from price_updater.lib.update import Update
from price_updater.lib.text_input import TextInputC
from price_updater.lib.button import ButtonC
from price_updater.lib.language import language, Text
from price_updater.lib.settings import settings
from price_updater.lib.currency import Currency
from price_updater.lib.auto_suggestion_text import AutoSuggestionText
from price_updater.lib.config import (
    color_checkbox,
    color_orange_theme,
    color_button,
    color_error,
    font_config,
)


@dataclass
class Info:
    check: bool
    price: Dict[Currency, str]


class ModifyCoin(BoxLayout, OnCheckBoxActive):
    def __init__(self, scrollapp: Any, popup: Popup, coin: Asset) -> None:
        super().__init__()
        self.scrollapp: Any = scrollapp
        self.popup: Popup = popup
        self.coin: Asset = coin
        AutoSuggestionText.modified_coin = self.coin.name
        self.orientation = "vertical"
        self.opacity: float = 0.8
        self.spacing: int = 5
        self.workbook = Update().try_load_workbook()
        self.coin_name_input = AutoSuggestionText(
            text=self.coin.name, suggestions=assets_list
        )
        self.coin_name_input.select_all()
        self.coin_name_input.focus = True
        self.worksheet_input: str = ""
        self.cell_input = TextInputC(text=self.coin.cell)
        chosen_currency: Currency = self.get_chosen_currency()
        self.checkboxes_currency = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.15)
        )
        self.checkbox_currency_labels = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.07)
        )
        self.checkbox_usd = CheckBox(
            active=chosen_currency == Currency.USD,
            color=color_checkbox,
        )
        self.checkbox_usd.bind(active=self.on_checkbox_active)
        self.checkbox_eur = CheckBox(
            active=chosen_currency == Currency.EUR,
            color=color_checkbox,
        )
        self.checkbox_eur.bind(active=self.on_checkbox_active)
        self.checkbox_gbp = CheckBox(
            active=chosen_currency == Currency.GBP,
            color=color_checkbox,
        )
        self.checkbox_gbp.bind(active=self.on_checkbox_active)
        self.checkbox_pln = CheckBox(
            active=chosen_currency == Currency.PLN,
            color=color_checkbox,
        )
        self.checkbox_pln.bind(active=self.on_checkbox_active)
        self.label_usd = Label(
            text="USD", color=color_orange_theme, font_name=font_config
        )
        self.label_eur = Label(
            text="EUR", color=color_orange_theme, font_name=font_config
        )
        self.label_gbp = Label(
            text="GBP", color=color_orange_theme, font_name=font_config
        )
        self.label_pln = Label(
            text="PLN", color=color_orange_theme, font_name=font_config
        )
        self.checkbox_currency_labels.add_widget(self.label_usd)
        self.checkbox_currency_labels.add_widget(self.label_eur)
        self.checkbox_currency_labels.add_widget(self.label_gbp)
        self.checkbox_currency_labels.add_widget(self.label_pln)
        self.checkboxes_currency.add_widget(self.checkbox_usd)
        self.checkboxes_currency.add_widget(self.checkbox_eur)
        self.checkboxes_currency.add_widget(self.checkbox_gbp)
        self.checkboxes_currency.add_widget(self.checkbox_pln)

        self.scroll_sheets = ScrollView()
        self.sheets_widget = BoxLayout(
            orientation="vertical", size_hint_y=None, spacing=2
        )
        self.sheets_widget.bind(minimum_height=self.sheets_widget.setter("height"))
        self.scroll_sheets.add_widget(self.sheets_widget)
        if self.workbook is not None:
            self.sheets: list[str] = self.workbook.sheetnames
        self.sheets.remove("data")
        for sheet in self.sheets:
            sheet_button = MDRaisedButton(
                text=sheet,
                md_bg_color=color_button,
                size_hint=(1, None),
                height=35,
                on_release=self.chosen_sheet,
                font_name=font_config,
                font_size=17,
                text_color=color_orange_theme,
            )
            if self.coin.worksheet == sheet:
                self.worksheet_input = sheet
                sheet_button.md_bg_color = color_orange_theme
                sheet_button.text_color = color_button
            self.sheets_widget.add_widget(sheet_button)
        self.add_widget(self.coin_name_input)
        self.add_widget(self.scroll_sheets)
        self.add_widget(self.cell_input)

        self.add_widget(self.checkboxes_currency)
        self.add_widget(self.checkbox_currency_labels)

        buttons = BoxLayout(orientation="horizontal", size_hint=(1, 0.4))
        self.add_widget(buttons)
        self.button_modify = ButtonC(
            text=language.get_text(Text.MODIFY.value),
            on_release=self.modify,
            size_hint=(0.5, 0.8),
        )
        buttons.add_widget(self.button_modify)
        self.button_delete = ButtonC(
            text=language.get_text(Text.DELETE.value),
            on_release=self.delete,
            size_hint=(0.5, 0.8),
        )
        self.button_delete.text_color = color_error
        buttons.add_widget(BoxLayout(size_hint=(0.01, 1)))
        buttons.add_widget(self.button_delete)

    def get_chosen_currency(self) -> Currency:
        return Currency(self.coin.chosen_currency)

    def chosen_sheet(self, instance: MDRaisedButton) -> None:
        if instance.md_bg_color == color_orange_theme:
            self.worksheet_input = instance.text
            for sheet in self.sheets_widget.children:
                if instance is not sheet:
                    sheet.md_bg_color = color_button
                    sheet.text_color = color_orange_theme
        else:
            for sheet in self.sheets_widget.children:
                sheet.md_bg_color = color_button
                sheet.text_color = color_orange_theme
            self.worksheet_input = instance.text
            instance.md_bg_color = color_orange_theme
            instance.text_color = color_button

    def modify(self, instance: ButtonC) -> None:
        if self.workbook is not None:
            data = self.workbook["data"]
        info = self.check_input_data()
        if info.check:
            chosen_currency: Currency
            if self.checkbox_usd.active:
                chosen_currency = Currency.USD
            elif self.checkbox_eur.active:
                chosen_currency = Currency.EUR
            elif self.checkbox_gbp.active:
                chosen_currency = Currency.GBP
            else:
                chosen_currency = Currency.PLN
            self.coin.chosen_currency = chosen_currency

            data = self.workbook["data"]
            data.cell(row=1, column=self.coin.asset_id).value = (
                self.coin_name_input.text.lower()
                if self.coin_name_input.text != ""
                else self.coin.name.lower()
            )
            data.cell(row=2, column=self.coin.asset_id).value = self.worksheet_input
            data.cell(
                row=3, column=self.coin.asset_id
            ).value = self.cell_input.text.upper()
            data.cell(row=4, column=self.coin.asset_id).value = chosen_currency.name
            self.workbook.save(settings.get_xlsx_file_path())
            for coin in self.scrollapp.coins_tab:
                if coin.asset_id == self.coin.asset_id:
                    coin.name = (
                        self.coin_name_input.text.lower()
                        if self.coin_name_input.text != ""
                        else self.coin.name
                    )
                    coin.worksheet = self.worksheet_input
                    coin.cell = self.cell_input.text.upper()
                    coin.price_usd = info.price[Currency.USD]
                    coin.price_pln = info.price[Currency.PLN]
                    coin.price_gbp = info.price[Currency.GBP]
                    coin.price_eur = info.price[Currency.EUR]
                    coin.asset_logo = info.price[Currency.LOGO]
                    break
            self.scrollapp.initialize_coins(False)
            self.popup.dismiss()

    def delete(self, instance: ButtonC) -> None:
        if self.workbook is not None:
            data = self.workbook["data"]
            data.cell(row=1, column=self.coin.asset_id).value = "-"
            data.cell(row=2, column=self.coin.asset_id).value = ""
            data.cell(row=3, column=self.coin.asset_id).value = ""
            self.workbook.save(settings.get_xlsx_file_path())
        for coin in self.scrollapp.coins_tab:
            if coin.asset_id == self.coin.asset_id:
                self.scrollapp.coins_tab.remove(coin)
                break
        self.scrollapp.initialize_coins(False)
        self.scrollapp.coins.height = (
            self.scrollapp.spacing
            + self.scrollapp.coin_height * len(self.scrollapp.coins_tab)
        )
        self.popup.dismiss()

    def check_input_data(self) -> Info:
        if not self.coin_name_input.text in (self.coin.name, ""):
            test_price: Dict[Currency, str] = Update().get_asset_price(
                self.coin_name_input.text
            )
        else:
            test_price = {
                Currency.USD: self.coin.price_usd,
                Currency.PLN: self.coin.price_pln,
                Currency.GBP: self.coin.price_gbp,
                Currency.EUR: self.coin.price_eur,
                Currency.LOGO: self.coin.asset_logo,
            }

        name_ok: bool = False
        sheet_ok: bool = False
        cell_ok: bool = False
        currency_ok: bool = False
        ##############################################
        print(test_price)
        if test_price not in (
            None,
            {
                Currency.USD: "0,0",
                Currency.PLN: "0,0",
                Currency.GBP: "0,0",
                Currency.EUR: "0,0",
                Currency.LOGO: "",
            },
        ):
            self.coin_name_input.text_ok()
            name_ok = True
        else:
            self.coin_name_input.text_error()
        ##############################################
        if self.workbook is not None:
            if "data" not in self.workbook.sheetnames:
                self.workbook.create_sheet("data")
                hidden = self.workbook["data"]
                hidden.sheet_state = "hidden"
                self.workbook.save(settings.get_xlsx_file_path())
        if self.worksheet_input != "":
            sheet_ok = True
        else:
            for sheet in self.sheets_widget.children:
                sheet.color = color_error
        ##############################################
        cell_pattern = r"^[A-Za-z]\d+$"
        if re.match(cell_pattern, self.cell_input.text):
            self.cell_input.text_ok()
            cell_ok = True
        else:
            self.cell_input.text_error()
        ##############################################
        if (
            self.checkbox_usd.active
            or self.checkbox_eur.active
            or self.checkbox_gbp.active
            or self.checkbox_pln.active
        ):
            currency_ok = True
        ##############################################
        return Info(check=name_ok & sheet_ok & cell_ok & currency_ok, price=test_price)
