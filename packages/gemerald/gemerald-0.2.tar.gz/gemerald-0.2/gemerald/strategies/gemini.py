from typing import override
from gemerald.formatter import ElementFormatter, FormattingStrategy
from gemerald.elements import MarkdownElement
import gemerald.line_elements as le


class Heading1(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"# {element.character_data()}"]


class Heading2(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"## {element.character_data()}"]


class Heading3(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"### {element.character_data()}"]


class Heading4(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"#### {element.character_data()}"]


class Heading5(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"##### {element.character_data()}"]


class Heading6(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"###### {element.character_data()}"]


class Quote(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"> {element.character_data()}", ""]


class PreformattedText(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [
            f"`{element.character_data()}`",
        ]


class Codeblock(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return ["```", f"{element.character_data()}", "```", ""]


class Text(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"{element.character_data()}"]


class Paragraph(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f" {element.character_data()}", ""]


class Link(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        assert isinstance(element, le.Link)
        return [f"=> {element.address} {element.character_data()}"]


class UnorderedList(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        assert isinstance(element, le.UnorderedList)
        return [f"* {it.character_data()}" for it in element.content]


class OrderedList(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        assert isinstance(element, le.OrderedList)
        return [f"{k}) {it.character_data()}" for k, it in enumerate(element.content)]


class GeminiStrategy(FormattingStrategy):

    format_extension = "gmi"
    skip_index_in_path = "index.gmi"

    formatters = {
        "Codeblock": Codeblock,
        "Quote": Quote,
        "Link": Link,
        "Bold": Text,
        "Italics": Text,
        "Paragraph": Paragraph,
        "OrderedList": OrderedList,
        "UnorderedList": UnorderedList,
        "HorizontalRule": Text,
        "Text": Text,
        "PreformattedText": PreformattedText,
        "Heading6": Heading6,
        "Heading5": Heading5,
        "Heading4": Heading4,
        "Heading3": Heading3,
        "Heading2": Heading2,
        "Heading1": Heading1,
    }
