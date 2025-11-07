import pytest

from moleql.mql.errors import LimitError
from moleql.mql.limit_skip_handler import LimitHandler


class TestLimitHandler:
    def test_when_limit_parameter_has_no_value(self):
        expected: int = 0
        actual: int = LimitHandler(limit_parameter="limit=").limit
        assert expected == actual

    def test_when_limit_value_has_valid_value(self):
        expected: int = 100
        actual: int = LimitHandler(limit_parameter="limit=100").limit
        assert expected == actual

    def test_when_limit_value_has_no_numerical_value(self):
        with pytest.raises(ValueError):
            LimitHandler(limit_parameter="limit=abc").limit

    def test_when_limit_value_is_negative(self):
        with pytest.raises(LimitError):
            LimitHandler(limit_parameter="limit=-100").limit
