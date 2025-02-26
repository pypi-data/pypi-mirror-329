import logging
from pathlib import Path

from markdownsausagemachine.document import Document

logger = logging.getLogger(__name__)


class SausageMachine:
    """The sausauge machine"""

    def __init__(self) -> None:
        self.documents: dict[str, Document] = {}

    def flush_machine(self) -> None:
        """Reset sausage machine to initial state"""
        self.documents = {}

    def add_document(self, filename: str) -> Document:
        new_document = Document(filename)
        self.documents[filename] = new_document
        return new_document

    def output_markdown_documents(self, directory: Path) -> None:
        directory.mkdir(parents=True, exist_ok=True)
        for document in self.documents.values():
            output_file = directory / f"{document.filename}.md"
            logger.info("Generating file: %s", output_file)
            markdown = document.get_markdown()
            with output_file.open("w") as f:
                f.write(markdown)
            logger.info("Done.")
        # TODO: Use pymarkdown to lint the outputted files
