# Markdown Sausage Machine

A Python3 library to creates markdown documents programatically.

## Usage

You can integrate and use the markdown sausage machine via two interfaces:

1. SausageMachine: A class that lets you call programatically on its
   instantiated self to create a markdown document.

2. SausageMan: A class that lets you import a Python dict of content to create a
   markdown document.

More details on each approach is shown below.

### SausageMachine

SausageMachine can be instantiated and controlled programatically to produce a
markdown document.

```
import logging
from pathlib import Path

from markdownsausagemachine.contents import OrderedList, Paragraph, UnorderedList
from markdownsausagemachine.sausage_machine import SausageMachine

my_sausage_machine = SausageMachine()
index_doc = my_sausage_machine.add_document("index")
index_doc.set_header("Index")
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

output_dir = Path("./example1/output")
output_dir.mkdir(parents=True, exist_ok=True)
my_sausage_machine.output_markdown_documents(output_dir)
logger.info("Done! Output created in: %s", output_dir)
```

### SausageMan

SausageMan can be instantiated and wraps a SausageMachine instance, and takes a
dictionary as input to produce a markdown document. Said dictionary is of an
expected format that is not yet fully documented but the example below provides
a rough guideline.

```
import logging
from pathlib import Path

from markdownsausagemachine.sausage_man import SausageMan

logger = logging.getLogger(__name__)
logging.basicConfig(encoding="utf-8", level=logging.DEBUG)

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

my_sausage_man = SausageMan()
my_sausage_man.give_ingredients(example_mystery_meat)

output_dir = Path("./example2/output")
output_dir.mkdir(parents=True, exist_ok=True)
my_sausage_man.get_markdown_files(output_dir)
logger.info("Done! Output created in: %s", output_dir)
```

SausageMan also supports enforcing "promises" around the digested content. This
allows you to enforce things such as required documents, required contents, etc.

```
import logging

from markdownsausagemachine.sausage_man import IngredientPromise, SausageMan

logger = logging.getLogger(__name__)
logging.basicConfig(encoding="utf-8", level=logging.DEBUG)

def check_has_index_doc(ingredients: dict[str, Any]) -> bool:
    """Return True if promise met else False"""
    documents = ingredients.get("documents", {})
    return "index" in documents

promises = [
    IngredientPromise("An index document is present.", check_has_index_doc),
]

my_sausage_man = SausageMan()
my_sausage_man.give_ingredients(example_mystery_meat)
my_sausage_man.give_promises(promises)
promises_met = my_sausage_man.check_promises()
if not promises_met:
    logger.error("Quality not met! Ingredients are not good!")
```

## Developers

The following is information for developers working with extending/enhancing
this library.

### Unit Tests

You can run the unit tests like so:

```
pdm install --dev
pdm unit-test
```