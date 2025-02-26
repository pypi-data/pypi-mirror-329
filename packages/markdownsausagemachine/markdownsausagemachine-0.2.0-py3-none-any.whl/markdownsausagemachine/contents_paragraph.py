import textwrap

from markdownsausagemachine.document import SectionContent


class Paragraph(SectionContent):
    def __init__(self, text: str) -> None:
        self.contents: str = text
        self.initial_indent: str = ""
        self.subsequent_indent: str = ""
        self.wrap_width: int = 80

    def get_markdown(self) -> str:
        width = self.wrap_width - len(self.subsequent_indent)
        return textwrap.fill(
            self.contents,
            width=width,
            initial_indent=self.initial_indent,
            subsequent_indent=self.subsequent_indent,
            tabsize=4,
            break_long_words=False,
        )
