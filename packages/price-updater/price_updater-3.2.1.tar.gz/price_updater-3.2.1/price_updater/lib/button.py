from typing import Any
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.button import MDIconButton
from kivymd.uix.tooltip import MDTooltip
from kivymd.font_definitions import theme_font_styles

from price_updater.lib.config import color_button, color_orange_theme


class ButtonC(MDRaisedButton):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.font_style = theme_font_styles[5]
        self.font_size: int = 17
        self.md_bg_color: list[float] = color_button
        self.text_color: list[float] = color_orange_theme


class TooltipMDIconButton(MDIconButton, MDTooltip):
    pass
