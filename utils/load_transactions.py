import json
from pathlib import Path
from typing import Any, Dict

BASE_DIR = Path(__file__).resolve().parent.parent


def load_transactions(filename: str = "transactions.json", base_dir: Path | None = None) -> list[Dict[str, Any]]:
    """
    Функция принимает файл с данными формата json и возвращает json данные
    :param base_dir:
    :param filename:
    :return:
    """
    if base_dir is None:
        base_dir = BASE_DIR
    file_path = base_dir / "data" / filename

    if not file_path.exists():
        return []

    if file_path.stat().st_size == 0:
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            transactions_json = json.load(f)
    except json.JSONDecodeError:
        return []

    return transactions_json


print(load_transactions())
