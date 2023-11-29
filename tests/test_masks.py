import pytest

from src.masks import mask_card, mask_card_with_name, mask_count


@pytest.mark.parametrize(
    "value, expected_result",
    [
        ("7286844946221431", "7286 84** **** 1431"),
        ("3820488829287420", "3820 48** **** 7420"),
        ("6804119550473710", "6804 11** **** 3710"),
    ],
)
def test_mask_card(value: str, expected_result: str) -> None:
    assert mask_card(value) == expected_result


@pytest.mark.parametrize(
    "value, expected_result",
    [
        ("39745660563456619397", "**9397"),
        ("58803664561298323391", "**3391"),
        ("23294994494356835683", "**5683"),
    ],
)
def test_mask_count(value: str, expected_result: str) -> None:
    assert mask_count(value) == expected_result


@pytest.mark.parametrize(
    "value, expected_result",
    [
        ("Discover 0325955596714937", "Discover 0325 95** **** 4937"),
        ("Visa 3820488829287420", "Visa 3820 48** **** 7420"),
        ("Счет 23294994494356835683", "Счет **5683"),
        ("Счет 76145988629288763144", "Счет **3144"),
        ("American Express 5556525473658852", "American Express 5556 52** **** 8852"),
        ("Visa 3820488829287", "Некорректный номер карты/счёта"),
        ("Счет 76145988629", "Некорректный номер карты/счёта"),
    ],
)
def test_mask_card_with_name(value: str, expected_result: str) -> None:
    assert mask_card_with_name(value) == expected_result
