from pydantic import BaseModel, Field
from typing import Sequence, Optional, Mapping, Any, Literal
from .step import Step
from .stepdefaults import StepDefaults
from .filetype import (  # noqa: F401
    ExtractorFactory as ExtractorFactory,
    FileType as FileType,
    FileTypes as FileTypes,
)
from ..dataschema_6_0 import DataSchema as NewDataSchema


class DataSchema(BaseModel, extra="forbid"):
    """
    A :class:`pydantic.BaseModel` implementing ``DataSchema-5.1`` model
    introduced in ``yadg-5.1``.
    """

    version: Literal["5.1"]

    metadata: Optional[Mapping[str, Any]]
    """Input metadata for :mod:`yadg`."""

    step_defaults: StepDefaults = Field(..., default_factory=StepDefaults)
    """Default values for configuration of each :class:`Step`."""

    steps: Sequence[Step]
    """Input commands for :mod:`yadg`'s extractors, organised as a :class:`Sequence`
    of :class:`Steps`."""

    def update(self):
        nsch = self.model_dump(exclude_none=True, exclude_defaults=True)

        nsch["version"] = "6.0"
        return NewDataSchema(**nsch)
