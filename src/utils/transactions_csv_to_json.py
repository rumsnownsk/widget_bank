import json
from pathlib import Path
from typing import List, Dict, Any

from src.config import PROJECT_ROOT
from src.loggers import logger_utils

import pandas as pd

logger = logger_utils()


def transactions_csv_to_json(
        filename: str = 'transactions.csv',
        base_dir: Path | None = None
) -> List[Dict[str, Any]]:
    """
    Преобразует CSV‑файл с транзакциями в список словарей с вложенной структурой

    Параметры:
      filename: имя CSV‑файла (по умолчанию 'transactions.csv').
      base_dir: корневая директория для поиска файла. Если не указана, используется PROJECT_ROOT.

    Возвращает:
      List[Dict]: список транзакций в виде словарей. Если файл не найден, пуст или ошибка чтения — пустой список.
    """

    root_dir = base_dir if base_dir is not None else PROJECT_ROOT
    file_path = root_dir / "data" / filename

    if not file_path.exists():
        logger.error(f'Файл {file_path} не найден (модуль "%s", функция "%s")', __name__,
                     transactions_csv_to_json.__name__)
        return []

    if file_path.stat().st_size == 0:
        logger.error(f'Файл {file_path} пустой (модуль "%s", функция "%s")', __name__,
                     transactions_csv_to_json.__name__)
        return []

    try:
        df = pd.read_csv(file_path, delimiter=";")
    except Exception as e:
        logger.error(
            'Ошибка при чтении CSV‑файла %s: %s (модуль "%s", функция "%s")',
            file_path, e, __name__, transactions_csv_to_json.__name__
        )
        return []
    if df.empty:
        logger.warning('CSV‑файл %s не содержит данных', file_path)
        return []

    # data = reviews.to_dict(orient='records')
    transactions = []

    for idx, row in df.iterrows():
        if  pd.isna(row.get('id')):
            logger.warning('Пропущена строка %d: отсутствует id', idx)
            continue

        # Безопасное приведение ID к int
        try:
            tx_id = int(row['id'])
        except (ValueError, TypeError):
            logger.warning('Пропущена строка %d: некорректный id "%s"', idx, row['id'])
            continue

        # Вложенная структура currency
        currency = {
            "name": row.get('currency_name', "unknown"),
            "code": row.get("currency_code","unknown")
        }

        # Вложенная структура operationAmount
        operation_amount = {
            "amount": str(row.get('amount', str(0))),
            "currency": currency
        }

        transaction = {
            "id": tx_id,
            "state": row.get('state',""),
            "date": row.get('date',""),
            "operationAmount": operation_amount,
            "description": row.get('description',""),
            "from": row.get('from',""),
            "to": row.get("to", ""),
            "type": row.get('type', ""),
            "category": row.get('category', ""),
            "paymentSystemId": "",
            "processingStatus": "",
            "reference": ""
        }
        transactions.append(transaction)
    # print(json.dumps(transactions, indent=2, ensure_ascii=False))

    return transactions


if __name__ == "__main__":
    transactions_csv_to_json()
