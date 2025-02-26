from hamcrest import assert_that, not_none

from markdownsausagemachine.contents_list import UnorderedList


def test_unordered_list():
    items = ["1", "2", "3", "4", "5"]
    an_unordered_list = UnorderedList(items)
    markdown = an_unordered_list.get_markdown()
    assert_that(markdown, not_none)
