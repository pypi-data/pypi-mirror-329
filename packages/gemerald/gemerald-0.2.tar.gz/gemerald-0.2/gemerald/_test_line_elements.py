from gemerald.line_elements import *


def test_HorizontalRule():
    test_pass = "----"
    test_fail = "--"
    assert HorizontalRule.could_begin_with(test_pass)
    assert not HorizontalRule.could_begin_with(test_fail)


def test_OrderedList():
    tests_pass = [
        " 1. d",
        " #. heh",
    ]
    tests_fail = [
        " 2. asd",
        " asd. ",
        " a. ",
        " 1) ",
        "1. ",
        " 1. ",
        " #. ",
    ]

    for test in tests_pass:
        assert OrderedList.could_begin_with(test)

    for test in tests_fail:
        assert not OrderedList.could_begin_with(test)


def test_UnorderedList():
    tests_pass = [
        " - a point",
        " - lol",
    ]

    tests_fail = [
        " * this is not a point",
    ]

    for test in tests_pass:
        assert UnorderedList.could_begin_with(test)

    for test in tests_fail:
        assert not UnorderedList.could_begin_with(test)


def test_Paragraph():
    test_pass = "lol"
    test_fail = "\t"
    assert Paragraph.could_begin_with(test_pass)
    assert not Paragraph.could_begin_with(test_fail)


def test_Heading3():
    tests_pass = [
        "### This is a heading",
        "### And this is also a heading ###",
    ]

    tests_fail = [
        "#### This is a heading of different level",
        "####This is missing a space",
    ]

    for test in tests_pass:
        assert Heading3.could_begin_with(test)

    for test in tests_fail:
        assert not Heading3.could_begin_with(test)


def test_Heading2_parse():
    h = Heading2(["## A heading ##"])
    assert len(h.content) == 1
    assert h.content[0].__class__.__name__ == "Text"

    # TODO
    # assert h.content[0].content == "A heading"


def test_HorizontalRule_parse():
    hr = HorizontalRule(["---"])
    assert len(hr.content) == 0


def test_UnorderedList_parse():
    ul = UnorderedList(
        [
            " - first point",
            " - second point",
        ]
    )

    assert len(ul.content) == 2
    assert ul.content[0].__class__.__name__ == "UnorderedPoint"
    assert ul.content[1].__class__.__name__ == "UnorderedPoint"
    # assert ul.content[0].text_content == ["first point"]
    # assert ul.content[1].text_content == ["second point"]


def test_UnorderedList_parse_complicated():
    ul = UnorderedList(
        [
            " - first point",
            "hehehehe",
            " - second point",
        ]
    )

    assert len(ul.content) == 2
    assert ul.content[0].__class__.__name__ == "UnorderedPoint"
    assert ul.content[1].__class__.__name__ == "UnorderedPoint"
    # assert ul.content[0].text_content == ["first point hehehehe"]
    # assert ul.content[1].text_content == ["second point"]


def test_OrderedList_parse():
    ol = OrderedList(
        [
            " 1. first point",
            " 2. second point",
            " 3. third point",
        ]
    )

    assert len(ol.content) == 3
    assert ol.content[0].__class__.__name__ == "OrderedPoint"
    assert ol.content[1].__class__.__name__ == "OrderedPoint"
    assert ol.content[2].__class__.__name__ == "OrderedPoint"
    # assert ol.content[0].text_content == ["first point"]
    # assert ol.content[1].text_content == ["second point"]
    # assert ol.content[1].text_content == ["second point"]


def test_OrderedList_parse_hashes():
    ol = OrderedList(
        [
            " #. first point",
            " #. second point",
            " #. third point",
        ]
    )

    assert len(ol.content) == 3
    assert ol.content[0].__class__.__name__ == "OrderedPoint"
    assert ol.content[1].__class__.__name__ == "OrderedPoint"
    assert ol.content[2].__class__.__name__ == "OrderedPoint"
    # assert ol.content[0].text_content == ["first point"]
    # assert ol.content[1].text_content == ["second point"]
    # assert ol.content[1].text_content == ["second point"]
