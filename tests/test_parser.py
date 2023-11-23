import os
from typing import Any

import pytest
import requests
from dotenv import load_dotenv

from src.parser import get_currency

load_dotenv()

API_KEY = os.getenv("EXCHANGE_API_KEY")
assert API_KEY is not None


def get_currency_from_site(currency: str) -> Any:
    if API_KEY is None:
        return "Ошибка. Пустой API"
    url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency}"
    response = requests.get(url, headers={"apikey": API_KEY})
    return response.json()


@pytest.fixture
def currency() -> list[str]:
    return ["USD", "EUR", "RUB", "CNY", "IDR"]


def test_get_currency_from_site(currency: str) -> None:
    assert get_currency_from_site(currency[0])["base"] == "USD"
    assert get_currency_from_site(currency[0])["success"] is True

    assert get_currency_from_site(currency[1])["base"] == "EUR"
    assert get_currency_from_site(currency[1])["success"] is True

    assert get_currency_from_site(currency[3])["base"] == "CNY"
    assert get_currency_from_site(currency[3])["success"] is True

    assert get_currency_from_site(currency[4])["base"] == "IDR"
    assert get_currency_from_site(currency[4])["success"] is True


def test_get_currency(currency: list[str]) -> None:
    assert get_currency("RUB") == "Неправильно введённая валюта. Выберите другую валюту"
