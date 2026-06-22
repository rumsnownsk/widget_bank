import re
from datetime import datetime

from typing import Literal


def filter_by_state(data: list, state: Literal["EXECUTED", "CANCELED"] = "EXECUTED") -> list:
    """
    Функция возвращает список словарей, у которых поле 'state' точно соответствует
    указанному значению.

    Args:
        data (list): Список словарей с транзакциями.
        state (str): Значение state для фильтрации. Допустимые значения:
            - 'EXECUTED' (по умолчанию);
            - 'CANCELED'

    Returns:
        list: Отфильтрованный список словарей.
    """
    if not isinstance(data, list):
        raise TypeError("Parameter 'data' must be a list")

    result = []
    for item in data:
        if not isinstance(item, dict):
            continue
        #проверка наличия ключа 'state' и его значение
        item_state = item.get("state")
        if isinstance(item_state, str) and item_state == state:
            result.append(item)

    return result


def sort_by_date(data: list, sort_by: Literal["from_last", "from_first"] = "from_last") -> list:
    """
    Функция возвращает список словарей, отсортированных по полю 'date'.
    Args:
        data (list): Список словарей с полем 'date'.
        sort_by (str): Способ сортировки. Допустимые значения:
            - 'from_last' (по умолчанию) — от последних к первым;
            - 'from_first' — от первых к последним.

    Returns:
        list: Отсортированный список словарей.

    Raises:
        TypeError: если data не является списком или sort_by имеет недопустимое значение
    """
    if not isinstance(data, list):
        raise TypeError("Parameter 'data' must be a list")

    if sort_by not in ["from_last", "from_first"]:
        raise ValueError("Parameter 'sort_by' must be 'from_last' or 'from_first'")

    def parse_date(el: dict) -> datetime | None:
        date_str = el.get("date")

        if not isinstance(date_str, str):
            return None
        try:
            return datetime.fromisoformat(date_str)
        except ValueError:
            return None

    result = []
    for item in data:
        if isinstance(item, dict):
            if parse_date(item) is not None:
                result.append(item)
    reverse = sort_by == "from_last"

    return sorted(result, key=lambda x: x["date"], reverse=reverse)
