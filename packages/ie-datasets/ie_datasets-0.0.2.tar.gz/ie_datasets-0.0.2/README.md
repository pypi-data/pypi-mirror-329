# Information Extraction Datasets

This package takes care of all of the tedium when loading various information extraction datasets, providing the data in fully validated and typed Pydantic objects.

## Datasets

### WikiEvents [Event Argument Extraction]

> [**NAACL 2021**](https://aclanthology.org/2021.naacl-main.69/) |
> [**GitHub**](https://github.com/raspberryice/gen-arg)

```py
from ie_datasets import WikiEvents

WikiEvents.load_ontology()
WikiEvents.load_wikievents_units("train")
WikiEvents.load_wikievents_units("dev")
WikiEvents.load_wikievents_units("test")
```
