from src.controller import get_transactions
from src.logger import setup_logger
from src.parser import get_currency
from src.utils import get_info_about_transaction, get_kind_of_transaction

logger = setup_logger()

if __name__ == "__main__":
    while True:
        transactions = get_transactions()
        try:
            user_input = int(
                input(
                    'Если вы хотите посмотреть транзакцию, нажмите "1". '
                    'Если вы хотите отсортировать транзакции по статусу, нажмите "2". '
                    'Если хотите выйти, нажмите "3": '
                )
            )

            if user_input == 1:
                transaction_input = int(input("Введите индитификатор транзакции, чтобы посмотреть транзакцию: "))
                if len(str(transaction_input)) == 7 or len(str(transaction_input)) == 6:
                    transaction = get_info_about_transaction(transaction_input)
                    print(transaction)

                    if transaction == "Неверно введён индитификатор транзакции":
                        continue
                    else:
                        currency_input = int(
                            input(
                                "Если сумма транзакции не в рублях, Вы можете её изменить. " 'Для этого нажмите "1": '
                            )
                        )

                        if currency_input == 1:
                            currency = get_currency(transaction["Тикер валюты"])
                            print(currency)
                            transaction["Сумма"] = round(currency * transaction["Сумма"], 2)
                            transaction["Тикер валюты"] = "RUB"
                            print(transaction)
                        continue

            elif user_input == 2:
                status_input = input('Введите один из типов транзакций: "EXECUTED", "CANCELED" или "PENDING": ')
                if status_input in ["EXECUTED", "CANCELED", "PENDING"]:
                    print(get_kind_of_transaction(status_input))
                else:
                    print("Неверно введён тип транзакции")
                    continue

            elif user_input == 3:
                break

            else:
                print("Некорректно введён запрос")
                continue

        except ValueError:
            print("Ответ должен содержать только цифры")
            continue
