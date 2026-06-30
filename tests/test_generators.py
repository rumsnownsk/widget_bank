import json
import random
from pathlib import Path
from unittest import result

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions

base_dir = Path(__file__).resolve().parent.parent
file_path = base_dir / "data" / "transactions.json"

transactions_json = []
if not file_path.exists():
    print(f"Предупреждение: файл не найден: {file_path}. Возвращаем пустой набор транзакций.")
else:
    with open(file_path, "r", encoding="utf-8") as f:
        transactions_json = json.load(f)


@pytest.mark.parametrize(
    "value, result",
    [
        (
                transactions_json,
                [
                    {
                        "id": 939719570,
                        "state": "EXECUTED",
                        "date": "2018-06-30T02:08:58.425572",
                        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
                        "description": "Перевод организации",
                        "from": "Счет 75106830613657916952",
                        "to": "Счет 11776614605963066702",
                        "type": "INTERNAL_TRANSFER",
                        "category": "BUSINESS_PAYMENTS",
                        "tags": ["payment", "supplier"],
                        "fee": {"amount": "0.00", "currency": "USD"},
                        "paymentSystemId": "PS-20180630-001234",
                        "processingStatus": "COMPLETED",
                        "reference": "INV-2018-654321",
                    },
                    {
                        "id": 142264268,
                        "state": "EXECUTED",
                        "date": "2019-04-04T23:20:05.206878",
                        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
                        "description": "Перевод со счета на счет",
                        "from": "Счет 19708645243227258542",
                        "to": "Счет 75651667383060284188",
                        "type": "ACCOUNT_TO_ACCOUNT",
                        "category": "INTERNAL_FUNDS",
                        "tags": ["transfer", "personal"],
                        "fee": {"amount": "15.00", "currency": "USD"},
                        "paymentSystemId": "PS-20190404-009876",
                        "processingStatus": "COMPLETED",
                        "reference": None,
                    },
                    {
                        "id": 774488332,
                        "state": "EXECUTED",
                        "date": "2024-02-14T12:12:12.121212",
                        "operationAmount": {"amount": "199.99", "currency": {"name": "USD", "code": "USD"}},
                        "description": "Онлайн-покупка подписки",
                        "from": "Карта 411111******1111",
                        "to": "Merchant 1234567890",
                        "type": "CARD_PAYMENT",
                        "category": "SUBSCRIPTIONS",
                        "tags": ["subscription", "online"],
                        "fee": {"amount": "0.00", "currency": "USD"},
                        "paymentSystemId": "PS-20240214-002211",
                        "processingStatus": "COMPLETED",
                        "reference": "SUB-2024-FEB",
                    },
                ],
        ),
    ],
)
def test_filter_by_currency(value: list, result: list):
    assert list(filter_by_currency(value)) == result


def test_filter_by_currency_with_exist_currency():
    assert list(filter_by_currency(transactions_json, "SAME")) == []


@pytest.fixture
def empty_json() -> list:
    return []


def test_filter_by_currency_empty_json(empty_json):
    assert list(filter_by_currency(empty_json)) == []


def test_transaction_descriptions():
    assert list(transaction_descriptions(transactions_json)) == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Оплата услуг подрядчика",
        "Пополнение счёта для закупки",
        "Платёж поставщику (отменён)",
        "Мелкий платёж за лицензию",
        "Выплата зарплаты по ведомости",
        "Онлайн-покупка подписки",
    ]


def test_transaction_descriptions_empty_json(empty_json):
    assert list(transaction_descriptions(empty_json)) == []


@pytest.mark.parametrize("start, end, list_cards", [
    (1, 10, [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
        "0000 0000 0000 0006",
        "0000 0000 0000 0007",
        "0000 0000 0000 0008",
        "0000 0000 0000 0009"
    ]),
    (5, 5, [
    ]),
])
def test_card_number_generator(start, end, list_cards):
    assert list(card_number_generator(start, end)) == list_cards

def test_card_number_generator_invalid_range():
    with pytest.raises(ValueError):
        list(card_number_generator(-1, 10))

    with pytest.raises(ValueError):
        list(card_number_generator(0, 10**16 + 1))
