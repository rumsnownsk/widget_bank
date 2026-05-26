import re


def mask_account_card(text_data:str)->str:

    card_match = re.search(r'\b\d{16}\b', text_data)
    if card_match:
        card_number = card_match.group()
        card_mask = card_number[0:6] + '*'*6 + card_number[-4:]

        # Добавляем пробелы после каждого 4‑го символа
        return ' '.join(card_mask[i:i+4] for i in range(0, len(card_mask), 4))

    account_match = re.search(r'\b\d{20}\b', text_data)
    if account_match:
        account = account_match.group()
        return "**" + account[-4:]

    return "No data"


if __name__ == '__main__':
    print(mask_account_card('Visa Platinum 7000792289606361'))