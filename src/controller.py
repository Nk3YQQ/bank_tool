import json
import logging
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


def get_transactions(file_path: str = "../data/transactions.csv") -> Any:
    """
    Функция принимает на вход путь до .csv и xlsx-файла, записывает данные в json-файл и возвращает список словарей
    с данными о финансовых транзакциях. Если файл пустой, содержит не список или не найден, функция возвращает пустой
    список.
    """
    try:
        if ".csv" in file_path:
            data = pd.read_csv(file_path)
            data["id"] = data["id"].fillna(0).astype(int)
            data.to_json("../data/transactions.json", orient="records", force_ascii=False, indent=4)
            logger.info("get_transactions is working. Status: ok")
            return data
        elif ".xlsx" in file_path:
            data = pd.read_excel(file_path)
            data["id"] = data["id"].fillna(0).astype(int)
            data.to_json("../data/transactions.json", orient="records", force_ascii=False, indent=4)
            logger.info("get_transactions is working. Status: ok")
            return data
        else:
            logger.error("get_transaction error: Некорректно введено имя файла")
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        logger.error("get_transaction error: FileNotFoundError/json.decoder.JSONDecodeError")
        return []
