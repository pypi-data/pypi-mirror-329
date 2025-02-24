from collections.abc import Callable
from typing import override, Iterable, Any
import os
import re
from gemerald.elements import InlineElement, MarkdownElement


def has_slash_before(text, x):
    return x != 0 and text[x - 1] == "\\"


def is_escaped(text, x):
    return has_slash_before(text, x) and not has_slash_before(text, x - 1)


def unescape(text: str) -> str:
    return text.replace(r"\`", "`").replace(r"\*", "*")


def find_unescaped(text: str, match: str) -> int:
    """
    Returns index of fist occurrance of `match` within `text`.
    -1 if not matched.
    """
    # This uses "negative lookbehind". Search this!
    indexes = iter(m.start() for m in re.finditer(rf"(?<!\\){re.escape(match)}", text))
    return next(indexes, -1)


def first(predicate: Callable, l: Iterable) -> Any:
    """
    Function takes list and returns first element that matches the predicate.
    Returns None if not found.
    """
    for ele in l:
        if predicate(ele):
            return ele
    return None


def md_line_to_ast(parent: MarkdownElement, line: str) -> list[InlineElement]:
    parsed_content: list[InlineElement] = []
    line = line.removesuffix(os.linesep)

    # Notice:
    # The order of elements in this list matters.
    line_elements = [PreformattedText, Bold, Italics]
    Fallback = Text

    x = 0
    previous_matched_end = 0
    while x < len(line):
        rest_of_the_line = line[x:]
        Matched = first(
            lambda E: rest_of_the_line.startswith(E.beginning_symbol)
            and not is_escaped(line, x),
            line_elements,
        )
        if Matched is not None:
            unparsed_by_any = line[previous_matched_end:x]
            if len(unparsed_by_any) > 0:
                parsed_content.append(Fallback(parent, unparsed_by_any))
            e = Matched(parent, rest_of_the_line)
            x += e.raw_len
            previous_matched_end = x
            parsed_content.append(e)
        else:
            x += 1

    unparsed_by_any = line[previous_matched_end:x]
    if len(unparsed_by_any) > 0:
        parsed_content.append(Fallback(parent, unparsed_by_any))
    return parsed_content


class PreformattedText(InlineElement):
    beginning_symbol = "`"

    @override
    def __init__(self, parent, content: str):
        _ = parent
        end = find_unescaped(content[1:], self.beginning_symbol)
        if end == -1:
            self.raw_len = len(content)
        else:
            end = end + 1 + len(self.beginning_symbol)
            self.raw_len = end
            content = content[:end]
        content = content.removeprefix("`")
        content = content.removesuffix("`")
        self.text = content

    @property
    @override
    def text_content(self) -> list[str]:
        return [self.text]


class DefaultBehaviourInlineElement(InlineElement):

    @override
    def __init__(self, parent, content: str):
        _ = parent
        self.text = unescape(self.reflow_whitespace(content))

    def reflow_whitespace(self, text: str) -> str:
        reflowed = " ".join(text.split())
        if text.startswith(" "):
            reflowed = " " + reflowed
        if text.endswith(" "):
            reflowed = reflowed + " "
        return reflowed

    @property
    @override
    def text_content(self) -> list[str]:
        return [self.text]


class Bold(DefaultBehaviourInlineElement):
    beginning_symbol = "**"

    def __init__(self, parent, content: str):
        end = find_unescaped(content[1:], self.beginning_symbol)
        if end == -1:
            self.raw_len = len(content)
        else:
            end = end + 1 + len(self.beginning_symbol)
            self.raw_len = end
            content = content[:end]
        content = content.removeprefix("**")
        content = content.removesuffix("**")
        super().__init__(parent, content)


class Italics(DefaultBehaviourInlineElement):
    beginning_symbol = "*"

    def __init__(self, parent, content: str):
        end = find_unescaped(content[1:], self.beginning_symbol)
        if end == -1:
            self.raw_len = len(content)
        else:
            end = end + 1 + len(self.beginning_symbol)
            self.raw_len = end
            content = content[:end]
        content = content.removeprefix("*")
        content = content.removesuffix("*")
        super().__init__(parent, content)


class Text(DefaultBehaviourInlineElement):
    beginning_symbol = None

    def __init__(self, parent, content: str):
        super().__init__(parent, content)
        self.raw_len = len(content)


class UnorderedPoint(DefaultBehaviourInlineElement):

    is_complex = True

    @override
    def __init__(self, parent, content: str):
        self.parent = parent
        self.content = md_line_to_ast(self, content)


class OrderedPoint(DefaultBehaviourInlineElement):

    is_complex = True

    @override
    def __init__(self, parent, content: str):
        self.parent = parent
        self.content = md_line_to_ast(self, content)
