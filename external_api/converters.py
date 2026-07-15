import os

import requests
from dotenv import load_dotenv

load_dotenv()


def convert_to_rub(trn):
    """
    Функция возвращает сумму операции в рублях.

    :param trn:
    :return:
    """

    operation_amount = trn.get("operationAmount")

    if not operation_amount:
        raise ValueError("Нет данных по стоимости")

    amount_val = operation_amount.get("amount")
    currency = operation_amount.get("currency", {})
    from_code = currency.get("code")
    to_code = "RUB"

    if not from_code:
        raise ValueError("Не указан код валюты операции")

    try:
        amount = float(amount_val)
    except (TypeError, ValueError):
        raise ValueError(f"Некорректное значение суммы: {amount_val}")

    if from_code == "RUB":
        return amount

    api_key = os.getenv("API_KEY_APILAYER")
    if not api_key:
        raise RuntimeError("API ключ API_KEY_APILAYER не найден в переменных окружения")

    payload = {}
    headers = {"apikey": api_key}
    url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_code}&from={from_code}&amount={amount}"

    try:
        response = requests.request("GET", url, headers=headers, data=payload, timeout=5)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        raise RuntimeError("Превышено время ожидания ответа от API сервиса")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Ошибка сети при запросе курса: {e}") from e
    except ValueError as e:
        raise RuntimeError(f"Не удалось распарсить ответ API: {e}") from e

    result = data.get("result")
    if result is None:
        raise RuntimeError(f"API не вернул поле 'result'. Ответ: {data}")

    return float(result)

if __name__ == "__main__":

    transaction = {
        "id": 663399221,
        "state": "EXECUTED",
        "date": "2023-11-03T08:55:22.334455",
        "operationAmount": {"amount": "210000.00", "currency": {"name": "JPY", "code": "JPY"}},
        "description": "Выплата зарплаты по ведомости",
        "from": "Счет 44556677889900112233",
        "to": "null",
        "type": "PAYROLL",
        "category": "PAYROLL_EXPENSES",
        "tags": ["salary", "payroll"],
        "fee": {"amount": "1050.00", "currency": "RUB"},
        "paymentSystemId": "PS-20231103-008877",
        "processingStatus": "COMPLETED",
        "reference": "PAY-2023-Q4",
    }

    print(convert_to_rub(transaction))
