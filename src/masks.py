from typing import Union


def get_mask_card_number(card_number: Union[str, int]) -> str:
    """
    Функция маскировки номера банковской карты по шаблону XXXX XX** **** XXXX.
    Функция validator() проверяет корректность (есть ли буквы и длину строки)

    Args:
        card_number (Union[int, str]): число или строка из 16 цифр

    Returns:
        str: замаскированный номер
    """
    card_number = str(card_number)

    (errors, is_valid) = validator(card_number)

    if is_valid:
        part1 = card_number[0:4]
        part2 = card_number[4:6]
        part3 = card_number[-4:]

        return f"{part1} {part2}** **** {part3}"
    else:
        print(*["❌ " + error for error in errors], sep="\n")
        return ""


def get_mask_account(account_number: Union[int, str]) -> str:
    """
    Функция маскировки номера банковского счета
    Оставляет видимым только последние 4 цифры
    🦧 Отдельную функцию валидации прикручивать не стал. Скучно .
    🐼 Тороплюсь делаю уроки до более интересных заданий
    Args:
        account_number (Union[int, str]): число или строка из 16 цифр

    Returns:
        str: замаскированный номер
    """
    if isinstance(account_number, int):
        account_number = str(account_number)
    if len(account_number) >= 4:
        return f"**{str(account_number)[-4:]}"
    else:
        print(f"Неверный формат счёта клиента")
        return ""


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


# print(get_mask_card_number("1234567890123456"))
# print(get_mask_card_number("12srdgadf56"))
# print(get_mask_account("73654108430135874305"))
