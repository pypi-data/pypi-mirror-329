from importlib.resources import files
from kivy.utils import get_color_from_hex
from kivy.core.text import LabelBase


VERSION: str = "Price Updater© 3.2.1"

with files("price_updater").joinpath("Gabarito-SemiBold.ttf").open("rb") as font_path:
    LabelBase.register(name="standard", fn_regular=font_path.name)

font_config: str = "standard"

color_error: list[float] = get_color_from_hex("#FF0000")
color_button: list[float] = get_color_from_hex("#444444FF")
color_background_input: list[float] = get_color_from_hex("#5AC4FF0F")
color_top_bar: list[float] = get_color_from_hex("#403C3CFF")
color_top_bar_button: list[float] = get_color_from_hex("#403C3C00")
color_orange_theme: list[float] = get_color_from_hex("#E06600")
color_window: list[float] = get_color_from_hex("#FFFDF5FF")
color_behind_window: list[float] = get_color_from_hex("#000000CC")
color_behind_info: list[float] = get_color_from_hex("#00000000")
color_success_info: list[float] = get_color_from_hex("#00FF00DD")
color_error_info: list[float] = get_color_from_hex("#FF0000DD")
color_checkbox: list[float] = [80, 80, 80, 1]
color_asset_button: list[float] = get_color_from_hex("#EBE6D5CC")
