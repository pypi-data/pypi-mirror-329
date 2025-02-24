from typing import override, Type
from textwrap import wrap
from gemerald.formatter import ElementFormatter, FormattingStrategy
from gemerald.elements import MarkdownElement
from gemerald.line_elements import AbstractHeading, Heading1, Heading2


class TextFormatter(ElementFormatter):

    def wrap_lines_to_80(self, lines: list[str]) -> list[str]:
        wrapped = []
        for line in lines:
            wrapped += wrap(line, 80)
        wrapped += [""]
        return wrapped

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return self.wrap_lines_to_80(element.character_data())


class HeadingTextFormatter(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        assert isinstance(element, AbstractHeading)
        text = " ".join(element.character_data())

        if not isinstance(element, Heading1) and not isinstance(element, Heading2):
            return ["", text, ""]

        underline = "=" if isinstance(element, Heading1) else "-"

        return ["", text, underline * len(text), ""]


class PlaintextStrategy(FormattingStrategy):

    format_extension = "txt"
    skip_index_in_path = None

    @classmethod
    def find_formatter(cls, element) -> Type[ElementFormatter]:
        if isinstance(element, AbstractHeading):
            return HeadingTextFormatter
        return TextFormatter
