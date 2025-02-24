from typing import override
from gemerald.elements import LineElement, ParseException
from gemerald.inline_elements import (
    md_line_to_ast,
    Text,
    UnorderedPoint,
    OrderedPoint,
    PreformattedText,
)
from abc import ABC
import re


def md_lines_to_ast(lines):
    debug = False
    if lines == [
        "---\n",
        "title: Two\n",
        "---\n",
        "This is second file for the blog\n",
    ]:
        debug = True
    lines = lines + [""]
    parsed_content: list[LineElement] = []

    # Notice:
    # The order of elements in this list matters.
    # Particularly for Paragraph that can begin with anything.
    # So it is important to check if given text can be anything
    # besides Paragraph before we say it is just text.
    line_elements = [
        Heading1,
        Heading2,
        Heading3,
        Heading4,
        Heading5,
        Heading6,
        Link,
        Quote,
        Codeblock,
        OrderedList,
        UnorderedList,
        HorizontalRule,
        Paragraph,
    ]

    x = 0
    while x < len(lines):
        next_line = lines[x]

        if next_line.strip() == "":
            x += 1
            continue

        for Element in line_elements:

            if Element.could_begin_with(next_line):
                lines_in_element = [next_line]
                x += 1
                next_line = lines[x]

                while not is_terminated(next_line, Element):
                    lines_in_element.append(next_line)
                    x += 1
                    if x >= len(lines):
                        break
                    next_line = lines[x]

                if Element.is_greedy:
                    lines_in_element.append(next_line)
                    x += 1
                    next_line = lines[x]

                parsed_content.append(Element(lines_in_element))
                break
    if debug:
        print(parsed_content)
    return parsed_content


class AbstractHeading(LineElement, ABC):
    """
    A generalization of all headings
    """

    is_single_line = True
    is_terminated_with_blank_line = True
    termination_sequence = None
    termination_func = None

    def __init__(self, lines: list[str], heading_level: int):
        if len(lines) != 1:
            raise ParseException("You tried to parse more than one line as a heading")

        text = lines[0].strip()
        text = text[heading_level + 1 :]
        text = text.removesuffix(" " + "#" * heading_level)
        self.content = [Text(parent=self, content=text)]


class Heading1(AbstractHeading):

    @override
    @staticmethod
    def could_begin_with(line: str) -> bool:
        return line.startswith("#" * 1 + " ")

    @override
    def __init__(self, lines: list[str]):
        super().__init__(lines, 1)


class Heading2(AbstractHeading):

    @override
    @staticmethod
    def could_begin_with(line: str) -> bool:
        return line.startswith("#" * 2 + " ")

    @override
    def __init__(self, lines: list[str]):
        super().__init__(lines, 2)


class Heading3(AbstractHeading):

    @override
    @staticmethod
    def could_begin_with(line: str) -> bool:
        return line.startswith("#" * 3 + " ")

    @override
    def __init__(self, lines: list[str]):
        super().__init__(lines, 3)


class Heading4(AbstractHeading):

    @override
    @staticmethod
    def could_begin_with(line: str) -> bool:
        return line.startswith("#" * 4 + " ")

    @override
    def __init__(self, lines: list[str]):
        super().__init__(lines, 4)


class Heading5(AbstractHeading):

    @override
    @staticmethod
    def could_begin_with(line: str) -> bool:
        return line.startswith("#" * 5 + " ")

    @override
    def __init__(self, lines: list[str]):
        super().__init__(lines, 5)


class Heading6(AbstractHeading):

    @override
    @staticmethod
    def could_begin_with(line: str) -> bool:
        return line.startswith("#" * 6 + " ")

    @override
    def __init__(self, lines: list[str]):
        super().__init__(lines, 6)


class Quote(LineElement):

    is_single_line = False
    is_terminated_with_blank_line = False
    termination_sequence = None

    @override
    @staticmethod
    def termination_func(line):
        return not Quote.could_begin_with(line) and not Quote.is_author_line(line)

    @override
    @staticmethod
    def could_begin_with(line: str) -> bool:
        strip = line.strip()
        return len(strip) != 0 and strip[0] == ">"

    @staticmethod
    def is_author_line(line: str) -> bool:
        strip = line.strip()
        return len(strip) != 0 and strip[0] == "~"

    def __init__(self, lines: list[str]):
        self.author = None
        quote_lines = []

        lines = [line.strip() for line in lines]
        for line in lines:
            if line[0] == ">":
                quote_lines.append(line[1:])
            elif line[0] == "~":
                self.author = line[1:]

        self.content = md_lines_to_ast(quote_lines)


class Paragraph(LineElement):

    is_single_line = False
    is_terminated_with_blank_line = True
    termination_sequence = None
    termination_func = None

    @override
    @staticmethod
    def could_begin_with(line: str) -> bool:
        return line.strip() != ""

    def __init__(self, lines: list[str]):
        self.content = md_line_to_ast(self, "\n".join(lines))  # pyright: ignore


