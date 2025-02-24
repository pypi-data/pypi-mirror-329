from typing import Tuple, Any
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.clock import Clock

from price_updater.lib.language import language, Text
from price_updater.lib.config import (
    color_background_input,
    color_orange_theme,
    color_error,
    color_button,
    font_config,
)


class AutoSuggestionText(TextInput):
    modified_coin: str = ""

    def __init__(self, suggestions: Tuple[str, ...], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.suggestion_coins: Tuple[str, ...] = suggestions
        self.text_chosen: str = ""
        self.dropdown: DropDown = None
        self.multiline: bool = False
        self.size_hint: tuple = (1, 0.2)
        self.background_color: list[float] = color_background_input
        self.foreground_color: list[float] = color_orange_theme
        self.focus: bool = True
        self.cursor_color: list[float] = color_orange_theme
        self.font_name: str = "standard"
        self.font_size: int = 16
        self.select_all()
        self.focus = True

    def text_ok(self) -> None:
        self.foreground_color = color_orange_theme

    def text_error(self) -> None:
        self.foreground_color = color_error

    @staticmethod
    def on_text(inst: TextInput, value: str) -> None:
        if (
            value != language.get_text(Text.COIN_NAME.value)
            and value != AutoSuggestionText.modified_coin
        ):
            if inst.dropdown:
                inst.dropdown.dismiss()
            inst.dropdown = DropDown()

            def push(textinput: Button) -> None:
                inst.dropdown.dismiss()
                inst.text_chosen = textinput.text
                inst.push_text(textinput)

            if inst.text_chosen != value and inst.text != "":
                Clock.unschedule(inst.dropdown.open)
                for suggestion in inst.suggestion_coins:
                    if suggestion.startswith(value.lower()):
                        button = Button(
                            text=suggestion,
                            size_hint_y=None,
                            height=32,
                            on_release=push,
                            background_color=color_button,
                            font_name=font_config,
                            font_size=14,
                            color=color_orange_theme,
                        )
                        inst.dropdown.add_widget(button)
                if inst.dropdown.children:
                    inst.dropdown.open(inst)

    def push_text(self, textinput: TextInput) -> None:
        self.text = textinput.text
        self.dropdown = None
