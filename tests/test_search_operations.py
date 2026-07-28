from unittest.mock import patch

from src.search_operations import get_all_available_states, process_bank_operations, process_bank_search


def test_process_bank_search_exact_match():
    data = [
        {"state": "EXECUTED"},
        {"state": "PENDING"},
        {"state": "CANCELED"},
    ]
    result = process_bank_search(data, "EXECUTED")
    assert len(result) == 1
    assert result[0]["state"] == "EXECUTED"


def test_process_bank_search_case_insensitive():
    data = [
        {"state": "executed"},
        {"state": "Executed"},
        {"state": "EXECUTED"},
    ]
    result = process_bank_search(data, "EXECUTED")
    assert len(result) == 3


def test_process_bank_search_partial_match_via_regex():
    data = [
        {"state": "EXECUTED_OK"},
        {"state": "PARTIALLY_EXECUTED"},
        {"state": "NOT_EXECUTED"},
    ]
    result = process_bank_search(data, "EXECUTED")
    assert len(result) == 3


def test_process_bank_search_no_matches():
    data = [
        {"state": "PENDING"},
        {"state": "CANCELED"},
    ]
    result = process_bank_search(data, "EXECUTED")
    assert result == []


def test_process_bank_search_missing_state_key():
    data = [
        {"other_field": "value"},
        {"state": None},
        {"state": 123},
    ]
    result = process_bank_search(data, "EXECUTED")
    assert result == []


def test_process_bank_operations_exact_match():
    data = [
        {"description": "Перевод с карты на счет"},
        {"description": "Открытие вклада"},
        {"description": "Перевод организации"},
        {"description": "Перевод с карты на счет"},
    ]
    categories = ["Перевод с карты на счет", "Открытие вклада", "Перевод организации"]

    result = process_bank_operations(data, categories)

    assert result == {"Перевод с карты на счет": 2, "Открытие вклада": 1, "Перевод организации": 1}


def test_process_bank_operations_ignores_non_listed_descriptions():
    data = [
        {"description": "Перевод с карты на счет"},
        {"description": "Неизвестная операция"},
        {"description": "Еще одна неизвестная"},
    ]
    categories = ["Перевод с карты на счет"]
    result = process_bank_operations(data, categories)
    assert result == {"Перевод с карты на счет": 1}


def test_process_bank_operations_empty_data():
    data = []
    categories = ["Перевод с карты на счет"]
    result = process_bank_operations(data, categories)
    assert result == {}


@patch("src.search_operations.load_transactions")
def test_get_all_available_states_returns_numbered_dict(mock_load):
    mock_load.return_value = [
        {"state": "EXECUTED"},
        {"state": "PENDING"},
        {"state": "EXECUTED"},  # дубликат
        {"state": "CANCELED"},
        {"state": None},  # пропускается
        {"state": 123},  # пропускается (не строка)
    ]
    result = get_all_available_states()
    # порядок сохраняется по первому вхождению, дубликаты удалены
    expected = {
        1: "executed",
        2: "pending",
        3: "canceled",
    }
    assert result == expected


@patch("src.search_operations.load_transactions")
def test_get_all_available_states_empty_data(mock_load):
    mock_load.return_value = []
    result = get_all_available_states()
    assert result == {}


@patch("src.search_operations.load_transactions")
def test_get_all_available_states_all_invalid_states(mock_load):
    mock_load.return_value = [
        {"state": None},
        {"state": 123},
        {"state": ""},
        {"state": "   "},
    ]
    result = get_all_available_states()
    assert result == {}
