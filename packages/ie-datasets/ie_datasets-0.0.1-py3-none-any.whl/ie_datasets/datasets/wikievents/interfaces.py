from functools import cached_property
from typing import Annotated, Mapping, Sequence

from annotated_types import Ge, Gt
from pydantic import Field, model_validator

from ie_datasets.util.interfaces import EmptyList, ImmutableModel


class WikiEventsWordSpan(ImmutableModel):
    start: Annotated[int, Ge(0)]
    end: Annotated[int, Ge(0)]
    text: str
    sent_idx: Annotated[int, Ge(0)]

    @model_validator(mode="after")
    def check_indices_correct(self):
        assert 0 <= self.start < self.end
        return self


class WikiEventsEntityMention(WikiEventsWordSpan):
    id: str
    entity_type: str
    mention_type: str

    @model_validator(mode="after")
    def make_oneoff_corrections(self):
        if self.id == "33_VOA_EN_NW_2014.12.18.2564370-T116":
            assert self.text == "James Whitey Bulger"
            with self._unfreeze():
                self.text = 'James "Whitey" Bulger'
        return self


class WikiEventsEventTrigger(WikiEventsWordSpan):
    pass


class WikiEventsEventArgument(ImmutableModel):
    entity_id: str
    role: str
    text: str


class WikiEventsEventMention(ImmutableModel):
    id: str
    event_type: str
    trigger: WikiEventsEventTrigger
    arguments: Sequence[WikiEventsEventArgument]

    @model_validator(mode="after")
    def make_oneoff_corrections(self):
        if self.id == "scenario_en_kairos_53-E12":
            assert len(self.arguments) == 2

            arg = self.arguments[0]
            assert arg.entity_id == "scenario_en_kairos_53-T43"
            assert arg.role == "Observer"
            with arg._unfreeze():
                arg.role = "Investigator"

            arg = self.arguments[1]
            assert arg.entity_id == "scenario_en_kairos_53-T46"
            assert arg.role == "ObservedEntity"
            with arg._unfreeze():
                arg.role = "Defendant"

        if self.event_type in (
            "Contact.RequestCommand.Broadcast",
            "Contact.RequestCommand.Correspondence",
            "Contact.RequestCommand.Meet",
        ):
            with self._unfreeze():
                self.event_type = "Contact.RequestCommand.Unspecified"

        elif self.event_type in (
            "Contact.ThreatenCoerce.Broadcast",
            "Contact.ThreatenCoerce.Correspondence",
        ):
            with self._unfreeze():
                self.event_type = "Contact.ThreatenCoerce.Unspecified"

        return self


class WikiEventsCoreferences(ImmutableModel):
    doc_key: str
    clusters: Sequence[Sequence[str]]
    informative_mentions: Sequence[str]

    @model_validator(mode="after")
    def check_paired(self):
        assert len(self.clusters) == len(self.informative_mentions)
        return self


class WikiEventsUnit(ImmutableModel):
    doc_id: str
    tokens: Sequence[str]
    text: str
    sentences: Sequence[tuple[Sequence[tuple[str, int, int]], str]]
    entity_mentions: Sequence[WikiEventsEntityMention]
    relation_mentions: EmptyList
    event_mentions: Sequence[WikiEventsEventMention]
    coreferences: WikiEventsCoreferences

    @cached_property
    def token_spans(self) -> Sequence[tuple[int, int]]:
        return [
            (start, end)
            for sentence, _ in self.sentences
            for _, start, end in sentence
        ]

    @cached_property
    def entity_mentions_by_id(self) -> Mapping[str, WikiEventsEntityMention]:
        return {
            e.id: e
            for e in self.entity_mentions
        }

    @cached_property
    def event_mentions_by_id(self) -> Mapping[str, WikiEventsEventMention]:
        return {
            e.id: e
            for e in self.event_mentions
        }

    @cached_property
    def entity_names_by_entity_mention(self) -> Mapping[str, str]:
        assert self.coreferences.doc_key == self.doc_id
        names: dict[str, str] = {}
        for cluster, name in zip(
            self.coreferences.clusters,
            self.coreferences.informative_mentions,
            strict=True,
        ):
            for mention_id in cluster:
                assert mention_id not in names
                names[mention_id] = name
        return names

    @cached_property
    def entity_mentions_by_entity_name(self) -> Mapping[str, frozenset[str]]:
        assert self.coreferences.doc_key == self.doc_id
        mentions: dict[str, frozenset[str]] = {}
        for name, cluster in zip(
            self.coreferences.informative_mentions,
            self.coreferences.clusters,
            strict=True,
        ):
            cluster_set = frozenset(cluster)
            assert len(cluster_set) == len(cluster)
            mentions[name] = cluster_set
        return mentions

    @model_validator(mode="after")
    def fix_text_whitespace(self):
        """
        The start and end bounds of each token cannot be used on self.text.
        The offsets account for whitespace between sentences, which is deleted
        in self.text.
        Instead, the original text should be reconstructed by concatenating the
        sentences, with faithful amounts of whitespace inserted between them.
        """
        text = ""
        for tokens, sentence in self.sentences:
            _, start, _ = tokens[0]
            assert len(text) <= start
            text = text.ljust(start) + sentence.strip()

            for token, start, end in tokens:
                assert text[start:end] == token

        with self._unfreeze():
            self.text = text
        return self

    @model_validator(mode="after")
    def make_oneoff_fixes(self):
        if self.doc_id == "wiki_ied_bombings_0":
            with self._unfreeze():
                self.event_mentions = [
                    mention for mention in self.event_mentions
                    if mention.id != "wiki_ied_bombings_0-E55"
                ]
        return self

    @model_validator(mode="after")
    def check_entities(self):
        entity_ids = set(e.id for e in self.entity_mentions)
        assert len(entity_ids) == len(self.entity_mentions)

        for em in self.event_mentions:
            for a in em.arguments:
                assert a.entity_id in entity_ids

        return self

    @model_validator(mode="after")
    def check_spans(self):
        """
        Must run after self.fix_text_whitespace.
        """
        for e in self.entity_mentions:
            start, end = self.get_char_span(e.start, e.end)
            assert self.text[start:end] == e.text

        for e in self.event_mentions:
            start, end = self.get_char_span(e.trigger.start, e.trigger.end)
            assert self.text[start:end] == e.trigger.text
            for a in e.arguments:
                assert a.text == self.entity_mentions_by_id[a.entity_id].text

        return self

    def get_char_span(
            self,
            start_token: int,
            end_token: int,
    ) -> tuple[int, int]:
        assert start_token < end_token
        start_char, _ = self.token_spans[start_token]
        _, end_char = self.token_spans[end_token - 1]
        return start_char, end_char


