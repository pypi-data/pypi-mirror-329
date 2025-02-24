from pydantic.v1 import BaseModel, Extra, Field, root_validator
from typing import Sequence, Literal
from .tomato import Tomato
from .sample import Sample
from .method import Method
from ..payload_0_2 import Payload as NewPayload

import logging
from pathlib import Path
import yaml
import json

logger = logging.getLogger(__name__)


class Payload(BaseModel, extra=Extra.forbid):
    version: Literal["0.1"]
    tomato: Tomato = Field(default_factory=Tomato)
    sample: Sample
    method: Sequence[Method]

    @root_validator(pre=True)
    def extract_samplefile(cls, values):  # pylint: disable=E0213
        if "samplefile" in values:
            sf = Path(values.pop("samplefile"))
            assert sf.exists()
            with sf.open() as f:
                if sf.suffix in {".yml", ".yaml"}:
                    sample = yaml.safe_load(f)
                elif sf.suffix in {".json"}:
                    sample = json.load(f)
                else:
                    raise ValueError(f"Incorrect suffix of samplefile: '{sf}'")
            assert "sample" in sample
            values["sample"] = sample["sample"]
        return values

    @root_validator(pre=True)
    def extract_methodfile(cls, values):  # pylint: disable=E0213
        if "methodfile" in values:
            mf = Path(values.pop("methodfile"))
            assert mf.exists()
            with mf.open() as f:
                if mf.suffix in {".yml", ".yaml"}:
                    method = yaml.safe_load(f)
                elif mf.suffix in {".json"}:
                    method = json.load(f)
                else:
                    raise ValueError(f"Incorrect suffix of methodfile: '{mf}'")
            assert "method" in method
            values["method"] = method["method"]
        return values

    def update(self):
        logger.info("Updating from Payload-0.1 to Payload-0.2")
        md = self.dict(exclude_defaults=True, exclude_none=True)
        md["version"] = "0.2"

        return NewPayload(**md)
