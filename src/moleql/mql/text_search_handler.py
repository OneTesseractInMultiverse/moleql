from moleql.mql.errors import TextOperatorError

TEXT_SEARCH_KEY: str = "$text"
TEXT_SEARCH_ALIAS: str = "text"
SEARCH_KEY: str = "$search"
KEY_VALUE_SEPARATOR: str = "="
SECOND_ELEMENT_INDEX: int = 1


def convert_with_text_operator(parameter: str):
    for key in (TEXT_SEARCH_KEY, TEXT_SEARCH_ALIAS):
        if parameter == f"{key}=":
            raise TextOperatorError()
        if parameter.startswith(f"{key}="):
            return parameter.split(KEY_VALUE_SEPARATOR, 1)[SECOND_ELEMENT_INDEX]
    raise TextOperatorError()


class TextSearchHandler:
    def __init__(self, text_search_parameter: str):
        self.parameter: str = text_search_parameter

    @property
    def filter(self) -> dict:
        return {TEXT_SEARCH_KEY: {SEARCH_KEY: convert_with_text_operator(self.parameter)}}
