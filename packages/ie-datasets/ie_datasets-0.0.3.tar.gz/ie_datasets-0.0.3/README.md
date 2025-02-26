# Information Extraction Datasets

This package takes care of all of the tedium when loading various information extraction datasets, providing the data in fully validated and typed Pydantic objects.

## Datasets

### [ChemProt](./src/ie_datasets/datasets/chemprot/README.md)

<details>
  <summary>Example</summary>

  ```py
  from ie_datasets import ChemProt
  ChemProt.load_units("train")
  ChemProt.load_units("validation")
  ChemProt.load_units("test")
  ```
</details>

### [SciERC](./src/ie_datasets/datasets/scierc/README.md)

<details>
  <summary>Example</summary>

  ```py
  from ie_datasets import SciERC
  SciERC.load_units("train")
  SciERC.load_units("dev")
  SciERC.load_units("test")
  ```
</details>

### [WikiEvents](./src/ie_datasets/datasets/wikievents/README.md)

<details>
  <summary>Example</summary>

  ```py
  from ie_datasets import WikiEvents
  WikiEvents.load_ontology()
  WikiEvents.load_units("train")
  WikiEvents.load_units("dev")
  WikiEvents.load_units("test")
  ```
</details>
