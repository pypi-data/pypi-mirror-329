import os
import subprocess
import sys
import platform
from typing import Any
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from price_updater.lib.language import language, Text
from price_updater.lib.button import ButtonC
from price_updater.lib.config import font_config, color_success_info


class VersionAvailableMenu(BoxLayout):
    def __init__(
        self, scrollApp: Any, popup: Popup, latest_version: str, **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.scrollapp = scrollApp
        self.popup: Popup = popup
        self.orientation: str = "vertical"
        self.opacity: float = 0.8
        self.warning_content = Label(
            text=latest_version,
            font_name=font_config,
            font_size=19,
            color=color_success_info,
        )
        self.add_widget(self.warning_content)
        self.button = BoxLayout(orientation="horizontal")
        self.add_widget(self.button)
        self.install_button = ButtonC(
            text=language.get_text(Text.INSTALL.value),
            on_release=self.install,
            size_hint=(0.15, 0.75),
        )
        self.button.add_widget(self.install_button)

    def install(self, instance: ButtonC) -> None:
        if platform.system() == "Windows":
            script_name = "install_update.bat"
        elif platform.system() == "Linux":
            script_name = "install_update.sh"
        script_path = os.path.join(os.path.dirname(__file__), script_name)
        subprocess.Popen([script_path])
        sys.exit(0)
