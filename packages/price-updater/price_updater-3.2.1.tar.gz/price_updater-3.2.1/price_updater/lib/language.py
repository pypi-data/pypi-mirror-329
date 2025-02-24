from typing import Any
from importlib.resources import files
from enum import Enum
import json

from price_updater.lib.settings import Settings, settings


class Text(Enum):
    UPDATE = "update"
    EDIT_COIN = "edit_asset"
    MODIFY = "modify"
    DELETE = "delete"
    COIN_NAME = "asset"
    WORKSHEET_NAME = "worksheet_name"
    CELL = "cell"
    ADD = "add"
    ADD_NEW_COIN = "add_new_asset"
    CHANGE_XLSX_WORKBOOK = "change_xlsx_workbook"
    PATH_TO_XLSX = "path_to_xlsx"
    SEARCH = "search"
    EMPTY_LIST_TEXT = "your_assets_will_be_here"
    LOADING_LIST_TEXT = "please_wait"
    PLEASE_SELECT_WORKBOOK = "please_select_workbook"
    FETCH_ERROR_TITLE = "fetch_error_title"
    OUTDATED_VERSION = "outdated_version"
    INSTALL = "install"
    FETCH_ERROR_MSG = "fetch_error_msg"
    CONNECTION_LOST = "connection_lost"
    DATA_SAVING_SUCCESSFUL = "data_saving_successful"
    DATA_SAVING_FAILED = "data_saving_failed"
    REFRESH_DATA = "refresh_data"
    CHANGE_LANGUAGE = "change_language"
    CHANGE_API = "change_api"
    OPEN_XLSX = "open_xlsx"


class Language:
    def __init__(self, stngs: Settings) -> None:
        self.language_file: Any = self.read_file()
        self.settings = stngs

    def get_text(self, word: str) -> str:
        return self.language_file[self.settings.get_current_language()][word]

    def read_file(self) -> Any:
        with files("price_updater").joinpath("data_translations.json").open(
            "rb"
        ) as lang_data:
            data = json.load(lang_data)
            return data


language = Language(settings)
