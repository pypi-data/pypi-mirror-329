from pydantic.v1 import BaseModel, Extra


class Sample(BaseModel, extra=Extra.allow):
    name: str
