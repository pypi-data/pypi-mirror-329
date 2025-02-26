#!/usr/bin/env python3

import logging
from typing import Any

from markdownsausagemachine.sausage_man import IngredientPromise, SausageMan

logger = logging.getLogger(__name__)
logging.basicConfig(encoding="utf-8", level=logging.DEBUG)


def show_unmet_promise() -> None:
    example_mystery_meat = {
        "schema": "0.1",
        "documents": {
            "index": {
                "header": "Top-Level Header (Main)",
                "lede": "The root of the problems.",
                "sections": [
                    {
                        "header": "Meats",
                        "contents": [
                            {
                                "type": "paragraph",
                                "text": [
                                    "A small paragraph about meats.",
                                ],
                            },
                        ],
                    },
                    {
                        "header": "Salads",
                        "contents": [
                            {
                                "type": "paragraph",
                                "text": [
                                    "A small paragraph about salads.",
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
                    },
                    {
                        "header": "Vegetables",
                        "contents": [
                            {
                                "type": "paragraph",
                                "text": [
                                    "A small paragraph about vegetables.",
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
                    },
                ],
            },
        },
    }

    def check_has_index_doc(ingredients: dict[str, Any]) -> bool:
        """Return True if promise met else False"""
        documents = ingredients.get("documents", {})
        return "index" in documents

    def check_index_doc_has_list_of_salads(ingredients: dict[str, Any]) -> bool:
        """Return True if promise met else False"""
        if not check_has_index_doc(ingredients):
            return False

        documents = ingredients.get("documents", {})
        index_doc = documents.get("index")
        for section in index_doc.get("sections", []):
            header = section.get("header")
            contents = section.get("contents", [])
            if header == "Salads":
                for content in contents:
                    if content.get("type") == "ordered_list":
                        return True

        return False

    def check_index_doc_has_list_of_meats(ingredients: dict[str, Any]) -> bool:
        """Return True if promise met else False"""
        if not check_has_index_doc(ingredients):
            return False

        documents = ingredients.get("documents", {})
        index_doc = documents.get("index")
        for section in index_doc.get("sections", []):
            header = section.get("header")
            contents = section.get("contents", [])
            if header == "Meats":
                for content in contents:
                    if content.get("type") == "ordered_list":
                        return True

        return False

    promises = [
        IngredientPromise("An index document is present.", check_has_index_doc),
        IngredientPromise(
            "Index document has list of salads.", check_index_doc_has_list_of_salads
        ),
        IngredientPromise(
            "Index document has list of meats.", check_index_doc_has_list_of_meats
        ),
    ]

    my_sausage_man = SausageMan()
    my_sausage_man.give_ingredients(example_mystery_meat)
    my_sausage_man.give_promises(promises)
    promises_met = my_sausage_man.check_promises()
    if not promises_met:
        logger.error("Not all required promises were kept. Ingredients are not good!")


if __name__ == "__main__":
    show_unmet_promise()
