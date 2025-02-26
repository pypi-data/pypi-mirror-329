#!/usr/bin/env python3

import logging
from pathlib import Path

from markdownsausagemachine.contents import Paragraph, UnorderedList, CodeBlock
from markdownsausagemachine.sausage_machine import SausageMachine

logger = logging.getLogger(__name__)
logging.basicConfig(encoding="utf-8", level=logging.DEBUG)


def generate_example() -> None:
    logger.info("Generating example4...")

    my_sausage_machine = SausageMachine()
    index_doc = my_sausage_machine.add_document("coded-sausages")
    index_doc.set_header("Sausages in Code blocks")
    index_doc.set_lede("Sausages can also be coded.")
    new_section = index_doc.add_section("sausage-code")
    new_section.set_header("Sausage Code")
    new_section.add_content(Paragraph("Here is a representation of a code block:"))
    new_section.add_content(
        CodeBlock(
            "#!/bin/bash\n"
            "\n"
            "echo \"Hello Sausage!\""
        )
    )
    new_section.add_content(Paragraph("Here is a representation of a code block in a list:"))
    new_section.add_content(
        UnorderedList(
            [
                CodeBlock(
                    "Bratwurst is a traditional German sausage known for its mild and savory flavor. "
                    "It's typically made with pork, beef, or veal, and its name comes from the Old "
                    "High German word “brät,” meaning finely chopped meat, and “wurst,” meaning [...]"
                ),
            ]
        )
    )

    output_dir = Path("./outputs/example4")
    output_dir.mkdir(parents=True, exist_ok=True)
    my_sausage_machine.output_markdown_documents(output_dir)
    logger.info("Done! Output created in: %s", output_dir)


if __name__ == "__main__":
    generate_example()
