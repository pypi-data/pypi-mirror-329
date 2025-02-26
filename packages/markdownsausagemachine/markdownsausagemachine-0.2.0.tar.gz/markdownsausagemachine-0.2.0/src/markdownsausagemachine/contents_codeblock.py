import textwrap

from markdownsausagemachine.document import SectionContent


class CodeBlock(SectionContent):
    def __init__(self, text: str) -> None:
        self.contents: str = text
        self.initial_indent: str = ""
        self.subsequent_indent: str = ""

    def get_markdown(self) -> str:
        markdown = f"{self.initial_indent}```\n"
        for line in self.contents.split("\n"):
            markdown += f"{self.subsequent_indent}{line}\n"
        markdown += f"{self.subsequent_indent}```"
        return markdown
