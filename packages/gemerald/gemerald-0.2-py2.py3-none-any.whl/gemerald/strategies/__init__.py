from gemerald.formatter import FormattingStrategy
from gemerald.strategies import debug, plaintext, html, gemini


class FormattingStrategyNotFoundException(Exception):
    pass


def get_all() -> list[type[FormattingStrategy]]:
    return [
        debug.DebugStrategy,
        plaintext.PlaintextStrategy,
        html.HTMLFormattingStrategy,
        gemini.GeminiStrategy,
    ]


def find_strategy(format_name: str) -> type[FormattingStrategy]:
    strategies = get_all()
    for st in strategies:
        if st.format_extension == format_name:
            return st
    raise FormattingStrategyNotFoundException
