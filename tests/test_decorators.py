from pathlib import Path

import pytest

from src.decorators import log

log_file_path_str = "tests/tmp/test_log.txt"

def test_log_success():
    @log(filename=log_file_path_str)
    def summ_nums(a, b):
        return a + b

    summ_nums(2, 3)

    log_file = Path(log_file_path_str)
    content = log_file.read_text(encoding='utf-8')

    assert "status: OK" in content
    assert "result: 5" in content


def test_log_error():
    @log(filename=log_file_path_str)
    def fail():
        raise Exception("Всё сломалось!!")

    with pytest.raises(Exception):
        fail()

    log_file = Path(log_file_path_str)
    content = log_file.read_text(encoding='utf-8')

    assert "status: ERROR" in content
    assert "error_type: " in content

def test_log_no_filename(capsys):
    @log()
    def say():
        return "hello"
    say()
    captured = capsys.readouterr()

    assert "func_name: say" in captured.out
    assert "status: OK" in captured.out