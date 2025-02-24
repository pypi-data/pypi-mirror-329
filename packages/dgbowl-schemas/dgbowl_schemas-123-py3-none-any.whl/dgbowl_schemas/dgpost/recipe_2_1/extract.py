from pydantic import BaseModel, Field, model_validator
from typing import Optional, Sequence, Any
import logging

logger = logging.getLogger(__name__)


class At(BaseModel, extra="forbid"):
    steps: Sequence[str] = None
    indices: Sequence[int] = None
    timestamps: Sequence[float] = None

    @model_validator(mode="before")
    def check_one_input(cls, values):  # pylint: disable=E0213
        keys = {"step", "steps", "index", "indices", "timestamp"}
        assert len(keys.intersection(set(values))) == 1, (
            f"multiple keys provided: {keys.intersection(values)}"
        )
        if "step" in values:
            values["steps"] = [values.pop("step")]
        elif "index" in values:
            values["indices"] = [values.pop("index")]
        return values


class Constant(BaseModel, extra="forbid"):
    value: Any
    as_: str = Field(alias="as")
    units: Optional[str] = None


class Column(BaseModel, extra="forbid"):
    key: str
    as_: str = Field(alias="as")


class Extract(BaseModel, extra="forbid"):
    """Extract columns from loaded files into tables, interpolate as necessary."""

    into: str
    """Name of a new, or existing / loaded table into which the extraction happens."""

    from_: Optional[str] = Field(None, alias="from")
    """Name of the source object for the extracted data."""

    at: Optional[At] = None
    """Specification of the steps (or data indices) from which data is to be extracted."""

    columns: Optional[Sequence[Column]] = None
    """Specifications for the columns to be extracted, including new headers."""

    constants: Optional[Sequence[Constant]] = None
    """Specifications for additional columns containing data constants, including units."""

    @model_validator(mode="before")
    def check_one_input(cls, values):  # pylint: disable=E0213
        keys = {"constants", "columns"}
        if len(keys.intersection(set(values))) == 0:
            logging.info("did not provide any of '%s'", keys)
        return values
