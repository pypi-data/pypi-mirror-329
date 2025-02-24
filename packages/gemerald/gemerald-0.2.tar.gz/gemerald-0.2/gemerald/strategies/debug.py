from typing import override, Type
from gemerald.formatter import ElementFormatter, FormattingStrategy
from gemerald.elements import MarkdownElement


class Str(ElementFormatter):

    @override
    def format(self, element: MarkdownElement):
        return [str(element)]


class DebugStrategy(FormattingStrategy):

    format_extension = "debug"
    skip_index_in_path = None

    @override
    @classmethod
    def find_formatter(cls, element) -> Type[ElementFormatter]:
        _ = element
        return Str
