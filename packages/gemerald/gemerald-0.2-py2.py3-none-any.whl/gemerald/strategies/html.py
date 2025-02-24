from typing import override
from gemerald.formatter import ElementFormatter, FormattingStrategy
from gemerald.elements import MarkdownElement
import gemerald.line_elements as le
import gemerald.inline_elements as ie


class Heading1(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"<h1>{element.character_data()}</h1>"]


class Heading2(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"<h2>{element.character_data()}</h2>"]


class Heading3(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"<h3>{element.character_data()}</h3>"]


class Heading4(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"<h4>{element.character_data()}</h4>"]


class Heading5(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"<h5>{element.character_data()}</h5>"]


class Heading6(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"<h6>{element.character_data()}</h6>"]


class Paragraph(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"<p>{element.character_data()}</p>"]


class Quote(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        strs = [
            "<figure>",
            f"<cite>{element.character_data()}</cite>",
        ]
        assert isinstance(element, le.Quote)
        if element.author is not None:
            strs.append(f"<figcaption>{element.author}</figcaption>")
        strs.append("</figure>")
        return strs


class Link(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        assert isinstance(element, le.Link)
        return [f"<a href={element.address}>{element.character_data()}</a><br/>"]


class Codeblock(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"<pre><code>{element.character_data()}</code></pre>"]


class Bold(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"<b>{element.character_data()}</b>"]


class Italics(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [f"<i>{element.character_data()}</i>"]


def format_list_elements(points):
    strs = []
    for point in points:
        assert isinstance(point, (le.OrderedPoint, le.UnorderedPoint))
        strs.append(f"<li>{point.character_data()}</li>")
    return strs


class UnorderedList(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        strs = ["<ul>"]
        assert isinstance(element, le.UnorderedList)
        strs += format_list_elements(element.content)
        strs.append("</ul>")
        return strs


class OrderedList(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        strs = ["<ol>"]
        assert isinstance(element, le.OrderedList)
        strs += format_list_elements(element.content)
        strs.append("</ol>")
        return strs


class HorizontalRule(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        _ = element
        return ["<hr>"]


class Text(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        assert isinstance(element, ie.Text)
        return element.character_data()


class PreformattedText(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        assert isinstance(element, ie.PreformattedText)
        return element.character_data()


class HTMLFormattingStrategy(FormattingStrategy):

    format_extension = "html"
    skip_index_in_path = "index.html"

    formatters = {
        "Heading1": Heading1,
        "Heading2": Heading2,
        "Heading3": Heading3,
        "Heading4": Heading4,
        "Heading5": Heading5,
        "Heading6": Heading6,
        "Quote": Quote,
        "Link": Link,
        "Codeblock": Codeblock,
        "Bold": Bold,
        "Italics": Italics,
        "Paragraph": Paragraph,
        "UnorderedList": UnorderedList,
        "OrderedList": OrderedList,
        "HorizontalRule": HorizontalRule,
        "Text": Text,
        "PreformattedText": PreformattedText,
    }
