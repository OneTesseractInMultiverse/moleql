from typing import Any

import pytest

from moleql.mql.errors import CustomCasterError
from moleql.mql.filter_handler import custom_cast


class TestCustomCast:
    def test_when_custom_caster_and_valid_rule(self):
        expected: str = "1.44"
        actual: str = custom_cast(value="string(1.44)", casters={"string": str})
        assert expected == actual

    def test_when_custom_caster_but_no_matching_rule(self):
        expected: Any = None
        actual: str = custom_cast(value="1.44", casters={"string": str})
        assert expected == actual

    def test_when_custom_caster_with_invalid_value(self):
        with pytest.raises(CustomCasterError):
            custom_cast(value="int(xyz)", casters={"int": int})

    def test_when_casters_is_none_returns_none(self):
        # Covers the "if not casters" guard branch
        assert custom_cast(value="anything", casters=None) is None

    def test_when_custom_caster_returns_none_intentionally(self):
        # The caster matched and explicitly returned None — must not fall back to default
        actual: Any = custom_cast(value="nullable(x)", casters={"nullable": lambda _: None})
        assert actual is None
