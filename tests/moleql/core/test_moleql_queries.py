import datetime

import pymongo
import pytest

from moleql.mql.core import MoleQL
from moleql.mql.errors import (
    FilterError,
    LimitError,
    ListOperatorError,
    SkipError,
    TextOperatorError,
)


class TestMoleQLQuery:
    def test_when_empty_query(self):
        expected = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual = MoleQL("").mongo_query
        assert expected == actual


class TestMoleQLProjection:
    def test_simple_projection(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": {"_id": 1},
        }
        actual = MoleQL("fields=_id").mongo_query
        assert expected == actual

    def test_exclusion_projection(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": {"_id": 0},
        }
        actual = MoleQL("fields=-_id").mongo_query
        assert expected == actual

    def test_embedded_projection(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": {"settings.group": 1},
        }
        actual = MoleQL("fields=settings.group").mongo_query
        assert expected == actual

    def test_multiple_field_projection(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": {"_id": 1, "score": 1, "status": 1},
        }
        actual = MoleQL("fields=_id,score,status").mongo_query
        assert expected == actual

    def test_multiple_exclusion_projection(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": {"_id": 0, "score": 0, "status": 0},
        }
        actual = MoleQL("fields=-_id,-score,-status").mongo_query
        assert expected == actual

    def test_complex_projection(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": {
                "vulnerabilities": {"$elemMatch": {"score": {"$gt": 5}}},
                "last_seen": 1,
                "due_date": 1,
            },
        }
        actual = MoleQL(
            'fields={"vulnerabilities": {"$elemMatch":{"score": {"$gt":' " 5}}}},last_seen,due_date"
        ).mongo_query
        assert expected == actual


class TestMoleQLQueryLimit:
    def test_good_limit(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 5,
            "limit": 0,
            "projection": None,
        }
        actual = MoleQL("skip=5").mongo_query
        assert expected == actual

    def test_empty_limit(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual = MoleQL("skip=").mongo_query
        assert expected == actual

    def test_negative_limit(self):
        with pytest.raises(SkipError):
            MoleQL("skip=-5").mongo_query

    def test_non_numeric_limit(self):
        with pytest.raises(ValueError):
            MoleQL("skip=bad_skip").mongo_query


class TestMoleQLQuerySkip:
    def test_good_limit(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 5,
            "projection": None,
        }
        actual = MoleQL("limit=5").mongo_query
        assert expected == actual

    def test_empty_limit(self):
        expected: dict = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual = MoleQL("limit=").mongo_query
        assert expected == actual

    def test_negative_limit(self):
        with pytest.raises(LimitError):
            MoleQL("limit=-5").mongo_query

    def test_non_numeric_limit(self):
        with pytest.raises(ValueError):
            MoleQL("limit=bad_limit").mongo_query


class TestRangeQueries:
    def test_simple_range_support(self):
        expected: dict = {
            "filter": {"score": {"$gt": 525, "$lt": 600}},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual = MoleQL("score>525&score<600").mongo_query
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
        actual: dict = MoleQL(
            "user_id>525&user_id<600&creation_date>=2022-10-29T00:00:00.000000"
            "&creation_date<=2022-10-30T00:00:00.000000",
            blacklist=tuple(["latitude", "longitude"]),
        ).mongo_query
        assert expected == actual


class TestMoleQLSort:
    def test_empty_sort(self):
        expected = {
            "filter": {},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual = MoleQL("sort=").mongo_query
        assert expected == actual

    def test_ascending_sort(self):
        expected = {
            "filter": {},
            "sort": [("_id", pymongo.ASCENDING)],
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual = MoleQL("sort=_id").mongo_query
        assert expected == actual

    def test_ascending_sort_with_operator(self):
        expected = {
            "filter": {},
            "sort": [("_id", pymongo.ASCENDING)],
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual = MoleQL("sort=+_id").mongo_query
        assert expected == actual

    def test_descending_sort_with_operator(self):
        expected = {
            "filter": {},
            "sort": [("_id", pymongo.DESCENDING)],
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual = MoleQL("sort=-_id").mongo_query
        assert expected == actual

    def test_multiple_ascending_sort(self):
        expected = {
            "filter": {},
            "sort": [
                ("_id", pymongo.ASCENDING),
                ("created_at", pymongo.ASCENDING),
                ("price", pymongo.ASCENDING),
            ],
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual = MoleQL("sort=_id,created_at,price").mongo_query
        assert expected == actual

    def test_multiple_descending_sort(self):
        expected = {
            "filter": {},
            "sort": [
                ("_id", pymongo.DESCENDING),
                ("created_at", pymongo.DESCENDING),
                ("price", pymongo.DESCENDING),
            ],
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual = MoleQL("sort=-_id,-created_at,-price").mongo_query
        assert expected == actual

    def test_multiple_mixed_sort(self):
        expected = {
            "filter": {},
            "sort": [
                ("_id", pymongo.ASCENDING),
                ("created_at", pymongo.DESCENDING),
                ("price", pymongo.ASCENDING),
                ("active", pymongo.DESCENDING),
            ],
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual = MoleQL("sort=_id,-created_at,price,-active").mongo_query
        assert expected == actual


class TestMoleQLFullTextSearch:
    def test_good_text_operator(self):
        expected = {
            "filter": {"$text": {"$search": "full text search"}},
            "sort": None,
            "skip": 0,
            "limit": 0,
            "projection": None,
        }
        actual = MoleQL("$text=full text search").mongo_query
        assert expected == actual

    def test_empty_text_operator(self):
        with pytest.raises(TextOperatorError):
            MoleQL("$text=").mongo_query


class TestMoleQLQueryErrors:
    def test_list_operator_error(self):
        with pytest.raises(ListOperatorError):
            MoleQL("tags<=CR,US,FR").mongo_query

    def test_filter_error(self):
        with pytest.raises(FilterError):
            MoleQL("tags==CR").mongo_query
