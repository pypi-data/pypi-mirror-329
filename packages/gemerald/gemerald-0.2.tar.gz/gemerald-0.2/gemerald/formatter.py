from abc import ABC, abstractmethod
from typing import override, Type, Optional
from gemerald.elements import MarkdownElement


class ElementFormatter(ABC):

    @abstractmethod
    def format(self, element: MarkdownElement) -> list[str]:
        pass


class FallbackFormatter(ElementFormatter):

    @override
    def format(self, element: MarkdownElement) -> list[str]:
        return [str(element)]


class FormattingStrategy(ABC):

    # What you need to do is to override this field
    formatters: dict[str, Type[ElementFormatter]] = {}

    # Don't forget to override format extension
    format_extension = "abstract"
    skip_index_in_path: Optional[str] = "index.abstract"

    @classmethod
    def find_formatter(cls, element) -> Type[ElementFormatter]:
        return cls.formatters.get(element.__class__.__name__) or FallbackFormatter
