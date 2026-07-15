from unittest.mock import patch

import pytest
import requests

from external_api.converters import convert_to_rub


@patch("external_api.converters.requests.request")
def test_conver_to_rub(mock_request):
    mock_request.return_value.status_code = 200
    mock_request.return_value.json.return_value = {"result": 65.42}

    transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "JPY"}}}
    result = convert_to_rub(transaction)
    assert result == 65.42
    mock_request.assert_called_once()
    assert mock_request.call_count == 1


@patch("external_api.converters.requests.request")
def test_convert_to_rub_no_api_call(mock_request):

    transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "RUB"}}}

    result = convert_to_rub(transaction)

    assert result == 100.00
    mock_request.assert_not_called()  # проверяем, что сеть не трогали
    assert mock_request.call_count == 0


def test_convert_to_rub_missing_amount():
    transaction = {"any": "data"}

    with pytest.raises(ValueError, match="Нет данных по стоимости"):
        convert_to_rub(transaction)


def test_convert_to_rub_missing_code_currency():
    transaction = {"operationAmount": {"amount": "100.00", "currency": {"NONE": "NONE"}}}

    with pytest.raises(ValueError, match="Не указан код валюты операции"):
        convert_to_rub(transaction)


@patch("external_api.converters.requests.request")
def test_convert_to_rub_network_timeout(mock_request):
    # Заставляем request сразу выбросить Timeout
    mock_request.side_effect = requests.exceptions.Timeout

    transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "JPY"}}}

    with pytest.raises(RuntimeError, match="Превышено время ожидания "):
        convert_to_rub(transaction)


@patch("external_api.converters.requests.request")
def test_convert_to_rub_missing_field(mock_request):
    mock_request.return_value.status_code = 200
    mock_request.return_value.json.return_value = {"other_field": 65.42}

    transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "EUR"}}}
    with pytest.raises(RuntimeError, match="API не вернул поле 'result'"):
        convert_to_rub(transaction)
