from typing import Literal


def filter_by_state(data: list, state: str = "EXECUTED") -> list:
    """Функция возвращает список словарей, у которых state соответствует"""
    return [item for item in data if item["state"] == state]


def sort_by_date(data: list, sort_by: Literal["from_last", "from_first"] = "from_last") -> list:
    """
    Функция сортирует данные по дате
    Args:
        data (list): Список словарей с полем 'date'.
        sort_by (str): Способ сортировки. Допустимые значения:
            - 'from_last' (по умолчанию) — от последних к первым;
            - 'from_first' — от первых к последним.

    Returns:
        list: Отсортированный список словарей.
    """
    if sort_by == "from_last":
        return sorted(data, key=lambda x: x["date"], reverse=True)
    elif sort_by == "from_first":
        return sorted(data, key=lambda x: x["date"], reverse=False)
    return data
