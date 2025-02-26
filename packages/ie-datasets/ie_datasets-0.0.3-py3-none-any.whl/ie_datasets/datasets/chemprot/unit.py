from functools import cached_property
from typing import Literal, Sequence, TypeAlias

from pydantic import model_validator

from ie_datasets.util.interfaces import ImmutableModel


ChemProtEntityType: TypeAlias = Literal[
    "CHEMICAL",
    "GENE-N",
    "GENE-Y",
]

ChemProtRelationType: TypeAlias = Literal[
    "CPR:0",
    "CPR:1",
    "CPR:2",
    "CPR:3",
    "CPR:4",
    "CPR:5",
    "CPR:6",
    "CPR:7",
    "CPR:8",
    "CPR:9",
    "CPR:10",
]


class ChemProtEntityMention(ImmutableModel):
    id: str
    entity_type: ChemProtEntityType
    text: str
    start: int
    end: int


class ChemProtRelation(ImmutableModel):
    relation_type: ChemProtRelationType
    argument_1: str
    argument_2: str


class ChemProtUnit(ImmutableModel):
    pmid: int
    text: str
    entities: Sequence[ChemProtEntityMention]
    relations: Sequence[ChemProtRelation]

    @cached_property
    def entity_by_id(self):
        return {entity.id: entity for entity in self.entities}

    @model_validator(mode="after")
    def validate_entities(self):
        for entity in self.entities:
            assert self.text[entity.start:entity.end] == entity.text
        return self

    @model_validator(mode="after")
    def validate_relations(self):
        for relation in self.relations:
            assert relation.argument_1 in self.entity_by_id
            assert relation.argument_2 in self.entity_by_id
        return self

    @property
    def num_chars(self):
        return len(self.text)

    @property
    def num_entity_mentions(self):
        return len(self.entities)

    @property
    def num_relations(self):
        return len(self.relations)


__all__ = [
    "ChemProtEntityMention",
    "ChemProtEntityType",
    "ChemProtRelation",
    "ChemProtRelationType",
    "ChemProtUnit",
]
