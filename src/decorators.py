import inspect
from datetime import datetime
from functools import wraps
from pathlib import Path
from time import time

base_dir = Path(__file__).resolve().parent.parent


def log(filename=None):
    """
    Декоратор для логирования вызовов функций: фиксирует входные данные, результат/ошибку,
    время выполнения и сохраняет лог в файл.

    Папка для логов создаётся относительно корня проекта (определяется автоматически по
    расположению файла decorators.py). Если папка не существует — она будет создана.
    """

    def decor(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            time_start_raw = time()
            time_start = datetime.fromtimestamp(time_start_raw).strftime("%d-%m-%Y %H:%M:%S")
            result = None
            error = None

            try:
                result = func(*args, **kwargs)
            except Exception as e:
                error = e
            time_end_raw = time()
            time_end = datetime.fromtimestamp(time_end_raw).strftime("%d-%m-%Y %H:%M:%S")
            duration = time_end_raw - time_start_raw

            # Формируем лог
            log_lines = [
                "-" * 40,
                f"source_file: {inspect.getfile(func)}",
                f"func_name: {func.__name__}",
                f"time_start: {time_start}",
                f"time_end: {time_end}",
                f"duration_sec: {duration:.4f}",
            ]
            if error is not None:
                log_lines.append("status: ERROR")
                log_lines.append(f"inputs: {args}, {kwargs}")
                log_lines.append(f"error_type: {type(error).__name__}")
                log_lines.append(f"error_message: {error}")
            else:
                log_lines.append("status: OK")
                log_lines.append(f"result: {str(result)}")

            log_txt = "\n".join(log_lines) + "\n"

            if filename:
                log_file_path = base_dir / filename
                parent_dir = log_file_path.parent

                print(f"this - {parent_dir}")

                if parent_dir:
                    parent_dir.mkdir(parents=True, exist_ok=True)

                try:
                    with open(log_file_path, "a", encoding="utf-8") as f:
                        f.write(log_txt)
                except OSError as e:
                    print(f"[LOG ERROR] не удалось записать лог в {log_file_path} : {e}")
                    print(log_txt)
            else:
                print(log_txt)

            if error is not None:
                raise error

            return result

        return wrapper

    return decor
