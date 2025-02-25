from contextlib import contextmanager
from typing import Annotated, Collection, TypeAlias, TypeVar

from pydantic import AfterValidator, BaseModel, ConfigDict


T_Collection = TypeVar("T_Collection", bound=Collection)

def assert_empty(collection: T_Collection) -> T_Collection:
    assert len(collection) == 0
    return collection


EmptyList: TypeAlias = Annotated[list, AfterValidator(assert_empty)]


class ImmutableModel(BaseModel):
    model_config = ConfigDict(frozen=True)

    @contextmanager
    def _unfreeze(self):
        """
        If you must mutate (such as in a model validator that updates a field)
        then you must explicitly allow it using this protected context manager.
        """
        old_frozen_value = self.model_config.get("frozen")
        try:
            self.model_config["frozen"] = False
            yield
        finally:
            if old_frozen_value is None:
                del self.model_config["frozen"]
            else:
                self.model_config["frozen"] = old_frozen_value

    def model_update(self, **kwargs):
        return self.model_copy(update=kwargs)
