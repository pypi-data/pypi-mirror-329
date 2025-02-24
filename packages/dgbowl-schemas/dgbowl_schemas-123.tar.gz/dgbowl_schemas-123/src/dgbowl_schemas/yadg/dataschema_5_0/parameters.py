from pydantic import BaseModel
from typing import Union

from .timestamp import Timestamp, TimeDate, UTS


class Parameters(BaseModel, extra="forbid"):
    """Empty parameters specification with no extras allowed."""

    pass


Timestamps = Union[Timestamp, TimeDate, UTS]
