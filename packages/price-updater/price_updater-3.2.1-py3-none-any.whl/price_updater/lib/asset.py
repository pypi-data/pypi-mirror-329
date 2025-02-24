from typing import Dict

from price_updater.lib.currency import Currency


class Asset:
    def __init__(
        self,
        *,
        asset_id: int,
        name: str,
        worksheet: str,
        cell: str,
        price: Dict[Currency, str],
        currency: Currency,
    ) -> None:
        self.asset_id: int = asset_id
        self.name: str = name
        self.worksheet: str = worksheet
        self.cell: str = cell
        self.chosen_currency: Currency = currency
        self.price_usd: str = price[Currency.USD]
        self.price_pln: str = price[Currency.PLN]
        self.price_eur: str = price[Currency.EUR]
        self.price_gbp: str = price[Currency.GBP]
        self.asset_logo: str = price[Currency.LOGO]
