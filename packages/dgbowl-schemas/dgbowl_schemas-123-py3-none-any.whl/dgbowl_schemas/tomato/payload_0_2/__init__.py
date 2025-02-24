from pydantic.v1 import BaseModel, Extra, Field, root_validator
from typing import Sequence, Literal
from .tomato import Tomato
from .sample import Sample
from .method import Method
from ..payload_1_0 import Payload as NewPayload

from pathlib import Path
import yaml
import json
import logging

logger = logging.getLogger(__name__)


class Payload(BaseModel, extra=Extra.forbid):
    version: Literal["0.2"]
    tomato: Tomato = Field(default_factory=Tomato)
    """Additional configuration options for tomato."""

    sample: Sample
    """Specification of the experimental sample."""

    method: Sequence[Method]
    """A sequence of the experimental methods."""

    @root_validator(pre=True)
    def extract_samplefile(cls, values):  # pylint: disable=E0213
        """
        If ``samplefile`` is provided in ``values``, parse the file as ``sample``.
        """
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
        """
        If ``methodfile`` is provided in ``values``, parse the file as ``method``.
        """
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
        logger.info("Updating from Payload-0.2 to Payload-1.0")
        md = self.dict(exclude_defaults=True, exclude_none=True)
        md["version"] = "1.0"
        md["settings"] = md.pop("tomato")
        for step in md["method"]:
            step["component_tag"] = step.pop("device")

            # max_duration is time in biologic and dummy
            if "time" in step:
                step["max_duration"] = step.pop("time")

            # sampling_interval is delay in dummy and record_every_dt in biologic
            if "delay" in step:
                step["sampling_interval"] = step.pop("delay")
            elif "record_every_dt" in step:
                step["sampling_interval"] = step.pop("record_every_dt")

            technique = {}
            for k in tuple(step.keys()):
                if k in {"component_tag", "max_duration", "sampling_interval"}:
                    continue
                elif k in {"technique"}:
                    step["technique_name"] = step.pop(k)
                else:
                    technique[k] = step.pop(k)
            step["technique_params"] = technique
        return NewPayload(**md)
