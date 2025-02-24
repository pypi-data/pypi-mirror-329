from datetime import datetime, date
from typing import Any
from gemerald.formatter import FormattingStrategy
from gemerald.line_elements import md_lines_to_ast
from pathlib import Path
from sys import stderr
from jinja2 import Template


class MarkdownFile:

    def __init__(self, path: str, contents: list[str]):
        self.path = path
        self.ctx = Context()
        title, dateReleased, header_len = self.detect_header(contents)
        self.ctx.dateReleased = dateReleased
        self.ctx.title = title
        self.parsed = md_lines_to_ast(contents[header_len:])

    def set_siblings(self, siblings):
        self.ctx.siblings = Siblings(siblings)

    def get_path_changed_extension(self, extension: str) -> Path:
        p = Path(self.path)
        return p.with_suffix(f".{extension}")

    def set_formatter(self, Strategy: type[FormattingStrategy]):

        # set content
        strategy = Strategy()
        lines = []
        for element in self.parsed:
            formatter = strategy.find_formatter(element)()
            formatted = formatter.format(element)
            lines += formatted
        self.ctx.set_content("\n".join(lines))

        # set correct href
        path = self.get_path_changed_extension(Strategy.format_extension)
        self.ctx.href = f"/{path}"
        skip = Strategy.skip_index_in_path
        if skip is not None:
            if self.ctx.href.endswith(skip):
                self.ctx.href = self.ctx.href[: -len(skip)]

    def template(self, template: Template) -> str:
        try:
            return template.render({"Ctx": self.ctx, "Site": self.ctx.site})
        except Exception:
            print(
                f"Error occured while processing template {template.filename}",
                file=stderr,
            )
            raise

    @staticmethod
    def detect_header(lines: list[str]) -> tuple[str, date, int]:
        if not (len(lines) > 0 and lines[0].strip() == "---"):
            return "No title", datetime.now(), 0

        header_content_len = 0
        header_exists = False
        for x in range(1, minimum(4, len(lines))):
            if lines[x].strip() == "---":
                header_exists = True
                header_content_len = x - 1

        if not header_exists:
            return "No title", datetime.now(), 0

        if header_content_len == 0:
            return "No title", datetime.now(), 2

        header = {}
        for x in range(1, 1 + header_content_len):
            split = lines[x].split(":")
            header[split[0]] = ":".join(split[1:]).strip()

        dateReleased = datetime.fromisoformat(
            header.get("dateReleased", datetime.now().isoformat())
        )
        return header.get("title", "No title"), dateReleased, header_content_len + 2


class Siblings:

    def __init__(self, siblings: list):
        self.s = siblings

    def __iter__(self):
        return iter(self.s)

    def by_date(self) -> list:
        return sorted(self.s, key=lambda md: md.ctx.dateReleased, reverse=True)


class Context:

    site: dict[str, str]
    href: str
    siblings: Siblings
    title: str
    dateReleased: date
    utils: dict[str, Any]

    def __init__(self):
        self.site = {}
        self.utils = {
            "now": datetime.now(),
        }

    def set_content(self, content: str):
        self.site["content"] = content


def minimum(a, b):
    if a <= b:
        return a
    return b
