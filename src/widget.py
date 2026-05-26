import re


def mask_account_card(text_data: str) -> str:
    """
    Функция принимает любую строку, в которой имеется 16тизначный номер карты
    или 20ти значным номер счёта и возвращает их маску
    """
    card_match = re.search(r"\b\d{16}\b", text_data)
    if card_match:
        card_number = card_match.group()
        card_mask = card_number[0:6] + "*" * 6 + card_number[-4:]

        # Добавляем пробелы после каждого 4‑го символа
        return " ".join(card_mask[i:i + 4] for i in range(0, len(card_mask), 4))

    account_match = re.search(r"\b\d{20}\b", text_data)
    if account_match:
        account = account_match.group()
        return "**" + account[-4:]

    return "No data"


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
    print(get_date("2024-03-11T02:26:18.671407"))
