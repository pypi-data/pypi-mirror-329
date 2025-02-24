from pydantic import BaseModel, Field
from typing import Sequence, Literal, Union, Optional


class Pivot(BaseModel, extra="forbid", populate_by_name=True):
    """Reorder tables by grouping rows into arrays using columns as indices."""

    table: str
    """The name of the table loaded in memory to be pivoted."""

    as_: str = Field(alias="as")
    """The name for the resulting table for in memory storage."""

    using: Union[str, Sequence[str]]
    """A column name (or their sequence) by which the pivoting is performed."""

    columns: Optional[Sequence[str]] = None
    """A sequence of column names which are to be pivoted."""

    timestamp: Literal["first", "last", "mean"] = "first"
    """Specification of the resulting timestamp for the pivoted data. For each pivoted
    row, the ``first`` or ``last`` timestamp can be used as index. Alternatively, the
    ``mean`` can be calculated and used as index."""

    timedelta: Optional[str] = None
    """If provided, the corresponding time deltas for the pivoted data is computed and
    stored under the provided column name. By default, this data is not computed."""
