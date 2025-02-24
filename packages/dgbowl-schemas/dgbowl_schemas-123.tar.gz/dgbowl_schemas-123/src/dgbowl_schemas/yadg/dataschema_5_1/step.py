from pydantic import BaseModel
from typing import Optional, Union
from .externaldate import ExternalDate
from .input import Input
from .filetype import FileTypes


class Step(BaseModel, extra="forbid"):
    extractor: Union[FileTypes]
    input: Input
    tag: Optional[str] = None
    externaldate: Optional[ExternalDate] = None
