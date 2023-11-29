import logging

logger = logging.getLogger(__name__)


def mask_card(card_number: str) -> str:
    """
    Функция принимает на вход номер карты и возвращает его маску
    """
    masked_card = card_number[:4] + " " + card_number[4:6] + "** " + "**** " + card_number[12:]
    logger.info("mask_card is working. Status: ok")
    return masked_card


def mask_count(count_number: str) -> str:
    """
    Функция принимает на вход номер счёта и возвращает его маску
    """
    masked_count = "**" + count_number[16:20]
    logger.info("mask_count is working. Status: ok")
    return masked_count


def mask_card_with_name(info: str) -> str:
    """
    Функция принимает строку с именем и номером карты/счёта и возвращает замаскированную карту/замаскированный счёт.
    Если номер карты или счёта не соответствует условиям, то функция возвращает текст "Некорректный номер карты/счёта"
    """
    split_info = info.split(" ")
    if len(split_info) == 3 and len(split_info[2]) == 16 and split_info[2].isdigit() is True:
        logger.info("mask_card_with_name is working. Status: ok")
        return f"{split_info[0]} {split_info[1]} {mask_card(split_info[2])}"
    if len(split_info[1]) == 16 and split_info[1].isdigit() is True:
        logger.info("mask_card_with_name is working. Status: ok")
        return f"{split_info[0]} {mask_card(split_info[1])}"
    elif len(split_info[1]) == 20 and split_info[1].isdigit() is True:
        logger.info("mask_card_with_name is working. Status: ok")
        return f"{split_info[0]} {mask_count(split_info[1])}"
    else:
        logger.error("mask_card_with_name error: Некорректный номер карты/счёта")
        return "Некорректный номер карты/счёта"
