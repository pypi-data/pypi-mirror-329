#!/usr/bin/env python3

import logging
from pathlib import Path

from markdownsausagemachine.sausage_man import IngredientPromise, SausageMan

logger = logging.getLogger(__name__)
logging.basicConfig(encoding="utf-8", level=logging.DEBUG)


def generate_example_two() -> None:
    example_mystery_meat = {
        "schema": "0.1",
        "documents": {
            "index": {
                "header": "Top-Level Header (Index)",
                "lede": "The root of the problems.",
                "sections": [
                    {
                        "header": "A Section Header",
                        "contents": [
                            {
                                "type": "paragraph",
                                "text": [
                                    "This is a standard paragraph section.",
                                    "Multiple lines can be passed in as an array.",
                                    "Allowing nicely formatted mystery meat.",
                                ],
                            },
                            {
                                "type": "unordered_list",
                                "items": [
                                    "Item 1: Hotdog",
                                    "Item 2: Cabbage",
                                    "Item 3: Broccoli",
                                ],
                            },
                            {
                                "type": "subsection",
                                "header": "A subsection",
                                "contents": [
                                    {
                                        "type": "paragraph",
                                        "text": ["A paragraph in a subsection."],
                                    }
                                ],
                            },
                        ],
                    }
                ],
            },
            "supplementary": {
                "header": "Top-Level Header (Supp)",
                "lede": "Additional problems.",
                "sections": [
                    {
                        "header": "A Section Header",
                        "contents": [
                            {
                                "type": "paragraph",
                                "text": [
                                    "This is a standard paragraph section.",
                                ],
                            },
                            {
                                "type": "ordered_list",
                                "items": [
                                    "Item 1: Random",
                                    "Item 2: Items",
                                    "Item 3: Are not hotdogs",
                                ],
                            },
                        ],
                    }
                ],
            },
        },
    }

    promises: list[IngredientPromise] = []

    my_sausage_man = SausageMan()
    my_sausage_man.give_ingredients(example_mystery_meat)
    my_sausage_man.give_promises(promises)
    promises_met = my_sausage_man.check_promises()
    if not promises_met:
        logger.error("Not all required promises were kept. Ingredients are not good!")

    output_dir = Path("./outputs/example2")
    output_dir.mkdir(parents=True, exist_ok=True)
    my_sausage_man.get_markdown_files(output_dir)
    logger.info("Done! Output created in: %s", output_dir)


if __name__ == "__main__":
    generate_example_two()
