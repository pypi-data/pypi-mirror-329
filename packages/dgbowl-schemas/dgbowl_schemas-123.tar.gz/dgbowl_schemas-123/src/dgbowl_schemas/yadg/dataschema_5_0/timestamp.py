from pydantic import BaseModel
from typing import Optional


class TimestampSpec(BaseModel, extra="forbid"):
    """Specification of the column index and string format of the timestamp."""

    index: Optional[int] = None
    format: Optional[str] = None


class Timestamp(BaseModel, extra="forbid"):
    """Timestamp from a column containing a single timestamp string."""

    timestamp: TimestampSpec


class UTS(BaseModel, extra="forbid"):
    """Timestamp from a column containing a Unix timestamp."""

    uts: TimestampSpec


class TimeDate(BaseModel, extra="forbid"):
    """Timestamp from a separate date and/or time column."""

    date: Optional[TimestampSpec] = None
    time: Optional[TimestampSpec] = None