class WikiEventsEntityType(ImmutableModel):
    type: str = Field(alias="Type")
    output_value_for_type: str = Field(alias="Output Value for Type")
    definition: str = Field(alias="Definition")


class WikiEventsEventType(ImmutableModel):
    event_id: str
    template: str
    i_label: Annotated[int, Gt(0)] = Field(alias="i-label")
    keywords: Sequence[str]
    roles: Sequence[str] # may contain duplicates
    role_types: Sequence[Sequence[str]]

    @cached_property
    def role_types_by_role(self) -> Mapping[str, frozenset[str]]:
        role_types: dict[str, frozenset[str]] = {}
        for role, types in zip(self.roles, self.role_types):
            types_set = frozenset(types)
            assert len(types_set) == len(types)
            if role in role_types:
                assert types_set == role_types[role]
            else:
                role_types[role] = types_set
        return role_types

    @model_validator(mode="after")
    def make_role_types_three_letter_uppercase(self):
        def transform_role_type(role_type: str):
            if role_type == "event":
                return "CRM"
            if role_type == "side":
                return "SID"
            return role_type.upper()

        with self._unfreeze():
            self.role_types = [
                [transform_role_type(t) for t in types]
                for types in self.role_types
            ]
            if hasattr(self, "role_types_by_role"):
                del self.role_types_by_role
        return self

    @model_validator(mode="after")
    def check_roles(self):
        assert (
            len(self.roles)
            == len(self.role_types)
            >= len(self.role_types_by_role)
        )
        return self

    @model_validator(mode="after")
    def make_oneoff_corrections(self):
        if self.event_id == "LDC_KAIROS_evt_004":
            assert self.template == "<arg1> dismantled <arg2> using <arg3> instrument in <arg4> place"
            assert len(self.roles) == 5
            with self._unfreeze():
                self.template = "<arg1> dismantled <arg2> into <arg4> components using <arg3> instrument in <arg5> place"
        return self

    @model_validator(mode="after")
    def check_template(self):
        for i in range(1, 1+len(self.roles)):
            arg_str = f"<arg{i}>"
            assert arg_str in self.template
        return self


class WikiEventsOntology(ImmutableModel):
    entity_types: Mapping[str, WikiEventsEntityType]
    event_types: Mapping[str, WikiEventsEventType]

    @cached_property
    def entity_types_by_name(self) -> Mapping[str, WikiEventsEntityType]:
        types: dict[str, WikiEventsEntityType] = {}
        for t in self.entity_types.values():
            assert t.type not in types
            types[t.type] = t
        return types

    @model_validator(mode="after")
    def add_crime_entity_type(self):
        crime_entity_type = WikiEventsEntityType(**{
            "Type": "CRM",
            "Output Value for Type": "crm",
            "Definition": "An unlawful act punishable by a state or other authority.",
        })
        with self._unfreeze():
            self.entity_types = {
                **self.entity_types,
                f"{len(self.entity_types)}": crime_entity_type
            }
            if hasattr(self, "entity_types_by_name"):
                del self.entity_types_by_name
        return self

    @model_validator(mode="after")
    def check_entity_types(self):
        for i, key in enumerate(self.entity_types.keys()):
            assert key == str(i)
        assert len(self.entity_types_by_name) == len(self.entity_types)

        return self

    @model_validator(mode="after")
    def check_event_types(self):
        for i, event_type in enumerate(self.event_types.values(), start=1):
            assert event_type.i_label == i
            for types in event_type.role_types:
                for t in types:
                    assert t in self.entity_types_by_name, t
        return self

    def validate(self, unit: WikiEventsUnit):
        for mention in unit.entity_mentions:
            assert mention.entity_type in self.entity_types_by_name

        for mention in unit.event_mentions:
            event_type = self.event_types[mention.event_type]
            for argument in mention.arguments:
                entity = unit.entity_mentions_by_id[argument.entity_id]
                role_types = event_type.role_types_by_role[argument.role]
                assert entity.entity_type in role_types, (argument, event_type)
