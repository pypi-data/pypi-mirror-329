#!/usr/bin/env python3

import logging
from pathlib import Path

from markdownsausagemachine.contents import OrderedList, Paragraph, UnorderedList
from markdownsausagemachine.sausage_machine import SausageMachine

logger = logging.getLogger(__name__)
logging.basicConfig(encoding="utf-8", level=logging.DEBUG)


def generate_example_one() -> None:
    logger.info("Generating example3...")

    my_sausage_machine = SausageMachine()
    index_doc = my_sausage_machine.add_document("sausages")
    index_doc.set_header("Sausages")
    index_doc.set_lede("There are many sausage types in this world.")
    new_section = index_doc.add_section("sausage-types")
    new_section.set_header("Sausage Types")
    new_section.add_content(Paragraph("Here are some sausage types:"))
    new_section.add_content(
        UnorderedList(
            [
                Paragraph(
                    "Bratwurst is a traditional German sausage known for its mild and savory flavor. "
                    "It's typically made with pork, beef, or veal, and its name comes from the Old "
                    "High German word “brät,” meaning finely chopped meat, and “wurst,” meaning "
                    "sausage. Bratwurst is heavily seasoned with ingredients like nutmeg, coriander, "
                    "pepper, and sometimes ginger or caraway seeds. These sausages are commonly "
                    "grilled or fried and served with mustard, sauerkraut, or on a bun as part of a "
                    "hearty meal. They're particularly popular during Oktoberfest celebrations and "
                    "other festive occasions."
                ),
                Paragraph(
                    "Chorizo is a spicy sausage that is a staple in Spanish and Mexican cuisines. In "
                    "Spain, chorizo is usually made from pork and flavored with smoked paprika "
                    "(pimentón), garlic, and other spices, giving it a deep red color and a smoky, "
                    "slightly spicy taste. The Spanish version can be either cured and eaten as is, "
                    "or cooked in a variety of dishes like stews, soups, or grilled.  Mexican "
                    "chorizo, on the other hand, is typically fresh and uncooked, made with ground "
                    "pork or beef, and often spiced with chili peppers, vinegar, and garlic.  Both "
                    "versions of chorizo are incredibly versatile and add bold flavor to a wide "
                    "range of meals."
                ),
                Paragraph(
                    "Italian sausage is a flavorful and aromatic sausage variety that comes in two "
                    "main types: sweet and hot. Sweet Italian sausage is flavored with fennel seeds, "
                    "garlic, and sometimes basil, while the hot version includes red pepper flakes "
                    "for a spicy kick. It is commonly made with pork, although it can also be found "
                    "with beef or veal. This sausage is a key ingredient in many Italian-American "
                    "dishes, such as pasta sauces, pizza, and sandwiches. Grilled, pan-fried, or "
                    "simmered in tomato sauce, Italian sausage adds a rich depth of flavor to any "
                    "meal."
                ),
            ]
        )
    )
    new_section.add_content(Paragraph("And here are some more sausage types:"))
    new_section.add_content(
        OrderedList(
            [
                Paragraph(
                    "Andouille is a heavily smoked, spicy sausage that originates from France but "
                    "has become a defining ingredient in Cajun and Creole cuisines, particularly in "
                    "Louisiana. Traditionally made with pork, andouille sausage is known for its "
                    "coarse texture and distinct smoky flavor, which comes from the slow smoking "
                    "process. It is often flavored with garlic, onions, thyme, and cayenne pepper, "
                    "making it quite spicy. Andouille is a key component in dishes like gumbo, "
                    "jambalaya, and crawfish etouffee, where it imparts a bold, smoky richness to "
                    "the meal."
                ),
                Paragraph(
                    "Merguez is a North African sausage, typically made from lamb or beef, and is "
                    "known for its spicy and flavorful profile. It is traditionally seasoned with "
                    "harissa, a chili paste made from roasted red peppers, garlic, and various "
                    "spices, as well as cumin and coriander. Merguez has a deep red color due to the "
                    "spices, and its heat makes it stand out in any dish. Commonly grilled or "
                    "pan-fried, it is often served with couscous, in flatbreads, or as part of a "
                    "larger mezze spread. The combination of heat and fragrant spices makes merguez "
                    "a unique and beloved sausage in Mediterranean and Middle Eastern cooking."
                ),
            ]
        )
    )

    output_dir = Path("./outputs/example3")
    output_dir.mkdir(parents=True, exist_ok=True)
    my_sausage_machine.output_markdown_documents(output_dir)
    logger.info("Done! Output created in: %s", output_dir)


if __name__ == "__main__":
    generate_example_one()
