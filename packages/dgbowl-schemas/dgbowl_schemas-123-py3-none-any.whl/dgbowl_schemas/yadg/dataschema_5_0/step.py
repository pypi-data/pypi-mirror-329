from pydantic import BaseModel, Field
from abc import ABC
from typing import Optional, Literal, Mapping, Union
from .externaldate import ExternalDate
from .input import Input
from .parameters import Parameters, Timestamps, Timestamp
from .filetype import (
    FileType,
    NoFileType,
    DummyFileTypes,
    FlowDataFileTypes,
    ElectroChemFileTypes,
    ChromTraceFileTypes,
    ChromDataFileTypes,
    MassTraceFileTypes,
    QFTraceFileTypes,
    XPSTraceFileTypes,
    XRDTraceFileTypes,
)


try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


class Parser(BaseModel, ABC, extra="forbid"):
    tag: Optional[str] = None
    parser: str
    input: Input
    extractor: Optional[FileType] = None
    parameters: Optional[Parameters] = None
    externaldate: Optional[ExternalDate] = None


class Dummy(Parser):
    """Dummy parser type, useful for testing."""

    class Parameters(BaseModel, extra="allow"):
        pass

    parser: Literal["dummy"]
    parameters: Optional[Parameters] = None
    extractor: DummyFileTypes = Field(default_factory=NoFileType)


class BasicCSV(Parser):
    """Customisable tabulated file parser."""

    class Parameters(BaseModel, extra="forbid"):
        sep: str = ","
        """Separator of table columns."""

        strip: Optional[str] = None
        """A :class:`str` of characters to strip from headers & data."""

        units: Optional[Mapping[str, str]] = None
        """A :class:`dict` containing ``column: unit`` keypairs."""

        timestamp: Optional[Timestamps] = None
        """Timestamp specification allowing calculation of Unix timestamp for
        each table row."""

    parser: Literal["basiccsv"]
    parameters: Parameters = Field(default_factory=Parameters)
    extractor: NoFileType = Field(default_factory=NoFileType)


class MeasCSV(Parser, extra="forbid"):
    """
    Legacy file parser for ``measurement.csv`` files from FHI.

    .. note::

        This parser is deprecated, and the :class:`BasicCSV` parser should be
        used instead.

    """

    class Parameters(BaseModel, extra="forbid"):
        timestamp: Timestamps = Field(
            Timestamp(timestamp={"index": 0, "format": "%Y-%m-%d-%H-%M-%S"})
        )

    parser: Literal["meascsv"]
    parameters: Parameters = Field(default_factory=Parameters)
    extractor: NoFileType = Field(default_factory=NoFileType)


class FlowData(Parser):
    """Parser for flow controller/meter data."""

    parser: Literal["flowdata"]
    extractor: FlowDataFileTypes = Field(..., discriminator="filetype")


class ElectroChem(Parser):
    """Parser for electrochemistry files."""

    parser: Literal["electrochem"]
    extractor: ElectroChemFileTypes = Field(..., discriminator="filetype")


class ChromTrace(Parser):
    """
    Parser for raw chromatography traces.

    .. note::

        For parsing processed (integrated) chromatographic data, use the
        :class:`ChromData` parser.

    """

    parser: Literal["chromtrace"]
    extractor: ChromTraceFileTypes = Field(..., discriminator="filetype")


class ChromData(Parser):
    """Parser for processed chromatography data."""

    parser: Literal["chromdata"]
    extractor: ChromDataFileTypes = Field(..., discriminator="filetype")


class MassTrace(Parser):
    """Parser for mass spectroscopy traces."""

    parser: Literal["masstrace"]
    extractor: MassTraceFileTypes  # = Field(..., discriminator="filetype")


class QFTrace(Parser):
    """Parser for network analyzer traces."""

    parser: Literal["qftrace"]
    extractor: QFTraceFileTypes  # = Field(..., discriminator="filetype")


class XPSTrace(Parser):
    """Parser for XPS traces."""

    parser: Literal["xpstrace"]
    extractor: XPSTraceFileTypes  # = Field(..., discriminator="filetype")


class XRDTrace(Parser):
    """Parser for XRD traces."""

    parser: Literal["xrdtrace"]
    extractor: XRDTraceFileTypes  # = Field(..., discriminator="filetype")


Steps = Annotated[
    Union[
        Dummy,
        BasicCSV,
        MeasCSV,
        FlowData,
        ElectroChem,
        ChromTrace,
        ChromData,
        MassTrace,
        QFTrace,
        XPSTrace,
        XRDTrace,
    ],
    Field(discriminator="parser"),
]
