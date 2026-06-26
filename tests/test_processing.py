import pytest
from mypy.types import Any

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def coll() -> list:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 0, "state": "", "date": ""},
        {"id": 0, "state": None, "date": ""},
        {"id": 0, "hello": "world", "str": "no"},
        "not a dict",
        {},
    ]


def test_filter_by_state_executed(coll: list[dict[str, Any]]) -> None:
    assert filter_by_state(coll, "EXECUTED") == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


def test_filter_by_state_canceled(coll: list[dict[str, Any]]) -> None:
    assert filter_by_state(coll, "CANCELED") == [
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
    ]


def test_sort_by_date_from_first(coll: list[dict[str, Any]]) -> None:
    assert sort_by_date(coll, "from_first") == [
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}
    ]


def test_sort_by_date_from_last(coll: list[dict[str, Any]]) -> None:
    assert sort_by_date(coll, "from_last") == [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
    ]


def test_invalid_sort_by() -> None:
    with pytest.raises(ValueError):
        sort_by_date([], "invalid_value")


def test_non_list_input() -> None:
    with pytest.raises(TypeError):
        sort_by_date("not_a_list")
