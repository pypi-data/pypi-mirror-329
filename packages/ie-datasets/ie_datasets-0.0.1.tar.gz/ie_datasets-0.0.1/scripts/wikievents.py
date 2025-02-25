from ie_datasets.datasets.wikievents.load import (
    load_wikievents_ontology,
    load_wikievents_units,
)


print("=" * 80)
print("ONTOLOGY")
ontology = load_wikievents_ontology()
print("-" * 80)
print("ENTITY TYPES")
for name, entity_type in ontology.entity_types_by_name.items():
    print(name, entity_type.definition)
print("-" * 80)
print("EVENT TYPES")
for name, event_type in ontology.event_types.items():
    print(event_type.i_label, name)

for split in ("train", "dev", "test"):
    print("=" * 80)
    print(split.upper())
    for unit in load_wikievents_units(split=split):
        print(unit.doc_id)
        ontology.validate(unit)
