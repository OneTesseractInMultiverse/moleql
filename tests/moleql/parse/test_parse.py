import datetime

from moleql import parse as parse
from moleql.default_casters import DEFAULT_HQL_CASTERS


class TestParse:
    def test_when_empty_query(self):
        expected = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual = parse("")
        assert expected == actual

    def test_simple_projection(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": {"_id": 1},
        }
        actual = parse("fields=_id")
        assert expected == actual

    def test_multiple_field_projection(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": {"_id": 1, "score": 1, "status": 1},
        }
        actual = parse("fields=_id,score,status")
        assert expected == actual

    def test_range_query_with_blacklist(self):
        expected: dict = {
            "filter": {
                "user_id": {"$gt": 525, "$lt": 600},
                "creation_date": {
                    "$gte": datetime.datetime.fromisoformat("2022-10-29T00:00:00.000000"),
                    "$lte": datetime.datetime.fromisoformat("2022-10-30T00:00:00.000000"),
                },
            },
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual: dict = parse(
            "user_id>525&user_id<600&creation_date>=2022-10-29T00:00:00.000000"
            "&creation_date<=2022-10-30T00:00:00.000000",
            blacklist=tuple(["latitude", "longitude"]),
        )
        assert expected == actual

    def test_caster_merge(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": {"_id": 1, "score": 1, "status": 1},
        }
        actual = parse("fields=_id,score,status", casters=DEFAULT_HQL_CASTERS)
        assert expected == actual
