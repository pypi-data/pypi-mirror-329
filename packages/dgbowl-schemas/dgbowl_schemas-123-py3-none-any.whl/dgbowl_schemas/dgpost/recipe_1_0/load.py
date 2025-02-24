from pydantic.v1 import BaseModel, Field
from typing import Literal


class Load(BaseModel, extra="forbid", allow_population_by_field_name=True):
    as_: str = Field(alias="as")
    path: str
    type: Literal["datagram", "table"] = "datagram"
    check: bool = True
