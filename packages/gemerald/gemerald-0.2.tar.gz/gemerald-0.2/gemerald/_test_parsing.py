from gemerald.line_elements import md_lines_to_ast


def test_parsing():
    parsed = md_lines_to_ast(
        [
            "line1 of a paragraph",
            "line2 of a paragraph",
            "",
            "---",
            "",
            "# A heading #",
            "",
            "line1 of a paragraph",
            "line2 of a paragraph",
        ]
    )

    assert len(parsed) == 4
    assert parsed[0].__class__.__name__ == "Paragraph"
    assert parsed[1].__class__.__name__ == "HorizontalRule"
    assert parsed[2].__class__.__name__ == "Heading1"
    assert parsed[3].__class__.__name__ == "Paragraph"
