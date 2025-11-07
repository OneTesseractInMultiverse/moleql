from moleql.mql.core import MoleQL
from tests.moleql.core.shared_constants import (
    BLACKLIST,
    EXPECTED_PARAMETER_LIST,
    EXPECTED_PARAMETER_LIST_WITH_BLACKLISTED,
    INPUT_HQL_NOT_ENCODED,
    INPUT_HQL_URL_ENCODED,
)


class TestRawHQLProperty:
    def test_with_encoded_hql_no_blacklist(self):
        expected: list[str] = EXPECTED_PARAMETER_LIST
        actual: list[str] = MoleQL(moleql_query=INPUT_HQL_URL_ENCODED).raw_parameters
        assert expected == actual

    def test_without_encoded_hql_no_blacklist(self):
        expected: list[str] = EXPECTED_PARAMETER_LIST
        actual: list[str] = MoleQL(moleql_query=INPUT_HQL_NOT_ENCODED).raw_parameters
        assert expected == actual

    def test_with_encoded_hql_with_blacklist(self):
        expected: list[str] = EXPECTED_PARAMETER_LIST_WITH_BLACKLISTED
        actual: list[str] = MoleQL(
            moleql_query=INPUT_HQL_URL_ENCODED, blacklist=BLACKLIST
        ).raw_parameters
        assert expected == actual

    def test_without_encoded_hql_with_blacklist(self):
        expected: list[str] = EXPECTED_PARAMETER_LIST_WITH_BLACKLISTED
        actual: list[str] = MoleQL(
            moleql_query=INPUT_HQL_NOT_ENCODED, blacklist=BLACKLIST
        ).raw_parameters
        assert expected == actual
