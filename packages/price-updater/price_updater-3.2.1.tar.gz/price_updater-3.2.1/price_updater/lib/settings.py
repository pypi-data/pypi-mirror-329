import os
from pathlib import Path
from typing import Any
from enum import Enum
import json


class Languages(Enum):
    EN = "EN"
    PL = "PL"
    DE = "DE"


class Settings:
    def __init__(self) -> None:
        self.data_file_path = self.get_data_path()
        self.settings_file: Any = self._read_file()

    def get_data_path(self) -> str:
        home_directory = os.path.expanduser("~")
        folder_path = os.path.join(home_directory, "price_updater_settings")
        file_path = os.path.join(folder_path, "data.json")
        os.makedirs(folder_path, exist_ok=True)
        return file_path

    def _read_file(self) -> Any:
        if not Path(self.data_file_path).exists():
            self._initialize_data_file()
        with open(self.data_file_path, encoding="utf-8") as file:
            data = json.load(file)
        return data

    def _initialize_data_file(self) -> None:
        data = {"path_to_xlsx": "", "chosen_language": "EN", "api": "api-off"}
        with open(self.data_file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    def get_xlsx_file_path(self) -> str:
        return self.settings_file["path_to_xlsx"]

    def change_xlsx_file_path(self, path: str) -> None:
        with open(self.data_file_path, mode="r+", encoding="utf-8") as file:
            data: Any = json.load(file)
            data["path_to_xlsx"] = path
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
        self.settings_file = self._read_file()

    def get_api_status(self) -> str:
        return self.settings_file["api"]

    def change_api_status(self, status: str) -> None:
        with open(self.data_file_path, mode="r+", encoding="utf-8") as file:
            data: Any = json.load(file)
            data["api"] = status
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
        self.settings_file = self._read_file()

    def get_current_language(self) -> str:
        return self.settings_file["chosen_language"]

    def change_language(self, new_language: Languages) -> None:
        with open(self.data_file_path, mode="r+", encoding="utf-8") as file:
            data: Any = json.load(file)
            data["chosen_language"] = new_language.value
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
        self.settings_file = self._read_file()


settings = Settings()
