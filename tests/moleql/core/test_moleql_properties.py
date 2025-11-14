from moleql.mql.constants import FILTER, LIMIT_KEY, PROJECTION_KEY, SKIP_KEY, SORT_KEY
from moleql.mql.core import MoleQL
from tests.moleql.core.shared_constants import (
    BLACKLIST,
    EXPECTED_PARAMETER_LIST,
    EXPECTED_PARAMETER_LIST_WITH_BLACKLISTED,
    INPUT_QUERY_NOT_ENCODED,
    INPUT_QUERY_URL_ENCODED,
)


class TestRawMoleQLProperty:
    def test_with_encoded_hql_no_blacklist(self):
        expected: list[str] = EXPECTED_PARAMETER_LIST
        actual: list[str] = MoleQL(moleql_query=INPUT_QUERY_URL_ENCODED).raw_parameters
        assert expected == actual

    def test_without_encoded_hql_no_blacklist(self):
        expected: list[str] = EXPECTED_PARAMETER_LIST
        actual: list[str] = MoleQL(moleql_query=INPUT_QUERY_NOT_ENCODED).raw_parameters
        assert expected == actual

    def test_with_encoded_hql_with_blacklist(self):
        expected: list[str] = EXPECTED_PARAMETER_LIST_WITH_BLACKLISTED
        actual: list[str] = MoleQL(
            moleql_query=INPUT_QUERY_URL_ENCODED, blacklist=BLACKLIST
        ).raw_parameters
        assert expected == actual

    def test_without_encoded_hql_with_blacklist(self):
        expected: list[str] = EXPECTED_PARAMETER_LIST_WITH_BLACKLISTED
        actual: list[str] = MoleQL(
            moleql_query=INPUT_QUERY_NOT_ENCODED, blacklist=BLACKLIST
        ).raw_parameters
        assert expected == actual

    def test_filter_when_empty(self):
        expected: dict = {
            FILTER: {},
            SORT_KEY: None,
            SKIP_KEY: 0,
            LIMIT_KEY: 0,
            PROJECTION_KEY: None,
        }[FILTER]

        actual: dict = MoleQL(moleql_query="").mongo_filter
        assert expected == actual

    def test_projection_when_empty(self):
        assert MoleQL(moleql_query="").mongo_projection is None
