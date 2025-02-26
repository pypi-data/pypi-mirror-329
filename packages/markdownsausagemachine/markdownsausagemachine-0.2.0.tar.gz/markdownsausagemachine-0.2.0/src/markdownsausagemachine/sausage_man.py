import logging
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any

from markdownsausagemachine.contents import OrderedList, Paragraph, UnorderedList
from markdownsausagemachine.document import Document, DocumentSection
from markdownsausagemachine.sausage_machine import SausageMachine
from markdownsausagemachine.version import MYSTERY_MEAT_SCHEMA_VERSION

logger = logging.getLogger(__name__)


class UnmetPromise(ValueError):
    """Error class for handling unmet promises when calling check_promise()"""


class IngredientPromise:
    def __init__(self, desc: str, callback: Callable[[dict[str, Any]], bool]) -> None:
        self.desc: str = desc
        self.callback: Callable[[dict[str, Any]], bool] = callback

    def check_promise(self, ingredients: dict[str, Any]) -> None:
        promise_met = self.callback(ingredients)
        if not promise_met:
            raise UnmetPromise()


class SausageMan:
    """Convenience interface for the sausage machine"""

    def __init__(self) -> None:
        self.sausage_machine: SausageMachine = SausageMachine()
        self.promises: list[IngredientPromise] = []
        self.ingredients: dict[str, Any] = {}

    def _process_content(self, section: DocumentSection, data: dict[str, Any]) -> None:
        content_type = data.get("type")
        if content_type == "subsection":
            subsection_header = data.get("header", "")
            subsection_contents = data.get("contents", [])
            subsection = section.add_subsection(subsection_header)
            for content in subsection_contents:
                self._process_content(subsection, content)
        elif content_type == "paragraph":
            text = " ".join(data.get("text", []))
            content = Paragraph(text)
            section.add_content(content)
        elif content_type == "unordered_list":
            items = data.get("items", [])
            content = UnorderedList(items)
            section.add_content(content)
        elif content_type == "ordered_list":
            items = data.get("items", [])
            content = OrderedList(items)
            section.add_content(content)
        else:
            raise ValueError(f"Unrecognised content type: {content_type}")

    def _process_section(self, doc: Document, data: dict[str, Any]) -> None:
        section_header = data.get("header", "")
        section = doc.add_section(section_header)
        contents = data.get("contents", [])
        for content in contents:
            self._process_content(section, content)

    def _process_doc(self, filename: str, data: dict[str, Any]) -> None:
        doc = self.sausage_machine.add_document(filename)
        doc.set_header(data.get("header", ""))
        doc.set_lede(data.get("lede", ""))
        for section in data.get("sections", []):
            self._process_section(doc, section)

    def _process_ingredients(self) -> None:
        documents = self.ingredients.get("documents", {})
        for doc_filename, doc_data in documents.items():
            self._process_doc(doc_filename, doc_data)

    def give_ingredients(self, ingredients: dict[str, Any]) -> None:
        if not isinstance(ingredients, dict):
            raise RuntimeError("Ingredients must be a dict type.")

        schema_version = ingredients.get("schema")
        if not schema_version == MYSTERY_MEAT_SCHEMA_VERSION:
            raise RuntimeError(
                f"Invalid mystery meat schema version: {schema_version}. Expecting: {MYSTERY_MEAT_SCHEMA_VERSION}."
            )

        self.ingredients = ingredients
        self._process_ingredients()

    def give_promises(self, promises: Iterable[IngredientPromise]) -> None:
        self.promises.extend(promises)

    def check_promises(self) -> bool:
        result = True
        for promise in self.promises:
            try:
                promise.check_promise(self.ingredients)
            except UnmetPromise:
                logger.info("Unmet promise: %s", promise.desc)
                result = False
        return result

    def get_markdown_files(self, output_dir: Path) -> None:
        self.sausage_machine.output_markdown_documents(output_dir)
