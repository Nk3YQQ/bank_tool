import pytest

from src.utils import (get_description_info, get_info_about_transaction, get_info_about_transactions,
                       get_kind_of_transaction, get_statistic_about_transactions, reformat_date)


@pytest.mark.parametrize(
    "date_, expected_result",
    [
        ("2018-07-11T02:26:18.671407", "11.07.2018"),
        ("2023-10-31T02:26:18.671407", "31.10.2023"),
        ("2023-13-31T02:26:18.671407", "Некорректно введена дата"),
        ("", "Некорректно введена дата"),
        ("2018-07-11", "11.07.2018"),
    ],
)
def test_reformat_date(date_: str, expected_result: str) -> None:
    assert reformat_date(date_) == expected_result


data = [
    {
        "Индитификатор": 650703,
        "Статус": "EXECUTED",
        "Дата": "05.09.2023",
        "Сумма": 16210.0,
        "Тикер валюты": "PEN",
        "Откуда": "Счет **3391",
        "Куда": "Счет **9397",
        "Описание": "Перевод организации",
    },
    {
        "Индитификатор": 3598919,
        "Статус": "EXECUTED",
        "Дата": "06.12.2020",
        "Сумма": 29740.0,
        "Тикер валюты": "COP",
        "Откуда": "Discover 3172 60** **** 0065",
        "Куда": "Discover 0720 42** **** 4643",
        "Описание": "Перевод с карты на карту",
    },
    {
        "Индитификатор": 593027,
        "Статус": "CANCELED",
        "Дата": "22.07.2023",
        "Сумма": 30368.0,
        "Тикер валюты": "TZS",
        "Откуда": "Visa 1959 23** **** 4097",
        "Куда": "Visa 6804 11** **** 3710",
        "Описание": "Перевод с карты на карту",
    },
]


@pytest.mark.parametrize(
    "value, expected_result",
    [
        (650703, data[0]),
        (3598919, data[1]),
        (593027, data[2]),
        (7782990902, "Неверно введён индитификатор транзакции"),
        ("Ошибка", "Неверно введён индитификатор транзакции"),
    ],
)
def test_get_info_about_transaction(value: int, expected_result: dict | str) -> None:
    assert get_info_about_transaction(value, "data/transactions.json") == expected_result


@pytest.fixture
def get_data() -> list[dict]:
    return [
        {
            "id": 650703,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210.0,
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
            "description": "Перевод организации",
        },
        {
            "id": 5380041,
            "state": "CANCELED",
            "date": "2021-02-01T11:54:58Z",
            "amount": 23789.0,
            "currency_name": "Peso",
            "currency_code": "UYU",
            "from": None,
            "to": "Счет 23294994494356835683",
            "description": "Открытие вклада",
        },
        {
            "id": 1932532,
            "state": "PENDING",
            "date": "2020-02-19T00:17:13Z",
            "amount": 25246.0,
            "currency_name": "Forint",
            "currency_code": "HUF",
            "from": "Discover 6177546839517597",
            "to": "American Express 9695664158183113",
            "description": "Перевод с карты на карту",
        },
    ]


def test_get_kind_of_transaction(get_data: list[dict]) -> None:
    assert get_data[0] in get_kind_of_transaction("EXECUTED", "data/transactions.json")
    assert get_data[1] in get_kind_of_transaction("CANCELED", "data/transactions.json")
    assert get_data[2] in get_kind_of_transaction("PENDING", "data/transactions.json")


def test_get_description_info() -> None:
    assert get_description_info("data/transactions.json") == {
        "Перевод организации": None,
        "Перевод с карты на карту": None,
        "Открытие вклада": None,
        "Перевод со счета на счет": None,
        "Без описания": None,
    }


def test_get_info_about_transactions() -> None:
    assert len(get_info_about_transactions("Перевод организации", "data/transactions.json")) == 117
    assert len(get_info_about_transactions("Перевод с карты на карту", "data/transactions.json")) == 587
    assert len(get_info_about_transactions("Открытие вклада", "data/transactions.json")) == 185
    assert len(get_info_about_transactions("Перевод со счета на счет", "data/transactions.json")) == 110


def test_get_statistic_about_transactions() -> None:
    description_info = get_description_info("data/transactions.json")
    description_statistic = get_statistic_about_transactions(description_info, "data/transactions.json")
    assert description_statistic["Перевод организации"] == 117
    assert description_statistic["Перевод с карты на карту"] == 587
    assert description_statistic["Открытие вклада"] == 185
    assert description_statistic["Перевод со счета на счет"] == 110
    assert description_statistic["Без описания"] == 1
