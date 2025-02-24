from gemerald.markdown_file import Context, Siblings, MarkdownFile
from datetime import date, datetime
from jinja2 import Template


def test_set_sibling():
    pass


def test_get_path_changed_extension():
    pass


def test_setting_formatter():
    pass


def test_templating():
    md = MarkdownFile(path="fakepath", contents=[])
    md.ctx.set_content("content")
    md.ctx.dateReleased = date(2024, 1, 1)
    md.ctx.title = "title"

    template = Template(
        "site: {{ Site.content }}"
        "site: {{ Ctx.site.content }}"
        "dateReleased: {{ Ctx.dateReleased }}"
        "title: {{ Ctx.title }}"
    )
    correct = "site: content" "site: content" "dateReleased: 2024-01-01" "title: title"

    assert md.template(template) == correct


def test_detecting_header():

    text = "this line should be untouched"
    headers = [
        {
            "dateReleased": datetime.now(),
            "title": "sampletitle",
            "len": 3,
            "lines": ["---", "title: sampletitle", "---"],
        },
        {
            "dateReleased": date(2024, 1, 1),
            "title": "sampletitle",
            "len": 4,
            "lines": ["---", "title: sampletitle", "dateReleased: 2024-01-01", "---"],
        },
        {
            "dateReleased": datetime.now(),
            "title": "No title",
            "len": 2,
            "lines": ["---", "---"],
        },
        {
            "dateReleased": datetime.now(),
            "title": "No title",
            "len": 0,
            "lines": [
                "---",
            ],
        },
    ]

    for header in headers:
        test_text = header["lines"]
        test_text += [text]

        title, date_released, len = MarkdownFile.detect_header(test_text)

        assert title == header["title"]
        # assert date_released.ctime() == header["dateReleased"].ctime()
        assert len == header["len"]


def test_sibling_sorting():

    class MarkdownFileMock:
        def __init__(self, id, date_released):
            self.ctx = Context()
            self.id = id
            self.ctx.dateReleased = date_released

    files = [
        MarkdownFileMock(0, date(2023, 1, 1)),
        MarkdownFileMock(1, date(2023, 3, 1)),
        MarkdownFileMock(2, date(2023, 2, 1)),
        MarkdownFileMock(3, date(2023, 7, 1)),
        MarkdownFileMock(4, date(2023, 9, 1)),
        MarkdownFileMock(5, date(2023, 8, 1)),
    ]

    correct_by_date = [4, 5, 3, 1, 2, 0]
    correct = [0, 1, 2, 3, 4, 5]
    siblings = Siblings(files)

    for i, f in enumerate(siblings):
        assert f.id == correct[i]

    for i, f in enumerate(siblings.by_date()):
        assert f.id == correct_by_date[i]
