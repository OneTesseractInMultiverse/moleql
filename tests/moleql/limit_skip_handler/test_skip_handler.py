import pytest

from moleql.mql.errors import SkipError
from moleql.mql.limit_skip_handler import SkipHandler


class TestLimitHandler:
    def test_when_skip_parameter_has_no_value(self):
        expected: int = 0
        actual: int = SkipHandler(skip_parameter="skip=").skip
        assert expected == actual

    def test_when_skip_value_has_valid_value(self):
        expected: int = 100
        actual: int = SkipHandler(skip_parameter="skip=100").skip
        assert expected == actual

    def test_when_skip_value_has_no_numerical_value(self):
        with pytest.raises(ValueError):
            SkipHandler(skip_parameter="skip=abc").skip

    def test_when_skip_value_is_negative(self):
        with pytest.raises(SkipError):
            SkipHandler(skip_parameter="skip=-100").skip
