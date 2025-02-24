from pydantic import BaseModel, Field
from typing import Literal, Sequence, Optional, Tuple, Any, Dict


class SeriesIndex(BaseModel, extra="forbid"):
    from_zero: bool = True
    to_units: Optional[str] = None


class Series(BaseModel, extra="allow"):
    y: str
    x: Optional[str] = None
    kind: Literal["scatter", "line", "errorbar"] = "scatter"
    index: Optional[SeriesIndex] = SeriesIndex()


class AxArgs(BaseModel, extra="allow"):
    cols: Optional[Tuple[int, int]] = None
    rows: Optional[Tuple[int, int]] = None
    series: Sequence[Series]
    methods: Optional[Dict[str, Any]] = None
    legend: bool = False


class PlotSave(BaseModel, extra="allow", populate_by_name=True):
    as_: str = Field(alias="as")
    tight_layout: Optional[Dict[str, Any]] = None


class Plot(BaseModel, extra="forbid"):
    """Plot data from a single table."""

    table: str
    """The name of the table loaded in memory to be plotted."""

    nrows: int = 1
    """Number of rows in the figure grid."""

    ncols: int = 1
    """Number of columns in the figure grid."""

    fig_args: Optional[Dict[str, Any]] = None
    """Any optional method calls for the figure; passed to ``matplotlib``."""

    ax_args: Sequence[AxArgs]
    """Specifications of the figure axes, including selection of data for the plots."""

    style: Optional[Dict[str, Any]] = None
    """Specification of overall ``matplotlib`` style."""

    save: Optional[PlotSave] = None
    """Arguments for saving the plotted figure into files."""
