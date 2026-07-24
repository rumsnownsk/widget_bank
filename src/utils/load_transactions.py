import json
from pathlib import Path
from typing import Any, Dict

from src.loggers import logger_utils
from src.config import PROJECT_ROOT


logger = logger_utils()


def load_transactions(
        filename: str = "transactions.json",
        base_dir: Path | None = None
) -> list[Dict[str, Any]]:
    """
    Функция принимает файл с данными формата json и возвращает json данные
    :param base_dir:
    :param filename:
    :return:
    """
    logger.debug('обращение к модулю "%s", функция "%s"', __name__, load_transactions.__name__)
    root_dir = base_dir if base_dir is not None else PROJECT_ROOT

    file_path = root_dir / "data" / filename

    if not file_path.exists():
        logger.error(f'Файл {file_path} не найден (модуль "%s", функция "%s")', __name__, load_transactions.__name__)
        return []

    if file_path.stat().st_size == 0:
        logger.error(f'Файл {file_path} пустой (модуль "%s", функция "%s")', __name__, load_transactions.__name__)
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            transactions_json = json.load(f)
            logger.info(f"Чтение файла {file_path} прошло зашибись!" )
    except json.JSONDecodeError:
        logger.error(
            f'Ошибка декодирования файла {file_path} (модуль "%s", функция "%s")', __name__, load_transactions.__name__
        )
        return []

    return transactions_json


if __name__ == "__main__":
    print(load_transactions())
