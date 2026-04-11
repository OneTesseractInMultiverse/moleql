import re

from moleql.mql.errors import FilterError

_SLASHED_RE = re.compile(
    r"""
    ^/
    (?P<pattern>(?:\\.|[^/])*)   # allow escaped slashes like \/
    /
    (?P<flags>[a-z]*)?           # optional flags (letters only)
    $
    """,
    re.VERBOSE,
)

# MongoDB-supported inline flags commonly encountered
_ALLOWED_FLAGS = frozenset("imsx")  # i=ignorecase, m=multiline, s=dotall, x=verbose
_INVALID_FLAG_ERROR: str = "Unrecognized regex flags: {flags!r}"


def _extract_slashed_parts(value: str) -> tuple[str, str] | None:
    """Computation: parses slash-delimited form into (pattern, flags) or None.

    Expects the value to already be stripped of surrounding whitespace.
    """
    m = _SLASHED_RE.fullmatch(value)
    if not m:
        return None
    return m.group("pattern"), m.group("flags") or ""


def _validate_regex_flags(flags_raw: str) -> None:
    """Computation: raises FilterError if flags_raw contains unrecognized characters."""
    invalid = "".join(ch for ch in flags_raw if ch not in _ALLOWED_FLAGS)
    if invalid:
        raise FilterError(_INVALID_FLAG_ERROR.format(flags=invalid))


def _build_regex_dict(pattern: str, flags: str) -> dict[str, str]:
    """Computation: assembles a MongoDB regex query dict."""
    out: dict[str, str] = {"$regex": pattern}
    if flags:
        out["$options"] = flags
    return out


def parse_regex(value: str) -> dict[str, str]:
    """Coordinator: converts a regex string into a MongoDB regex query dict.

    Examples:
        '/ab+c/i'      -> {'$regex': 'ab+c', '$options': 'i'}
        '/a\\/b/x'     -> {'$regex': 'a\\/b', '$options': 'x'}
        'plain-text'   -> {'$regex': 'plain-text'}

    Args:
        value: The user-supplied regex string.

    Returns:
        A dict suitable for MongoDB queries, e.g.
        {'$regex': '<pattern>', '$options': '<flags>'}.

    Raises:
        FilterError: If the slash-delimited form contains unrecognized flags.
    """
    stripped = value.strip()
    parts = _extract_slashed_parts(stripped)
    if parts is None:
        return _build_regex_dict(stripped, "")
    pattern, flags_raw = parts
    _validate_regex_flags(flags_raw)
    return _build_regex_dict(pattern, flags_raw)
