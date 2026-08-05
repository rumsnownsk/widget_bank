from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.utils.dataframe_to_json import dataframe_to_json


@pytest.fixture
def project_root(tmp_path):
    """Создает временную директорию для теста (изолированная среда)"""
    return tmp_path


@pytest.fixture
def data_dir(project_root):
    d = project_root / "data"
    d.mkdir(exist_ok=True)
    return d


@patch("src.utils.dataframe_to_json.pd.read_csv")
def test_csv_success(mock_read_csv, project_root, data_dir):
    mock_df = pd.DataFrame(
        [
            {
                "id": 1,
                "amount": 100.5,
                "currency_name": "Рубль",
                "currency_code": "RUB",
                "state": "COMPLETED",
                "date": "2024-01-01",
                "description": "Оплата",
                "from": "Client A",
                "to": "Bank",
                "type": "PAYMENT",
            },
            {
                "id": 2,
                "amount": 200.0,
                "currency_name": "Доллар",
                "currency_code": "USD",
                "state": "PENDING",
                "date": "2024-01-02",
                "description": "Перевод",
                "from": "Client B",
                "to": "Client C",
                "type": "TRANSFER",
            },
        ]
    )
    mock_read_csv.return_value = mock_df

    fake_file = data_dir / "test.csv"
    fake_file.write_text("id,amount,currency_name,currency_code,state,date,description,from,to,type\n")

    result = dataframe_to_json("test.csv", base_dir=project_root)

    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[0]["operationAmount"]["amount"] == 100.5
    assert result[1]["operationAmount"]["currency"]["code"] == "USD"

    mock_read_csv.assert_called_once()


@patch("src.utils.dataframe_to_json.pd.read_csv")
def test_bad_amount_fallback_to_zero(mock_read_csv, data_dir, project_root):
    mock_df = pd.DataFrame([{"id": 1, "amount": "сто рублей"}, {"id": 2, "amount": None}])
    mock_df.loc[1, "amount"] = float("nan")
    mock_read_csv.return_value = mock_df

    fake_file = data_dir / "test.csv"
    fake_file.write_text("test_any_data")

    result = dataframe_to_json("test.csv", base_dir=project_root)
    assert len(result) == 2
    assert all(t["operationAmount"]["amount"] == 0.0 for t in result)


def test_file_not_found(project_root, caplog):
    result = dataframe_to_json("non_existent.csv", base_dir=project_root)
    assert result == []
    assert "не найден" in caplog.text


def test_empty_file(project_root, caplog, tmp_path):
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)
    empty_file = data_dir / "empty.csv"
    empty_file.touch()

    result = dataframe_to_json("empty.csv", base_dir=project_root)
    assert result == []
    assert "пустой" in caplog.text


@patch("src.utils.dataframe_to_json.pd.read_csv", side_effect=Exception("Disk error"))
def test_pandas_read_error(mock_read_csv, project_root, caplog, data_dir):
    fake_file = data_dir / "broken.csv"
    fake_file.write_text("id,amount\n1,100\n")
    result = dataframe_to_json("broken.csv", base_dir=project_root)

    assert result == []
    assert "Ошибка при чтении" in caplog.text


@patch("src.utils.dataframe_to_json.pd.read_excel")
def test_xlsx_success(mock_read_excel, data_dir, project_root):
    mock_df = pd.DataFrame([{"id": 999, "amount": 50.0, "currency_name": "Евро", "currency_code": "EUR"}])
    mock_read_excel.return_value = mock_df

    fake_file = data_dir / "test.xlsx"
    fake_file.write_bytes(b"dummy")
    result = dataframe_to_json("test.xlsx", base_dir=project_root)

    assert len(result) == 1
    assert result[0]["id"] == 999
    assert result[0]["operationAmount"]["amount"] == 50.0
    mock_read_excel.assert_called_once()


@patch("src.utils.dataframe_to_json.pd.read_csv")
def test_nested_structure_correct(mock_read_csv, data_dir, project_root):
    mock_df = pd.DataFrame(
        [
            {
                "id": 1,
                "amount": 150.75,
                "currency_name": "Bitcoin",
                "currency_code": "BTC",
                "state": "OK",
                "date": "2024-10-10",
                "description": "BTC Buy",
                "from": "User1",
                "to": "Exchange",
                "type": "BUY",
                "category": "Crypto",
            }
        ]
    )
    mock_read_csv.return_value = mock_df

    fake_file = data_dir / "test.csv"
    fake_file.write_text("test_data")

    result = dataframe_to_json("test.csv", base_dir=project_root)
    tx = result[0]
    assert tx["operationAmount"]["amount"] == 150.75
    assert tx["operationAmount"]["currency"]["name"] == "Bitcoin"
    assert tx["paymentSystemId"] == ""


@patch("src.utils.dataframe_to_json.pd.read_csv")
def test_unsupported_extension(mock_read_csv, project_root, caplog, data_dir):
    bad_file = data_dir / "data.txt"
    bad_file.write_text("some text")

    result = dataframe_to_json("data.txt", base_dir=project_root)
    assert result == []
    assert "Неподдерживаемый формат" in caplog.text or "Ошибка определения типа файла" in caplog.text
    mock_read_csv.assert_not_called()
