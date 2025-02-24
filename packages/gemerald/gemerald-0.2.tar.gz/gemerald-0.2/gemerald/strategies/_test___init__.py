from gemerald.strategies import find_strategy


from . import find_strategy


def test_stratefy_finding():
    assert find_strategy("txt").format_extension == "txt"
