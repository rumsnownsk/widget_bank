import json

from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent

def get_transactions(filename="transactions.json") -> list:
    """
    Функция принимает файл с данными формата json и возвращает json данные
    :param filename:
    :return:
    """
    file_path = base_dir / "data" / filename

    if not file_path.exists():
        return []

    if file_path.stat().st_size == 0:
        return []

    try:
        with open(file_path, "r", encoding='utf-8') as f:
            transactions_json = json.load(f)
    except json.JSONDecodeError:
        return []

    return transactions_json
