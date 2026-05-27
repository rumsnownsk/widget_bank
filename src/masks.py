from typing import Union
import re

from black import replace


def get_mask_card_number(card_data: str) -> str:
    """
    Функция маскировки номера банковской карты по шаблону XXXX XX** **** XXXX
    """
    pattern = r'\b(\d{4})(\d{2})(\d{6})(\d{4})\b'
    replacement = r'\1 \2** **** \4'
    return re.sub(pattern, replacement, card_data)


def get_mask_account(account_data: str) -> str:
    """
    Функция маскировки номера банковского счета
    Оставляет видимым только последние 4 цифры
    """
    pattern = r'\b(\d{16})(\d{4})\b'
    replacement = r'**\2'
    return re.sub(pattern, replacement, account_data)


def validator(card_number: str) -> tuple[list[str], bool]:
    """
    Проверяет и преобразует номер карты к строковому формату

    Выполняет следующие проверки:
    1. Если номер — целое число, преобразует его в строку
    2. Убеждается, что номер имеет строковый тип
    3. Проверяет, что строка содержит только цифры
    4. Убеждается, что длина строки составляет ровно 16 символов

    Args:
        card_number (Union[str, int]): номер карты или счёта — строка или целое число

    Returns:
        str: валидный номер в виде строки из 16 цифр

    Raises:
        TypeError: если номер не является числом или строкой
        ValueError: если номер содержит нецифровые символы или не имеет длины 16
    """
    is_valid = True
    errors = list()

    if not isinstance(card_number, str):
        errors.append("Номер должен быть числом или строкой из чисел, где ровно 16 цифр")
        is_valid = False

    if not card_number.isdigit():
        errors.append("Номер должен содержать только цифры")
        is_valid = False

    if len(card_number) != 16:
        errors.append("Номер должен содержать ровно 16 цифр")
        is_valid = False

    return errors, is_valid
