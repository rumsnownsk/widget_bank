import re

from masks import get_mask_card_number, get_mask_account
from processing import filter_by_state


def mask_account_card(text_data: str) -> str:
    """
    Функция принимает любую строку, в которой имеется 16тизначный номер карты
    или 20ти значным номер счёта и определяет куда дальше направлять
    """
    mask = ""

    if bool(re.search(r"\b\d{16}\b", text_data)):
        mask = get_mask_card_number(text_data)

    if bool(re.search(r"\b\d{20}\b", text_data)):
        mask = get_mask_account(text_data)

    return mask


def get_date(date_str: str) -> str:
    """
    Функция принимает дату в формате 2024-03-11T02:26:18.671407,
    а возвращает в формате "ДД.ММ.ГГГГ"
    :param date_str:
    :return:
    """
    date_match = re.search(r"(\d{4})-(\d{2})-(\d{2})", date_str)
    if date_match:
        return f"{date_match.group(3)}.{date_match.group(2)}.{date_match.group(1)}"
    else:
        return f"в строке '{date_str}' дата не найдена"


if __name__ == "__main__":
    print(mask_account_card("Visa Platinum 7000792289606361"))
    print(mask_account_card("Счет 73654108430135874305"))
    print(get_date("2024-03-11T02:26:18.671407"))
    print(filter_by_state([{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                           {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
                           {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                           {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]
                          , 'CANCELED'))
