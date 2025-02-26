#!/usr/bin/env python3

import logging
from pathlib import Path

from markdownsausagemachine.contents import OrderedList, Paragraph, UnorderedList
from markdownsausagemachine.sausage_machine import SausageMachine

logger = logging.getLogger(__name__)
logging.basicConfig(encoding="utf-8", level=logging.DEBUG)


def generate_example_one() -> None:
    logger.info("Generating example1...")

    my_sausage_machine = SausageMachine()
    index_doc = my_sausage_machine.add_document("index")
    index_doc.set_header("Index")
    index_doc.set_lede("A small document preamble.")
    new_section = index_doc.add_section("my-sausage-machine")
    new_section.set_header("My Sausage Machine")
    new_section.add_content(
        Paragraph("P1: How does a sausage machine become a reality")
    )
    new_section.add_content(
        Paragraph("P2: Going back to the start (a brief history of the world)")
    )
    new_section.add_content(
        UnorderedList(["A brief intro", "A confusing middle", "A well deserved end"])
    )
    new_section.add_content(Paragraph("P3: An ordered history of the world"))
    new_section.add_content(
        OrderedList(["A brief intro", "A confusing middle", "A well deserved end"])
    )

    supp_doc = my_sausage_machine.add_document("supplementary-words")
    supp_doc.set_header("Supplementary Words")
    new_section = supp_doc.add_section("my-sausage-machine")
    new_section.add_content(
        Paragraph("P1: Cat Dog Sheep\n\nDog Sheep Cat\n\nSheep Dog Cat")
    )
    new_section.add_content(Paragraph("P2: Up Down Left Right"))
    new_section.add_content(Paragraph("P3: Music Dance Sunshine"))

    output_dir = Path("./outputs/example1")
    output_dir.mkdir(parents=True, exist_ok=True)
    my_sausage_machine.output_markdown_documents(output_dir)
    logger.info("Done! Output created in: %s", output_dir)


if __name__ == "__main__":
    generate_example_one()
