from abc import abstractmethod
from collections.abc import Collection

from markdownsausagemachine.contents_paragraph import Paragraph
from markdownsausagemachine.contents_codeblock import CodeBlock
from markdownsausagemachine.document import SectionContent

type ListItem = str | Paragraph | CodeBlock


class MarkdownList(SectionContent):
    """Shared abstraction for list classes"""

    def __init__(self, items: Collection[ListItem]) -> None:
        self.items = items
        self.nesting_level = 0

    @abstractmethod
    def get_initial_indent(self, item_no: int) -> str: ...

    def get_markdown(self) -> str:
        markdown = ""
        for i, item in enumerate(self.items):
            initial_indent = self.get_initial_indent(i)
            if isinstance(item, str):
                item = Paragraph(item)
                item.initial_indent = initial_indent
                item.subsequent_indent = f"{' '*len(item.initial_indent)}"
                markdown += item.get_markdown()
            elif isinstance(item, Paragraph):
                item.initial_indent = initial_indent
                item.subsequent_indent = f"{' '*len(item.initial_indent)}"
                markdown += item.get_markdown()
            elif isinstance(item, CodeBlock):
                item.initial_indent = initial_indent
                item.subsequent_indent = f"{' '*len(item.initial_indent)}"
                markdown += item.get_markdown()
            else:
                raise ValueError(f"Unsupported list item type: {type(item)}")
            # Add some separation between items
            if i != len(self.items) - 1:
                markdown += "\n"
        return markdown


class UnorderedList(MarkdownList):
    def get_initial_indent(self, item_no: int) -> str:
        return f"{' '*(self.nesting_level*4)}*   "


class OrderedList(MarkdownList):
    def get_initial_indent(self, item_no: int) -> str:
        return f"{' '*(self.nesting_level*4)}{item_no+1}.  "
