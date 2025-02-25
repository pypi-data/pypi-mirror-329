import json
import os
from typing import Iterable, Literal, TypeAlias

from ie_datasets.datasets.wikievents.interfaces import (
    WikiEventsOntology,
    WikiEventsUnit,
)
from ie_datasets.util.env import get_cache_dir
from ie_datasets.util.wget import open_or_wget

WikiEventsSplit: TypeAlias = Literal["train", "dev", "test"]


BASE_WIKIEVENTS_DIR = get_cache_dir(subpath="wikievents")
ENTITY_TYPES_URL = "https://raw.githubusercontent.com/raspberryice/gen-arg/refs/heads/tapkey/ontology/entity_types.json"
EVENT_TYPES_URL = "https://raw.githubusercontent.com/raspberryice/gen-arg/refs/heads/main/event_role_KAIROS.json"
DATASET_BASE_URL = "https://gen-arg-data.s3.us-east-2.amazonaws.com/wikievents/data"


def load_wikievents_ontology(
        entity_types_url: str = ENTITY_TYPES_URL,
        event_types_url: str = EVENT_TYPES_URL,
) -> WikiEventsOntology:
    with (
        open_or_wget(
            url=entity_types_url,
            local_path=os.path.join(BASE_WIKIEVENTS_DIR, "entity_types.json"),
        ) as entities_file,
        open_or_wget(
            url=event_types_url,
            local_path=os.path.join(BASE_WIKIEVENTS_DIR, "event_types.json"),
        ) as events_file
    ):
        entities_json = json.load(entities_file)
        events_json = json.load(events_file)
        ontology_json = {
            "entity_types": entities_json,
            "event_types": events_json,
        }
        ontology = WikiEventsOntology.model_validate_json(
            json.dumps(ontology_json),
            strict=True,
        )
    return ontology


def load_wikievents_units(
        split: WikiEventsSplit,
        base_url: str = DATASET_BASE_URL,
) -> Iterable[WikiEventsUnit]:
    with (
        open_or_wget(
            url=f"{base_url}/{split}.jsonl",
            local_path=os.path.join(BASE_WIKIEVENTS_DIR, f"{split}.jsonl"),
        ) as unit_file,
        open_or_wget(
            url=f"{base_url}/coref/{split}.jsonlines",
            local_path=os.path.join(BASE_WIKIEVENTS_DIR, "coref", f"{split}.jsonl"),
        ) as coref_file,
    ):
        for unit_line, coref_line in zip(unit_file, coref_file, strict=True):
            unit_json = json.loads(unit_line)
            coref_json = json.loads(coref_line)
            assert "coreferences" not in unit_json
            unit_json["coreferences"] = coref_json
            unit = WikiEventsUnit.model_validate_json(
                json.dumps(unit_json),
                strict=True,
            )
            yield unit
