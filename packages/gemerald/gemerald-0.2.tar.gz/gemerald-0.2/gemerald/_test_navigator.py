from pathlib import Path
from gemerald.navigator import DirectoryNavigator, MarkdownNavigator


class NavTest(DirectoryNavigator):
    pass


def test_directory_scan():
    nav = NavTest(Path("gemerald/test_navigator/test_files"))
    assert len(nav.files) == 3
    print(f"Contents: {[n for n in nav.files]}")
    for file in nav:
        print(file.relative_path)
    assert nav.get_file_by_relative("test_file_a.txt")
    assert nav.get_file_by_relative("test_file_b.txt")
    assert nav.get_file_by_relative("test_folder/test_file_c.txt")


def test_markdown_navigator():
    md = MarkdownNavigator(Path("gemerald/test_navigator/test_content"))
    assert len(md.files) == 3
    print(f"Contents: {[n for n in md.files]}")
    assert md.get_file_by_relative("test_file_a.md")
    assert md.get_file_by_relative("test_file_b.md")
    assert md.get_file_by_relative("test_folder/test_file_c.md")


def test_iterable():
    nav = NavTest(Path("gemerald/test_navigator/test_files"))
    files = [f for f in nav]
    assert len(files) == 3


def test_2_folders():
    nav_a = NavTest(Path("gemerald/test_navigator/test_2_folders/folder_a"))
    nav_b = NavTest(Path("gemerald/test_navigator/test_2_folders/folder_b"))

    files_a = [f for f in nav_a]
    files_b = [f for f in nav_b]

    assert len(files_a) == 2
    assert len(files_b) == 2

    file1a = files_a[0]
    file1b = files_b[0]
    file2a = files_a[1]
    file2b = files_b[1]

    assert file1a.relative_path == file1b.relative_path
    assert file2a.relative_path == file2b.relative_path