class Link(LineElement):

    is_single_line = True
    is_terminated_with_blank_line = False
    termination_sequence = None
    termination_func = None

    def get_elements(self, link: str):
        link = link.strip()
        link = link[1:]  # remove front bracket
        link = link[:-1]  # remove end bracket
        separation_point = link.index("](")
        link_text = link[:separation_point]
        link_address = link[separation_point + 2 :]
        return link_text, link_address

    @override
    @staticmethod
    def could_begin_with(line: str) -> bool:
        regex = "^\\[.+\\]\\(.+\\)$"
        return re.search(regex, line.strip()) is not None

    def __init__(self, lines: list[str]):
        text, addr = self.get_elements(lines[0])
        self.address = addr
        self.content = [Text(self, text)]


class Codeblock(LineElement):

    is_greedy = True
    is_single_line = False
    is_terminated_with_blank_line = False
    termination_sequence = "```"
    termination_func = None

    @override
    @staticmethod
    def could_begin_with(line: str) -> bool:
        return line.startswith("```")

    def __init__(self, lines: list[str]):
        lines = lines[1:]
        lines = lines[:-1]
        self.content = [PreformattedText(self, "\n".join(lines))]


class UnorderedList(LineElement):

    is_single_line = False
    is_terminated_with_blank_line = True
    termination_sequence = None
    termination_func = None

    @staticmethod
    def _is_a_point_(line: str) -> bool:
        return line.strip().startswith("- ") and line.startswith(" ")

    @staticmethod
    def _strip_point_marker_(line: str) -> str:
        return line[line.index("- ") + 2 :]

    @override
    @staticmethod
    def could_begin_with(line: str) -> bool:
        return UnorderedList._is_a_point_(line)

    def __init__(self, lines: list[str]):
        points: list[list[str]] = []

        current_point: list[str] = []
        for line in lines:
            if self._is_a_point_(line):
                points.append(current_point)
                current_point = []
                current_point.append(self._strip_point_marker_(line))
            else:
                current_point.append(line)

        points.append(current_point)
        points = points[1:]

        point_texts: list[str] = ["\n".join(point) for point in points]
        self.content = [UnorderedPoint(self, p) for p in point_texts]


class OrderedList(LineElement):

    is_single_line = False
    is_terminated_with_blank_line = True
    termination_sequence = None
    termination_func = None

    @override
    @staticmethod
    def could_begin_with(line: str) -> bool:
        return OrderedList._is_a_point_(line)

    @staticmethod
    def _is_a_hashpoint_(line: str):
        return line.startswith(" ") and line.strip().startswith("#. ")

    @staticmethod
    def _is_a_numberpoint_(number: int, line: str):
        return line.startswith(" ") and line.strip().startswith(f"{number}. ")

    @staticmethod
    def _is_a_point_(line: str) -> bool:
        return OrderedList._is_a_hashpoint_(line) or OrderedList._is_a_numberpoint_(
            1, line
        )

    @staticmethod
    def _strip_point_marker_(line: str) -> str:
        number_of_spaces = 0
        for i in range(100):
            if line[i] == " ":
                number_of_spaces = i
            else:
                break

        return line[number_of_spaces + 4 :]

    def _is_point_correct_type_(self, number: int, line: str):
        if self.numbered_list:
            return self._is_a_numberpoint_(number, line)
        return self._is_a_hashpoint_(line)

    @staticmethod
    def _measure_indentation_(point: str) -> int:
        for index, value in enumerate(point):
            if not value.isspace():
                return index
        raise ValueError("This should never happen")

    @staticmethod
    def _is_correct_indentation_(line: str, indentation: int) -> bool:
        return not line[indentation].isspace() and line[indentation - 1].isspace()

    @override
    def __init__(self, lines):
        points: list[list[str]] = []
        current_point: list[str] = []
        indentation = self._measure_indentation_(lines[0])

        if self._is_a_numberpoint_(1, lines[0]):
            self.numbered_list = True
        else:
            self.numbered_list = False

        point_num = 1
        for line in lines:
            if self._is_point_correct_type_(
                point_num, line
            ) and self._is_correct_indentation_(line, indentation):
                points.append(current_point)
                current_point = []
                current_point.append(self._strip_point_marker_(line))
                point_num += 1
            else:
                current_point.append(line)

        points.append(current_point)
        points = points[1:]

        point_texts: list[str] = ["\n".join(point) for point in points]
        self.content = [OrderedPoint(self, p) for p in point_texts]


class HorizontalRule(LineElement):

    is_single_line = True
    is_terminated_with_blank_line = True
    termination_sequence = None
    termination_func = None

    @override
    @staticmethod
    def could_begin_with(line: str) -> bool:
        stripped = line.strip()
        for i in range(3, 100):
            if stripped == "-" * i:
                return True
        return False

    def __init__(self, _: list[str]):
        self.content = []


def is_terminated(next_line, Element) -> bool:
    if Element.is_single_line:
        return True

    if Element.is_terminated_with_blank_line:
        return next_line.strip() == ""

    if Element.termination_sequence is not None:
        return next_line.strip() == Element.termination_sequence

    if Element.termination_func is not None:
        return Element.termination_func(next_line)

    raise ParseException(f"Could not find termination point of element: {str(Element)}")
