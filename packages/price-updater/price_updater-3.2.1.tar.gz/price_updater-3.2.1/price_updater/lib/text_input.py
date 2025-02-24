from typing import Any
from kivy.uix.textinput import TextInput

from price_updater.lib.config import (
    color_background_input,
    color_orange_theme,
    color_error,
)


class TextInputC(TextInput):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.size_hint: tuple = (1, 0.2)
        self.multiline: bool = False
        self.background_color: list[float] = color_background_input
        self.foreground_color: list[float] = color_orange_theme
        self.cursor_color: list[float] = color_orange_theme
        self.font_name: str = "standard"
        self.font_size: int = 16

    def text_ok(self) -> None:
        self.foreground_color = color_orange_theme

    def text_error(self) -> None:
        self.foreground_color = color_error
