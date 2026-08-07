import logging

from src.config import PROJECT_ROOT


def logger_masks():
    # Путь к папке и файлу
    logs_dir = PROJECT_ROOT / "logs"
    log_file = logs_dir / "log_masks.log"

    # Создаём только папку (не файл!)
    logs_dir.mkdir(parents=True, exist_ok=True)

    logger_object = logging.getLogger("logger_masks")
    logger_object.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file, encoding="utf-8", mode="w")
    file_formatter = logging.Formatter(f"{'=' * 30}\n%(asctime)s \n %(name)s \n %(levelname)s: %(message)s")

    file_handler.setFormatter(file_formatter)
    logger_object.addHandler(file_handler)
    return logger_object


def logger_utils():
    logs_dir = PROJECT_ROOT / "logs"
    log_file = logs_dir / "log_utils.log"

    logs_dir.mkdir(parents=True, exist_ok=True)

    logger_object = logging.getLogger("logger_utils")
    logger_object.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file, encoding="utf-8", mode="w")
    file_formatter = logging.Formatter(f"{'=' * 30}\n%(asctime)s \n %(name)s \n %(levelname)s: %(message)s")

    file_handler.setFormatter(file_formatter)
    logger_object.addHandler(file_handler)
    return logger_object
