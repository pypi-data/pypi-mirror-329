from pydantic.v1 import BaseModel, Field
from typing import Literal, Sequence, Optional, Tuple, Any, Dict


class SeriesIndex(BaseModel, extra="forbid"):
    from_zero: bool = True
    to_units: Optional[str]


class Series(BaseModel, extra="allow"):
    y: str
    x: Optional[str]
    kind: Literal["scatter", "line", "errorbar"] = "scatter"
    index: Optional[SeriesIndex] = SeriesIndex()


class AxArgs(BaseModel, extra="allow"):
    cols: Optional[Tuple[int, int]]
    rows: Optional[Tuple[int, int]]
    series: Sequence[Series]
    methods: Optional[Dict[str, Any]]
    legend: bool = False


class PlotSave(BaseModel, extra="allow", allow_population_by_field_name=True):
    as_: str = Field(alias="as")
    tight_layout: Optional[Dict[str, Any]]


class Plot(BaseModel, extra="forbid"):
    table: str
    ax_args: Sequence[AxArgs]
    fig_args: Optional[Dict[str, Any]]
    style: Optional[Dict[str, Any]]
    nrows: int = 1
    ncols: int = 1
    save: Optional[PlotSave]
