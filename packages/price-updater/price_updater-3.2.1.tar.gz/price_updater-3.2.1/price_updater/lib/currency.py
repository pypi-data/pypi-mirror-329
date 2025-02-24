from enum import Enum
from bs4 import BeautifulSoup
from requests import get, Response
from requests import exceptions


class Currency(Enum):
    LOGO = "_LOGO"
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    PLN = "PLN"


class CCurrency:
    def __init__(self) -> None:
        self.connection_lost: bool = False
        self.usd_pln: float = 0.0
        self.eur_pln: float = 0.0
        self.gbp_pln: float = 0.0

    def get_currency(self, currencyy: Currency) -> float:
        try:
            url: str = (
                f"https://www.biznesradar.pl/notowania/{currencyy.value}PLN#1d_lin_lin"
            )
            page: Response = get(url, timeout=5)
            page_content = BeautifulSoup(page.content, "html.parser")

            for nastronie in page_content.find_all("span", class_="profile_quotation"):
                price: str = nastronie.find("span", class_="q_ch_act")
                price = str(price)
                price = price.replace('<span class="q_ch_act">', "")
                price = price.replace("</span>", "")
                price = price[0:6]
                return float(price)
        except (
            ValueError,
            ZeroDivisionError,
            TypeError,
            exceptions.ConnectionError,
            exceptions.ReadTimeout,
        ) as error:
            if isinstance(error, (exceptions.ConnectionError, exceptions.ReadTimeout)):
                self.connection_lost = True
            return 0.0
        return 0.0

    def return_price(self, currencyy: Currency) -> float:
        match currencyy:
            case Currency.PLN:
                return 1.0
            case Currency.USD:
                return self.usd_pln
            case Currency.GBP:
                return self.gbp_pln
            case Currency.EUR:
                return self.eur_pln
        return 0.0


currency = CCurrency()
