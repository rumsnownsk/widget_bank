import re


def mask_account_card(text:str)->str:
    card_number_mask = ''

    card_match = re.search(r'\b\d{16}\b', text)
    if card_match:
        card_number = card_match.group()
        card_mask = card_number[0:6] + '*'*6 + card_number[-4:]

        # Добавляем пробелы после каждого 4‑го символа
        card_number_mask = ' '.join(card_mask[i:i+4] for i in range(0, len(card_mask), 4))

    else:
        return f"Номер карты не обнаружен. Исходные данные: '{text}'"
        return card_number_mask
    return 'No data'

if __name__ == '__main__':
    print(mask_account_card('Visa Platinum 7000792289606361'))