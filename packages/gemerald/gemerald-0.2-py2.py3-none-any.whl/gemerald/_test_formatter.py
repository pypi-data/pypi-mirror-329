from typing import override
from gemerald.elements import LineElement, MarkdownElement
from gemerald.formatter import FormattingStrategy, ElementFormatter


# 1. We define an Element
class SampleElement(LineElement):
    is_single_line = True

    @override
    def __init__(self, content):
        _ = content

    @staticmethod
    def could_begin_with(line) -> bool:
        _ = line
        return True


# 2. We create a formatting strategy for that element
class SampleFormattingStrategy(FormattingStrategy):

    class SampleElementFormatter(ElementFormatter):
        def format(self, element: MarkdownElement) -> list[str]:
            assert isinstance(element, SampleElement)
            return [f"{element.__class__.__name__}"]

    formatters = {  # we need to define it after class definitions
        "SampleElement": SampleElementFormatter,
    }


# 3. We try to fromat an instance of that element with that strategy
def test_elementFormatting():
    strategy = SampleFormattingStrategy()
    element = SampleElement([])
    formatter = strategy.find_formatter(element)()
    formatted = formatter.format(element)

    assert len(formatted) == 1
    assert formatted[0] == "SampleElement"
