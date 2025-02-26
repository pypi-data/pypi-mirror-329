from typing import Literal, Sequence, TypeAlias

from pydantic import model_validator

from ie_datasets.util.interfaces import ImmutableModel


SciERCEntityType: TypeAlias = Literal[
    "Generic",
    "Material",
    "Method",
    "Metric",
    "OtherScientificTerm",
    "Task",
]


SciERCRelationType: TypeAlias = Literal[
    "COMPARE",
    "CONJUNCTION",
    "EVALUATE-FOR",
    "FEATURE-OF",
    "HYPONYM-OF",
    "PART-OF",
    "USED-FOR",
]


class SciERCUnit(ImmutableModel):
    doc_key: str
    sentences: Sequence[Sequence[str]]
    clusters: Sequence[Sequence[tuple[int, int]]] # coreference resolution
    ner: Sequence[Sequence[tuple[int, int, SciERCEntityType]]]
    relations: Sequence[Sequence[tuple[int, int, int, int, SciERCRelationType]]]

    @model_validator(mode="after")
    def validate_clusters(self):
        for clusters in self.clusters:
            assert clusters == sorted(set(clusters))
        return self

    @model_validator(mode="after")
    def validate_sentences(self):
        assert len(self.sentences) == len(self.ner) == len(self.relations)
        return self

    @model_validator(mode="after")
    def validate_ner(self):
        for ner in self.ner:
            for start, end, entity_type in ner:
                assert start <= end
        return self

    @model_validator(mode="after")
    def validate_relations(self):
        for relations in self.relations:
            for start1, end1, start2, end2, relation_type in relations:
                assert start1 <= end1
                assert start2 <= end2
        return self

    @property
    def num_tokens(self) -> int:
        return sum(len(sentence) for sentence in self.sentences)

    @property
    def num_sentences(self) -> int:
        return len(self.sentences)

    @property
    def num_entity_mentions(self) -> int:
        return sum(len(ner) for ner in self.ner)

    @property
    def num_relations(self) -> int:
        return sum(len(relations) for relations in self.relations)
