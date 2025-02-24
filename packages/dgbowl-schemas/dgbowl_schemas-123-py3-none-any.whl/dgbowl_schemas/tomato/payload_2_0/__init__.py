from pydantic import BaseModel, Field, model_validator
from typing import Sequence, Literal
from .settings import Settings
from .sample import Sample
from .task import Task

from pathlib import Path
import yaml
import json


class Payload(BaseModel, extra="forbid"):
    version: Literal["2.0"]
    settings: Settings = Field(default_factory=Settings)
    """Additional configuration options for tomato."""

    sample: Sample
    """Specification of the experimental sample."""

    method: Sequence[Task]
    """A sequence of the experimental :class:`Tasks`."""

    @model_validator(mode="before")
    @classmethod
    def extract_samplefile(cls, values):
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

    @model_validator(mode="before")
    @classmethod
    def extract_methodfile(cls, values):
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
