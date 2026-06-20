import re

from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from datetime import datetime


def mask_account_card(text_data: str) -> str:
    """
    Функция принимает любую строку, в которой имеется 16тизначный номер карты
    или 20ти значным номер счёта и определяет куда дальше направлять
    После первого найденного номера обрабатывает его и возвращает текст до номера
    плюс замаскированный номер — без остальной части строки
    """
    card_found = bool(re.search(r"\b(\d{16})\b", text_data))
    account_found = bool(re.search(r"\b(\d{20})\b", text_data))

    if card_found and account_found:
        return "error: invalid format"
    if not card_found and not account_found:
        return ""

    # ищем 16ти значный номер карты в строке
    card_match = re.search(r"\b(\d{16})\b", text_data)
    if card_match:
        card_number = card_match.group(1)
        masked_card = get_mask_card_number(card_number)
        start, end = card_match.span()
        return text_data[:start] + masked_card

    # ищем 20ти значный номер счёта в строке
    account_match = re.search(r"\b(\d{20})\b", text_data)
    if account_match:
        account_number = account_match.group(1)
        masked_account = get_mask_account(account_number)
        start, end = account_match.span()
        return text_data[:start] + masked_account

    return ""


def get_date(date_str: str) -> str:
    """
    Функция принимает дату в формате 2024-03-11T02:26:18.671407,
    а возвращает в формате "ДД.ММ.ГГГГ"
    :param date_str:
    :return:
    """

    date_match = re.search(r"(\d{4})-(\d{2})-(\d{2})", date_str)
    if date_match:
        year, month, day = map(int, date_match.groups())
        try:
            datetime(year, month, day)  # валидация даты
            return f"{day:02d}.{month:02d}.{year}"
        except ValueError:
            return "error: invalid format"
    return "в строке дата формата 'YYYY-MM-DD' не найдена"


if __name__ == "__main__":
    # print(mask_account_card("Карта 1234567890123456 и ещё 9876543210000000"))
    # print(mask_account_card("Счет 12345678901234567890 и карта 1111222233334444"))
    print(mask_account_card("Visa Platinum 7000792289606361"))
    print(mask_account_card("Счет 73654108430135874305"))
    print(get_date("2024-03-11T02:26:18.671407"))
    print(
        filter_by_state(
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            "CANCELED",
        )
    )

    print(
        sort_by_date(
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            "from_first",
        )
    )
