import json
import logging
import re
from collections import Counter
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


def get_info_about_transactions(string: str, filepath: str = "../data/transactions.json") -> list[dict]:
    """
    Функция принимает данные о транзакциях и строку поиска и возвращает список транзакций по описанию
    транзакции, которая задана в строке поиска
    """
    with open(filepath, "r", encoding="utf-8") as file:
        transactions = json.load(file)

        matching_transactions = []

        for transaction in transactions:
            description = transaction.get("description")
            if description and re.search(re.escape(string), description, re.IGNORECASE):
                matching_transactions.append(transaction)

        return matching_transactions


def get_description_info(filepath: str = "../data/transactions.json") -> dict:
    """
    Функция создаёт словарь с категориями описаний транзакций в файле, который хранит список транзакций
    """
    data: dict = {}
    with open(filepath, "r", encoding="utf-8") as file:
        transactions = json.load(file)
        for transaction in transactions:
            description = transaction["description"]
            if description not in data.keys():
                data[description] = None
        data["Без описания"] = data.pop(None)
        return data


def get_statistic_about_transactions(categories: dict, filepath: str = "../data/transactions.json") -> dict:
    """
    Функция принимает список словарей с данными о банковских операциях и словарь категорий операций и возвращать
    словарь, в котором ключи — это названия категорий, а значения — это количество операций в каждой категории
    """
    with open(filepath, "r", encoding="utf-8") as file:
        transactions = json.load(file)
        list_of_description = [transaction["description"] for transaction in transactions]
        counted = Counter(list_of_description)
        categories["Перевод организации"] = counted["Перевод организации"]
        categories["Перевод с карты на карту"] = counted["Перевод с карты на карту"]
        categories["Открытие вклада"] = counted["Открытие вклада"]
        categories["Перевод со счета на счет"] = counted["Перевод со счета на счет"]
        categories["Без описания"] = counted[None]
        return categories


logger.info("utils.py is working. Status: ok")
