import json
import logging
from typing import Any, Optional

from src.masks import mask_card_with_name

logger = logging.getLogger(__name__)


def reformat_date(date_: str) -> str:
    """
    Функцию, которая принимает на вход строку, вида "2018-07-11T02:26:18.671407"
    и возвращает строку с датой в виде "11.07.2018"
    """
    if date_ == "":
        return "Некорректно введена дата"
    if 0 < int(date_[8:10]) <= 31 and 0 < int(date_[5:7]) <= 12:
        return date_[8:10] + "." + date_[5:7] + "." + date_[0:4]
    else:
        return "Некорректно введена дата"


def get_info_about_transaction(identifier: int, filepath: str = "../data/transactions.json") -> Any:
    """
    Функция возвращает данные от транзакции в виде словаря по её индитифиактору
    :rtype: object
    """
    with open(filepath) as file:
        transactions = json.load(file)
        for transaction in transactions:
            if identifier == transaction["id"]:
                transaction["date"] = reformat_date(transaction["date"])
                if transaction["from"] is not None:
                    transaction["from"] = mask_card_with_name(transaction["from"])
                else:
                    transaction["from"] = "Информация не найдена"
                transaction["to"] = mask_card_with_name(transaction["to"])
                reformat_transaction_date = {
                    "Индитификатор": transaction["id"],
                    "Статус": transaction["state"],
                    "Дата": transaction["date"],
                    "Сумма": transaction["amount"],
                    "Тикер валюты": transaction["currency_code"],
                    "Откуда": transaction["from"],
                    "Куда": transaction["to"],
                    "Описание": transaction["description"],
                }
                return reformat_transaction_date
        return "Неверно введён индитификатор транзакции"


def get_kind_of_transaction(
    value: Optional[str] = "EXECUTED", filepath: str = "../data/transactions.json"
) -> list[dict]:
    """
    Функция принимает на вход список словарей и значение для ключа state и возвращает новый список,
    содержащий только те словари, у которых ключ state содержит переданное в функцию значение
    """
    with open(filepath) as file:
        transactions = json.load(file)
        if value == "CANCELED":
            return [element for element in transactions if element["state"] == value]
        elif value == "PENDING":
            return [element for element in transactions if element["state"] == value]
    return [element for element in transactions if element["state"] == value]


logger.info("utils.py is working. Status: ok")
