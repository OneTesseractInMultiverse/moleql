import pytest

from moleql.mql.errors import FilterError
from moleql.mql.regex_parser import parse_regex


class TestParseRegex:
    @pytest.mark.parametrize(
        "value, expected",
        [
            # Plain text, no slashes
            ("plain-text", {"$regex": "plain-text"}),
            # Leading/trailing spaces are stripped
            ("  spaced  ", {"$regex": "spaced"}),
            # Slash form, no flags
            ("/ab+c/", {"$regex": "ab+c"}),
            # Slash form with single valid flag
            ("/ab+c/i", {"$regex": "ab+c", "$options": "i"}),
            # Slash form with multiple valid flags
            ("/foo.*/ims", {"$regex": "foo.*", "$options": "ims"}),
            # Escaped slash inside pattern
            (r"/a\/b/x", {"$regex": r"a\/b", "$options": "x"}),
            # Empty flags after trailing slash
            ("/foo.*/", {"$regex": "foo.*"}),
            # Empty pattern
            ("//", {"$regex": ""}),
        ],
    )
    def test_valid_forms(self, value, expected):
        assert parse_regex(value) == expected

    @pytest.mark.parametrize(
        "value",
        [
            "/",             # no closing slash
            "///",           # ambiguous, doesn't match ^/.../$ pattern
            "not/a/regex",   # inner slash not in slash-delimited form
            " /no-match",    # leading space and bad format
        ],
    )
    def test_non_slashed_returns_whole_string_as_pattern(self, value):
        assert parse_regex(value) == {"$regex": value.strip()}

    def test_strips_outer_whitespace_only(self):
        assert parse_regex("   /foo bar/i   ") == {"$regex": "foo bar", "$options": "i"}

    def test_raises_filter_error_on_partially_invalid_flags(self):
        # "g" and "z" are not MongoDB flags — must raise, not silently drop them
        with pytest.raises(FilterError):
            parse_regex("/foo.*/gz")

    def test_raises_filter_error_on_all_invalid_flags(self):
        with pytest.raises(FilterError):
            parse_regex("/foo.*/abc")

    def test_uppercase_flags_treated_as_literal_pattern(self):
        # The flags group only accepts [a-z]*; uppercase causes no slash-match,
        # so the whole string is returned as a literal regex pattern.
        assert parse_regex("/foo/Imi") == {"$regex": "/foo/Imi"}
