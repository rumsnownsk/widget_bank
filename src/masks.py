import re


def get_mask_card_number(card_number: str) -> str:
    """
    Функция маскировки номера банковской карты по шаблону XXXX XX** **** XXXX
    """
    pattern = r"\b(\d{4})(\d{2})(\d{6})(\d{4})\b"
    replacement = r"\1 \2** **** \4"
    return re.sub(pattern, replacement, card_number)


def get_mask_account(account_data: str) -> str:
    """
    Функция маскировки номера банковского счета
    Оставляет видимым только последние 4 цифры
    """
    pattern = r"\b(\d{16})(\d{4})\b"
    replacement = r"**\2"
    return re.sub(pattern, replacement, account_data)