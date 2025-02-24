from pydantic import BaseModel
from typing import Literal, Optional, Union


class ExternalDateFile(BaseModel, extra="forbid"):
    """Read external date information from file."""

    class Content(BaseModel, extra="forbid"):
        path: str
        """Path to the external date information file."""

        type: str
        """Type of the external date information file."""

        match: Optional[str] = None
        """String to be matched within the file."""

    file: Content


class ExternalDateFilename(BaseModel, extra="forbid"):
    """Read external date information from the file name."""

    class Content(BaseModel, extra="forbid"):
        format: str
        """``strptime``-like format string for processing the date."""

        len: int
        """Number of characters from the start of the filename to parse."""

    filename: Content


class ExternalDateISOString(BaseModel, extra="forbid"):
    """Read a constant external date using an ISO-formatted string."""

    isostring: str


class ExternalDateUTSOffset(BaseModel, extra="forbid"):
    """Read a constant external date using a Unix timestamp offset."""

    utsoffset: float


class ExternalDate(BaseModel, extra="forbid"):
    """Supply timestamping information that are external to the processed file."""

    using: Union[
        ExternalDateFile,
        ExternalDateFilename,
        ExternalDateISOString,
        ExternalDateUTSOffset,
    ]
    """Specification of the external date format."""

    mode: Literal["add", "replace"] = "add"
    """Whether the external timestamps should be added to or should replace the
    parsed data."""
