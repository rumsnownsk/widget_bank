import re


from masks import get_mask_card_number, get_mask_account


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
