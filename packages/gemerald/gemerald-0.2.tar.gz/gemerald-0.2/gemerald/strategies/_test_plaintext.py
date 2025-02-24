from gemerald.strategies.plaintext import PlaintextStrategy
from gemerald.markdown_file import MarkdownFile
from pprint import pprint


md = """

# Hi! this is a test file in markdown #




This should output as a paragraph.
And all lines should be wrapped.
And text properly reflowed.
Hehehe.

This is another paragraph.
Here also all lines should be wrapped to 80 characters and text properly reflowed.
This will probably fail.
Not that I'm suggesting something.


## And here is another heading
"""

txt = """
Hi! this is a test file in markdown
===================================

This should output as a paragraph. And all lines should be wrapped. And text
properly reflowed. Hehehe.

This is another paragraph. Here also all lines should be wrapped to 80
characters and text properly reflowed. This will probably fail. Not that I'm
suggesting something.


And here is another heading
---------------------------
"""


# def test_plaintextFormatting():
#    strategy = PlaintextStrategy()
#    mdf = MarkdownFile("fake", contents=md.split("\n"))
#    output = "\n".join(mdf.into(strategy))
#
#    assert len(mdf.parsed) == 4
#    pprint(mdf.parsed)
#    pprint(mdf.parsed[1])
#    print(
#        "                                                                      >> Output"
#    )
#    print(output)
#    print(
#        "                                                                      >> Wanted"
#    )
#    print(txt)
#    assert output == txt
