import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize('value, result', [
    ("1234567890123456", "1234 56** **** 3456"),
    ("0000000000000000", "0000 00** **** 0000"),
    ("", ""),
])
def test_get_mask_card_number(value, result):
    assert get_mask_card_number(value) == result

@pytest.mark.parametrize('value, result', [
    ("12345678901234567890", "**7890"),
    ("", ""),
])
def test_get_account(value, result):
    assert get_mask_account(value) == result

