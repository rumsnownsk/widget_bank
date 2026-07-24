import logging

from src.config import PROJECT_ROOT


def logger_masks():
    # Путь к папке и файлу
    logs_dir = PROJECT_ROOT / "logs"
    log_file = logs_dir / "log_masks.log"

    # Создаём только папку (не файл!)
    logs_dir.mkdir(parents=True, exist_ok=True)

    l = logging.getLogger("logger_masks")
    l.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file, encoding="utf-8", mode="w")
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s ')

    file_handler.setFormatter(file_formatter)
    l.addHandler(file_handler)
    return l

def logger_utils():
    logs_dir = PROJECT_ROOT / "logs"
    log_file = logs_dir / "log_utils.log"

    logs_dir.mkdir(parents=True, exist_ok=True)

    l = logging.getLogger("logger_utils")
    l.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file, encoding="utf-8", mode="w")
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s ')

    file_handler.setFormatter(file_formatter)
    l.addHandler(file_handler)
    return l