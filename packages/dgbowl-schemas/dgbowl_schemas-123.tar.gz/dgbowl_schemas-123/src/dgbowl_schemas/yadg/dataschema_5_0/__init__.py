from pydantic import BaseModel, Field
from typing import Sequence
from babel import Locale, UnknownLocaleError
import logging
from .metadata import Metadata
from .step import Steps
from .stepdefaults import StepDefaults
from .filetype import (  # noqa: F401
    ExtractorFactory as ExtractorFactory,
    FileType as FileType,
)
from ..dataschema_5_1 import DataSchema as NewDataSchema

logger = logging.getLogger(__name__)


class DataSchema(BaseModel, extra="forbid"):
    """
    A :class:`pydantic.BaseModel` implementing ``DataSchema-5.0`` model introduced in
    ``yadg-5.0``.
    """

    metadata: Metadata
    """Input metadata for :mod:`yadg`."""

    step_defaults: StepDefaults = Field(StepDefaults())
    """Default values for configuration of :mod:`yadg`'s parsers."""

    steps: Sequence[Steps]
    """Input commands for :mod:`yadg`'s parsers, organised as a sequence of steps."""

    def update(self):
        logger.info("Updating from DataSchema-5.0 to DataSchema-5.1")

        nsch = {"version": "5.1", "metadata": {}, "step_defaults": {}, "steps": []}
        for k, v in self.metadata.provenance.model_dump(exclude_none=True).items():
            if k == "version":
                continue
            else:
                nsch["metadata"][k] = v

        nsch["step_defaults"] = self.step_defaults.model_dump(
            exclude_none=True, exclude_defaults=True
        )

        # Make sure we only pass locales that are valid
        if nsch["step_defaults"].get("locale") is not None:
            try:
                v = str(Locale.parse(nsch["step_defaults"]["locale"]))
            except (TypeError, UnknownLocaleError, ValueError):
                del nsch["step_defaults"]["locale"]

        for step in self.steps:
            nstep = {
                "tag": step.tag,
                "input": step.input.model_dump(exclude_none=True),
            }
            extractor = step.extractor.model_dump(exclude_none=True)
            if step.parser == "dummy":
                if step.extractor.filetype == "tomato.json":
                    extractor["filetype"] = "tomato.json"
                else:
                    extractor["filetype"] = "example"
            elif step.parser == "basiccsv":
                extractor["filetype"] = "basic.csv"
            elif step.parser == "meascsv":
                extractor["filetype"] = "fhimcpt.csv"
            if extractor["filetype"] == "labview.csv":
                extractor["filetype"] = "fhimcpt.vna"
            if step.parameters is not None:
                extractor["parameters"] = step.parameters.model_dump(exclude_none=True)
            if step.externaldate is not None:
                nstep["externaldate"] = step.externaldate.model_dump(exclude_none=True)
            nstep["extractor"] = extractor
            nsch["steps"].append(nstep)

        return NewDataSchema(**nsch)
