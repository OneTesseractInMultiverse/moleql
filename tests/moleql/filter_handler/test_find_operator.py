from moleql.mql.constants import EMPTY_STRING
from moleql.mql.filter_handler import find_operator
from tests.moleql.core.shared_constants import (
    EQUALS,
    GREATER_OR_EQUALS_THAN,
    GREATER_THAN,
    LESS_OR_EQUALS_THAN,
    LESS_THAN,
    NOT,
    NOT_EQUALS,
)


class TestFindOperator:
    def test_equals_operator(self):
        expected: str = EQUALS
        actual: str = find_operator("key=value")
        assert expected == actual

    def test_not_equals(self):
        expected: str = NOT_EQUALS
        actual: str = find_operator("key!=value")
        assert expected == actual

    def test_less_or_equals_than_operator(self):
        expected: str = LESS_OR_EQUALS_THAN
        actual: str = find_operator("key<=value")
        assert expected == actual

    def test_greater_or_equals_than_operator(self):
        expected: str = GREATER_OR_EQUALS_THAN
        actual: str = find_operator("key>=value")
        assert expected == actual

    def test_greater_than_operator(self):
        expected: str = GREATER_THAN
        actual: str = find_operator("key>value")
        assert expected == actual

    def test_less_than_operator(self):
        expected: str = LESS_THAN
        actual: str = find_operator("key<value")
        assert expected == actual

    def test_exists_operator(self):
        # key
        expected: str = EMPTY_STRING
        actual: str = find_operator("key")
        assert expected == actual

    def test_not_exists_operator(self):
        expected: str = NOT
        actual: str = find_operator("!key")
        assert expected == actual

    def test_operator_char_in_value_picks_leftmost_operator(self):
        # ">" is leftmost; old code using find() would have returned "=" instead
        assert find_operator("price>10=something") == GREATER_THAN

    def test_two_char_operator_with_more_operators_in_value(self):
        # "!=" starts at index 3; stray ">" later in the string must not interfere
        assert find_operator("key!=val>other") == NOT_EQUALS
