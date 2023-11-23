import json
import logging
import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_API_KEY")

logger = logging.getLogger(__name__)


def get_currency(currency: str) -> Any:
    """
    Функция получает информацию о курсе введённой валюты к рублю с помощью API. Если введённая валюта рубль,
    то функция возвращает текст 'Неправильно введённая валюта. Выберите другую валюту'
    """
    if currency == "RUB":
        logger.error("get_currency error: Неправильно введённая валюта")
        return "Неправильно введённая валюта. Выберите другую валюту"
    if API_KEY is None:
        logger.error("get_currency error: Пустой API")
        return "Ошибка. Пустой API"
    url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency}"
    response = requests.get(url, headers={"apikey": API_KEY})
    response_data = json.loads(response.content)
    got_currency = response_data["rates"]["RUB"]
    return round(got_currency, 2)


logger.info("parser.py is working. Status: ok")
