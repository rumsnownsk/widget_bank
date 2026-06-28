import json
from pathlib import Path
import random

base_dir = Path(__file__).resolve().parent.parent
file_path = base_dir / "data" / "transactions.json"


transactions_json = []
if not file_path.exists():
    print(f"Предупреждение: файл не найден: {file_path}. Возвращаем пустой набор транзакций.")
else:
    with open(file_path, 'r', encoding="utf-8") as f:
        transactions_json = json.load(f)

print('\n')
print("========= список транзакций по 'currency_code' (по умолчанию - USD) ======== ")
def filter_by_currency(data, currency_code = "USD"):
    """
    Генератор для фильтрации транзакций по коду валюты.
    Фунция принимает итеррируемый объект и возвращает иттератор,
    который поочередно выдает транзакции,
    где валюта операции соответствует заданной
    :param data: Итерируемый набор транзакций (обычно list[dict])
    :param currency_code: Код валюты для фильтрации (по умолчанию "USD")
    :return: Генератор, выдающий подходящие транзакции
    """
    for t in data:
        try:
            curr_code = t['operationAmount']['currency']['code']
        except KeyError:
            continue
        if curr_code == currency_code:
            yield t


usd_transactions = filter_by_currency(transactions_json)

for i in usd_transactions:
    print(i)

print('\n')
print("========= возвращаем описание каждой операции по очереди ======== ")

def transaction_descriptions(data):
    for i in data:
        yield i["description"]


for i in transaction_descriptions(transactions_json):
    print(i)

print('\n')
print("========= генерируем случайные номера банковских карт ======== ")

def card_number_generator(count_card):
    def four_digits():
        digits = [str(random.randint(0, 9)) for _ in range(4)]
        return "".join(digits)
    for _ in range(count_card):
        yield f"{four_digits()} {four_digits()} {four_digits()} {four_digits()}"

for number_card in card_number_generator(5):
    print(number_card)

