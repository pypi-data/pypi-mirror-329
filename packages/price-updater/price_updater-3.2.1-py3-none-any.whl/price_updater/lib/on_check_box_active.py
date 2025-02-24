from kivy.uix.checkbox import CheckBox

from price_updater.lib.config import color_orange_theme, color_error


class OnCheckBoxActive:
    def on_checkbox_active(self: CheckBox, instance: CheckBox, value: bool) -> None:
        if instance == self.checkbox_usd:
            if value:
                self.checkbox_eur.active = False
                self.checkbox_gbp.active = False
                self.checkbox_pln.active = False
        if instance == self.checkbox_eur:
            if value:
                self.checkbox_usd.active = False
                self.checkbox_gbp.active = False
                self.checkbox_pln.active = False
        if instance == self.checkbox_gbp:
            if value:
                self.checkbox_usd.active = False
                self.checkbox_eur.active = False
                self.checkbox_pln.active = False
        if instance == self.checkbox_pln:
            if value:
                self.checkbox_usd.active = False
                self.checkbox_gbp.active = False
                self.checkbox_eur.active = False
        if (
            self.checkbox_usd.active
            or self.checkbox_gbp.active
            or self.checkbox_eur.active
            or self.checkbox_pln.active
        ):
            self.label_usd.color = color_orange_theme
            self.label_eur.color = color_orange_theme
            self.label_gbp.color = color_orange_theme
            self.label_pln.color = color_orange_theme
        else:
            self.label_usd.color = color_error
            self.label_eur.color = color_error
            self.label_gbp.color = color_error
            self.label_pln.color = color_error
