import json
import random
from pathlib import Path
from unittest import result

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def transactions() -> list:
    return [
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
            "fee": {"amount": "20.00", "currency": "USD"},
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
        },
        {
            "id": 309817234,
            "state": "EXECUTED",
            "date": "2020-01-15T11:47:12.102391",
            "operationAmount": {"amount": "3500.50", "currency": {"name": "EUR", "code": "EUR"}},
            "description": "Оплата услуг подрядчика",
            "from": "Счет 28374657382910293847",
            "to": "Счет 99887766554433221100",
            "type": "OUTGOING_PAYMENT",
            "category": "SERVICES",
            "tags": ["contract", "freelance"],
            "fee": {"amount": "25.75", "currency": "EUR"},
            "paymentSystemId": "PS-20200115-003322",
            "processingStatus": "COMPLETED",
            "reference": "CON-2020-9988",
        },
        {
            "id": 551298372,
            "state": "PENDING",
            "date": "2021-03-22T09:15:33.441002",
            "operationAmount": {"amount": "12000.00", "currency": {"name": "RUB", "code": "RUB"}},
            "description": "Пополнение счёта для закупки",
            "to": "Счет 55667788990011223344",
            "type": "DEPOSIT",
            "category": "FUNDS_IN",
            "tags": ["topup", "inventory"],
            "fee": {"amount": "0.00", "currency": "RUB"},
            "paymentSystemId": "PS-20210322-007766",
            "processingStatus": "IN_PROGRESS",
            "reference": "TOP-2021-5544",
        },
        {
            "id": 882937461,
            "state": "CANCELED",
            "date": "2021-05-10T16:22:11.992837",
            "operationAmount": {"amount": "850.00", "currency": {"name": "GBP", "code": "GBP"}},
            "description": "Платёж поставщику (отменён)",
            "from": "Счет 33445566778899001122",
            "to": "Счет 88776655443322110099",
            "type": "OUTGOING_PAYMENT",
            "category": "SERVICES",
            "tags": ["cancelled", "supplier"],
            "fee": {"amount": "5.50", "currency": "GBP"},
            "paymentSystemId": "PS-20210510-005544",
            "processingStatus": "CANCELLED_BY_USER",
            "reference": "ORD-2021-1122",
        },
        {
            "id": 227738495,
            "state": "EXECUTED",
            "date": "2022-08-19T14:03:45.112233",
            "operationAmount": {"amount": "450.75", "currency": {"name": "JPY", "code": "JPY"}},
            "description": "Мелкий платёж за лицензию",
            "from": "Счет 11223344556677889900",
            "to": "Счет 00998877665544332211",
            "type": "LICENCE_FEE",
            "category": "EXPENSES",
            "tags": ["license", "software"],
            "fee": {"amount": "2.00", "currency": "JPY"},
            "paymentSystemId": "PS-20220819-001100",
            "processingStatus": "COMPLETED",
            "reference": "LIC-2022-7766",
        },
        {
            "id": 663399221,
            "state": "EXECUTED",
            "date": "2023-11-03T08:55:22.334455",
            "operationAmount": {"amount": "210000.00", "currency": {"name": "RUB", "code": "RUB"}},
            "description": "Выплата зарплаты по ведомости",
            "from": "Счет 44556677889900112233",
            "type": "PAYROLL",
            "category": "PAYROLL_EXPENSES",
            "tags": ["salary", "payroll"],
            "fee": {"amount": "1050.00", "currency": "RUB"},
            "paymentSystemId": "PS-20231103-008877",
            "processingStatus": "COMPLETED",
            "reference": "PAY-2023-Q4",
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
    ]


def test_filter_by_currency_usd(transactions):
    expected = [t for t in transactions if t["operationAmount"]["currency"]["code"] == "USD"]
    assert list(filter_by_currency(transactions)) == expected


def test_filter_by_currency_with_exist_currency(transactions):
    assert list(filter_by_currency(transactions, "SAME")) == []


@pytest.fixture
def empty_json() -> list:
    return []


def test_filter_by_currency_empty_json(empty_json):
    assert list(filter_by_currency(empty_json)) == []


def test_transaction_descriptions(transactions):
    assert list(transaction_descriptions(transactions)) == [
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


@pytest.mark.parametrize(
    "start, end, list_cards",
    [
        (
            1,
            10,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
                "0000 0000 0000 0004",
                "0000 0000 0000 0005",
                "0000 0000 0000 0006",
                "0000 0000 0000 0007",
                "0000 0000 0000 0008",
                "0000 0000 0000 0009",
            ],
        ),
        (5, 5, []),
    ],
)
def test_card_number_generator(start, end, list_cards):
    assert list(card_number_generator(start, end)) == list_cards


def test_card_number_generator_invalid_range():
    with pytest.raises(ValueError):
        list(card_number_generator(-1, 10))

    with pytest.raises(ValueError):
        list(card_number_generator(0, 10**16 + 1))
