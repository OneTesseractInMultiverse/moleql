import pytest

from moleql.mql.errors import TextOperatorError
from moleql.mql.text_search_handler import TextSearchHandler


class TestTextSearchFilter:
    def test_with_valid_text_search_parameter(self):
        parameter: str = "$text=this is a full text search"
        expected: dict = {"$text": {"$search": "this is a full text search"}}
        actual: dict = TextSearchHandler(parameter).filter
        assert expected == actual

    def test_with_invalid_text_search_parameter(self):
        parameter: str = "$text="
        with pytest.raises(TextOperatorError):
            TextSearchHandler(parameter).filter
