import json
import re
from collections import Counter

from src.utils.load_transactions import load_transactions


def process_bank_search(
        data: list[dict],
        search: str = "EXECUTED"
) -> list[dict]:
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
        if (state := item.get('state')) is not None
           and isinstance(state, str)
           and pattern.search(state.lower())
    ]


def process_bank_operations(data: list[dict], categories: list) -> dict:

    counted = Counter([
        item['description']
        for item in data
        if item.get('description') in categories
    ])
    return dict(counted)



if __name__ == "__main__":
    json_transactions = load_transactions()
    event = 'EXECUTEd'

    search_result = process_bank_search(json_transactions, event)

    print(json.dumps(search_result, indent=4, ensure_ascii=False))
    print(f"Найдено операций по событию {event}: {len(search_result)};")
    print(f"Всего операций загружено из файла transactions.json: {len(json_transactions)};")
    # ===========================
    print('\n')
    count_desc = process_bank_operations(json_transactions, [
        "Перевод с карты на счет",
        "Открытие вклада",
        "Перевод организации"
    ])

    print(count_desc)


