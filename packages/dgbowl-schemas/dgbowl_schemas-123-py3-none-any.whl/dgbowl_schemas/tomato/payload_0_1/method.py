from pydantic.v1 import BaseModel, Extra


class Method(BaseModel, extra=Extra.allow):
    device: str
    technique: str
