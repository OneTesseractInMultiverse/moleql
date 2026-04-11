from moleql.mql.filter_handler import cast


class TestCast:
    def test_returns_none_when_custom_caster_returns_none(self):
        # Core bug fix: a matched custom caster that returns None must be preserved,
        # not treated as "no match" and silently replaced by default_cast.
        actual = cast(value="nullable(x)", casters={"nullable": lambda _: None})
        assert actual is None

    def test_falls_back_to_default_when_no_rule_matches(self):
        # Casters provided but no rule matches the value — default cast applies.
        actual = cast(value="42", casters={"string": str})
        assert actual == 42

    def test_falls_back_to_default_when_casters_is_none(self):
        actual = cast(value="3.14", casters=None)
        assert actual == 3.14
