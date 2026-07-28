import re
from collections import Counter
from typing import Any, Dict, List

from src.utils.load_transactions import load_transactions


def process_bank_search(data: List[Dict[str, Any]], search: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Функция принимает список словарей с данными о банковских операциях
    и строку поиска по банковской операции,
    а возвращает список операций, у которых есть данная операция
    :param data:
    :param search:
    :return:
    """
    search = search.lower()
    pattern = re.compile(re.escape(search))

    return [
        item
        for item in data
        if (state := item.get("state")) is not None and isinstance(state, str) and pattern.search(state.lower())
    ]


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество банковских операций по заданным категориям.

    Функция фильтрует список транзакций по полю ``description`` и возвращает
    словарь, где ключи — названия категорий (из списка ``categories``),
    а значения — количество операций, относящихся к каждой категории.

    Параметры
    ---------
    data : List[Dict[str, Any]]
        Список словарей, описывающих банковские операции. Каждый словарь
        должен содержать ключ ``"description"`` (желательно строку).
    categories : List[str]
        Список допустимых категорий (описаний операций), по которым
        выполняется подсчёт.

    Возвращает
    ----------
    Dict[str, int]
        Словарь вида ``{категория: количество}``. Если для какой‑либо
        категории не найдено ни одной операции, она не будет включена
        в результат.

    """
    counted = Counter([item["description"] for item in data if item.get("description") in categories])
    return dict(counted)


def get_all_available_states() -> Dict[int, str]:
    """
    Возвращает нумерованный словарь уникальных статусов транзакций.

    Функция загружает все транзакции, извлекает поле `state`, отфильтровывает
    нестроковые значения, убирает дубликаты (сохраняя порядок первого появления)
    и нормализует статусы к нижнему регистру.

    Возвращаемый словарь имеет вид: {номер: статус}, например:
        {1: "executed", 2: "pending", 3: "canceled"}
    """
    data = load_transactions()

    # dict.fromkeys убирает дубликаты и сохраняет порядок первого вхождения
    unique_states = dict.fromkeys(
        state.lower()
        for item in data
        if (state := item.get("state")) is not None and isinstance(state, str) and state.strip() != ""
    ).keys()
    return {i: state.lower() for i, state in enumerate(unique_states, start=1)}


# if __name__ == "__main__":
#     json_transactions = load_transactions()
#     event = "EXECUTEd"
#
#     search_result = process_bank_search(json_transactions, event)
#
#     print(json.dumps(search_result, indent=4, ensure_ascii=False))
#     print(f"Найдено операций по событию {event}: {len(search_result)};")
#     print(f"Всего операций загружено из файла transactions.json: {len(json_transactions)};")
#     # ===========================
#     print("\n")
#     count_desc = process_bank_operations(
#         json_transactions, ["Перевод с карты на счет", "Открытие вклада", "Перевод организации"]
#     )
#
#     print(count_desc)
#
#     get_all_available_states()
