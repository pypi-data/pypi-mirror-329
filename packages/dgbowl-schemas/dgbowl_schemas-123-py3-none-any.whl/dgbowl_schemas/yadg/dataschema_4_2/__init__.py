from pydantic.v1 import BaseModel, Extra
from typing import Sequence
from .metadata import Metadata
from .step import Steps
import logging

from ..dataschema_5_0 import DataSchema as NewDataSchema

logger = logging.getLogger(__name__)


class DataSchema(BaseModel, extra=Extra.forbid):
    metadata: Metadata
    """Metadata information for yadg."""

    steps: Sequence[Steps]
    """A sequence of parser steps."""

    def update(self):
        logger.info("Updating from DataSchema-4.2 to DataSchema-5.0")

        nsch = {"metadata": {}, "steps": []}
        nsch["metadata"] = {
            "version": "5.0",
            "provenance": self.metadata.provenance.dict(exclude_none=True),
        }
        if self.metadata.timezone is not None:
            nsch["step_defaults"] = {"timezone": self.metadata.timezone}
        if "metadata" not in nsch["metadata"]["provenance"]:
            nsch["metadata"]["provenance"]["metadata"] = {
                "updated-using": "dgbowl-schemas",
                "from": self.metadata.version,
            }
        for step in self.steps:
            nstep = {
                "parser": step.parser,
                "tag": step.tag,
                "input": step.input.dict(exclude_none=True),
            }
            if step.externaldate is not None:
                nstep["externaldate"] = step.externaldate.dict(exclude_none=True)
            if step.parameters is not None:
                nstep["parameters"] = step.parameters.dict(exclude_none=True)
            else:
                nstep["parameters"] = {}

            extractor = {}
            if nstep["parameters"].get("filetype", None) is not None:
                extractor["filetype"] = nstep["parameters"].pop("filetype")
            if nstep["input"].get("encoding", None) is not None:
                extractor["encoding"] = nstep["input"].pop("encoding")
            if len(extractor) > 0:
                nstep["extractor"] = extractor

            for k in {
                "sigma",
                "calfile",
                "convert",
                "species",
                "detectors",
                "method",
                "height",
                "distance",
                "cutoff",
                "threshold",
                "transpose",
            }:
                if k in nstep["parameters"]:
                    logger.warning(
                        "Parameter '%s' of parser '%s' is not "
                        "supported in DataSchema-5.0.",
                        k,
                        nstep["parser"],
                    )
                    del nstep["parameters"][k]

            if nstep["parameters"] == {}:
                del nstep["parameters"]

            nsch["steps"].append(nstep)

        return NewDataSchema(**nsch)
