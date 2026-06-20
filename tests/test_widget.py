import pytest

from src.widget import mask_account_card, get_date


@pytest.mark.parametrize('value, result', [
    ("Visa Platinum 7000792289606361","Visa Platinum 7000 79** **** 6361"),
    ("Счет 73654108430135874305", "Счет **4305"),
    ("Счет 2345", ""),
    ("",""),
    ("Просто текст", ""),
    ("Карта 1234567890123456 и ещё 9876543210987654", "Карта 1234 56** **** 3456"),  # Несколько 16‑значных
    ("Счет 12345678901234567890 и карта 1111222233334444", "error: invalid format"),  # 20‑ и 16‑значный

])
def test_mask_account_card(value, result):
    assert mask_account_card(value) == result

@pytest.mark.parametrize("value, result",[
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("2024-03-11", "11.03.2024"),
    pytest.param("2024.03.11", "в строке '2024.03.11' дата не найдена", id='invalid_format'),
    pytest.param("", "в строке '' дата не найдена", id='invalid_format'),
])
def test_get_date(value, result):
    assert get_date(value) == result