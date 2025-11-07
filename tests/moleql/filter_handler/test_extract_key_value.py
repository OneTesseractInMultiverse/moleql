from moleql.mql.constants import EMPTY_STRING
from moleql.mql.filter_handler import FilterHandler


class TestExtractKeyValue:
    def test_key_extraction(self):
        expected: str = "key1"
        actual: str = FilterHandler(filter_parameter="key1>1", custom_casters=None).key
        assert expected == actual

    def test_key_extraction_when_no_key(self):
        expected: str = EMPTY_STRING
        actual: str = FilterHandler(filter_parameter="value", custom_casters=None).key
        assert expected == actual

    def test_value_extraction(self):
        expected: str = "1"
        actual: str = FilterHandler(filter_parameter="key1>1", custom_casters=None).value
        assert expected == actual

    def test_operator_extraction(self):
        expected: str = ">"
        actual: str = FilterHandler(filter_parameter="key1>1", custom_casters=None).operator
        assert expected == actual
