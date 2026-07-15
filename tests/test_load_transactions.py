import json
from pathlib import Path
from unittest.mock import Mock

import pytest

from utils.load_transactions import load_transactions


def test_load_transactions_file_not_found(tmp_path: Path):
    result = load_transactions("transactions.json", base_dir=tmp_path)
    assert result == []


def test_load_transactions_empty_file(tmp_path: Path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    (data_dir / "transactions.json").write_text("")

    result = load_transactions("transactions.json", base_dir=tmp_path)
    assert result == []


def test_load_transactions_valid_json(tmp_path: Path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    transactions = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
    (data_dir / "transactions.json").write_text(json.dumps(transactions))
    result = load_transactions("transactions.json", base_dir=tmp_path)

    assert len(result) == 2
    assert result[0]["id"] == 1
