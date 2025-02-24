import os
import ctypes
import subprocess
from Xlib import display
import platform
from typing import Any
import importlib.resources

try:
    import tkinter  # type: ignore
except ImportError:
    print("Tkinter is not installed. Make sure you have it installed. ")
    if platform.system() == "Linux":
        prompt_decision = input("Do you want to try install now? y/n")
        if prompt_decision == "y":
            try:
                subprocess.run(["sudo apt-get update"])
                subprocess.run(["sudo apt-get install python3-tk"])
            except Exception as e:
                print(f"Tkinter installation failed: {e}")
    else:
        raise ImportError(
            "Tkinter is not installed. Make sure you have it installed. "
            "On Windows should be preinstalled with python"
            "On Linux, you may need to install the 'python3-tk' package."
            "'sudo apt-get install python3-tk'"
        )
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout

from price_updater.widgets.scroll_app import ScrollApp
from price_updater.widgets.top_bar import TopBar
from price_updater.widgets.menu import Menu


title: str = "Price Updater©"


if platform.system() == "Windows":
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
elif platform.system() == "Linux":
    os.system("clear")


class MainApp(MDApp):
    def __init__(self, *args: Any) -> None:
        super(MainApp, self).__init__(*args)
        self.window = BoxLayout(orientation="vertical")
        self.menu = RelativeLayout(size_hint=(1, 0.9))
        self.scroll_and_menu = BoxLayout(orientation="horizontal")
        self.top_bar_and_menu = BoxLayout(orientation="vertical")
        self.left_side = FloatLayout(size_hint=(1, 1))
        self.background = Image(source=self.get_bg_image(), fit_mode="fill")
        self.scrollview = ScrollApp()
        self.right_side = Menu(self.scrollview, size_hint=(0.3, 1))
        self.top_bar = TopBar(
            size_hint=(1, None), scrollapp=self.scrollview, right_side=self.right_side
        )

    def get_bg_image(self) -> str:
        with importlib.resources.path(
            "price_updater.images", "background_sode.jpg"
        ) as bg_path:
            return str(bg_path)

    def on_start(self, *args: Any) -> None:
        height: int = 500
        width: int = 850
        Window.minimum_width, Window.minimum_height = width, height
        Window.set_title(title)
        Window.size = (width, height)
        if platform.system() == "Windows":
            user32 = ctypes.windll.user32
            screen_width = user32.GetSystemMetrics(0)
            screen_height = user32.GetSystemMetrics(1)
        elif platform.system() == "Linux":
            disp = display.Display()
            screen = disp.screen()
            screen_height = screen.height_in_pixels
            screen_width = screen.width_in_pixels
        Window.size = (width, height)
        Window.top = screen_height - height * 2
        Window.left = screen_width - width * 2
        Window.borderless = False

    def build(self) -> BoxLayout:
        self.window.add_widget(self.menu)

        self.menu.add_widget(self.background)
        self.menu.add_widget(self.top_bar_and_menu)

        self.top_bar_and_menu.add_widget(self.top_bar)
        self.top_bar_and_menu.add_widget(self.scroll_and_menu)

        self.scroll_and_menu.add_widget(self.left_side)

        self.left_side.add_widget(self.scrollview)
        self.left_side.add_widget(self.right_side)
        return self.window


main_app = MainApp()
if __name__ == "__main__":
    main_app.run()
