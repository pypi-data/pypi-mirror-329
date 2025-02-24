
# Gemerald developer guide

## Main abstractions

 1. Elements
 2. Formatters
 3. Formatting strategies
 4. Navigators

### Element

It is an abstraction over part of Markdown file that can be separated.
An Element is a superclass of two classes: An InlineElement and LineElement.

LineElement is an Element that can hold inside other elements.
Inline elements are: bold, italics or preformatted text (inline version).
Line elements are cold blocks, lists, and paragraphs.

An Element must know how to detect itself given a raw part of markdown file.
For LineElements this will be a line.
For InlineElements, a string that doesn't exactly match any line of inputted markdown file.

LineElements detect themselves based on beginning symbol.
End is done the same way.

InlineElements have callback function that must be implemented which must return true or false.
End of InlineElement can be signified in different ways:
 - `is_single_line: bool`
 - `is_terminated_with_blank_line: bool`
 - `termination_sequence: str`
 - `termination_func: Callable[str] -> bool`

### Formatters

A formatter takes an Element and returns formatted content.
There is only one method this must implement: `format`.
It is given an `Element` as an input and has to output `list[str]` (a set of output lines).

### Formatting strategy

Strategy gathers a set of formatters along with apropriate logic to choose one for given Element.
Formatting strategies are representative of output formats: html, gmi, plaintext.

### Navigators

This is really most convoluted part of the code.
Navigator is an abstractrion over a set of files based on one root path.
File extensions are logically skipped.
Files are represented as only the relative path from the navigator root path (without root included).

Navigator is able to merge with another navigator.
In this case single reference can be assigned to 2 files: one from original navigator and one from
the merged.
Having a reference you can choose between files based on extension.

In project merging only happens between a navigator over a template directory and markdown
directory.
