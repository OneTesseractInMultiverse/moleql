import pytest

from moleql.mql.regex_parser import parse_regex


@pytest.mark.parametrize(
    "value, expected",
    [
        # Plain text, no slashes
        ("plain-text", {"$regex": "plain-text"}),
        ("  spaced  ", {"$regex": "spaced"}),  # leading/trailing spaces
        # Slash form, no flags
        ("/ab+c/", {"$regex": "ab+c"}),
        # Slash form with one allowed flag
        ("/ab+c/i", {"$regex": "ab+c", "$options": "i"}),
        # Slash form with multiple allowed flags
        ("/foo.*/ims", {"$regex": "foo.*", "$options": "ims"}),
        # Slash form with mixed allowed and disallowed flags
        # Only i,m,s,x should be kept
        ("/foo.*/imsyz", {"$regex": "foo.*", "$options": "ims"}),
        # Escaped slash inside pattern
        (r"/a\/b/x", {"$regex": r"a\/b", "$options": "x"}),
        # Empty flags after trailing slash
        ("/foo.*/", {"$regex": "foo.*"}),
        # Empty pattern ("//" is a valid match of the regex)
        ("//", {"$regex": ""}),
    ],
)
def test_parse_regex_valid_forms(value, expected):
    assert parse_regex(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        "/",  # no closing slash
        "///",  # ambiguous, but doesn't match the ^/.../$ pattern
        "not/a/regex",  # inner slash not in slash-delimited form
        " /no-match",  # leading space and bad format
    ],
)
def test_parse_regex_non_slashed_returns_whole_string(value):
    # For non-matching patterns, the whole stripped string
    # should be returned as the pattern.
    expected = {"$regex": value.strip()}
    assert parse_regex(value) == expected


def test_parse_regex_strips_outer_whitespace_only():
    # Outer spaces should be removed, but inner spaces kept
    value = "   /foo bar/i   "
    result = parse_regex(value)
    assert result == {"$regex": "foo bar", "$options": "i"}


def test_parse_regex_drops_all_flags_if_none_allowed():
    # All flags disallowed -> no $options key at all
    value = "/foo.*/abc"  # a,b,c are not in "imsx"
    result = parse_regex(value)
    assert result == {"$regex": "foo.*"}
    assert "$options" not in result


def test_parse_regex_uppercase_flags_make_value_literal():
    # Because the flags group only accepts [a-z]*,
    # any uppercase letters in the "flags" part cause the full
    # match to fail, and the whole string is treated as a literal
    # pattern instead of a slash-style regex.
    value = "/foo/Imi"
    result = parse_regex(value)
    assert result == {"$regex": "/foo/Imi"}
