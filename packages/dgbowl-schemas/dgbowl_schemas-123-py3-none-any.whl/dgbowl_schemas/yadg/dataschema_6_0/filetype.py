import sys
import inspect
from pydantic import BaseModel, Field, field_validator
from abc import ABC
from typing import Optional, Literal, Mapping, Any, TypeVar
import tzlocal
from babel import Locale
import logging

from .stepdefaults import StepDefaults
from .parameters import Timestamps, Timestamp

logger = logging.getLogger(__name__)


class FileType(BaseModel, ABC, extra="forbid"):
    """Template abstract base class for parser classes."""

    filetype: Optional[str] = None
    timezone: Optional[str] = None
    locale: Optional[str] = None
    encoding: Optional[str] = None
    parameters: Optional[Any] = None

    @field_validator("timezone")
    @classmethod
    def timezone_resolve_localtime(cls, v):
        if v == "localtime":
            v = tzlocal.get_localzone_name()
        return v

    @field_validator("locale")
    @classmethod
    def locale_validate_default(cls, v):
        if v is not None:
            v = str(Locale.parse(v))
        return v


class Example(FileType):
    class Parameters(BaseModel, extra="allow"):
        pass

    parameters: Parameters = Field(default_factory=Parameters)
    filetype: Literal["example"]


class Agilent_ch(FileType):
    filetype: Literal["agilent.ch"]


class Agilent_dx(FileType):
    filetype: Literal["agilent.dx"]


class Agilent_csv(FileType):
    filetype: Literal["agilent.csv"]


class Basic_csv(FileType):
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

    parameters: Parameters = Field(default_factory=Parameters)
    filetype: Literal["basic.csv"]


class Drycal_csv(FileType):
    filetype: Literal["drycal.csv"]


class Drycal_rtf(FileType):
    filetype: Literal["drycal.rtf"]


class Drycal_txt(FileType):
    filetype: Literal["drycal.txt"]


class EClab_mpr(FileType):
    filetype: Literal["eclab.mpr"]


class EClab_mpt(FileType):
    filetype: Literal["eclab.mpt"]
    encoding: Optional[str] = "windows-1252"

    @field_validator("encoding")
    @classmethod
    def set_encoding(cls, encoding):
        return encoding or "windows-1252"


class EmpaLC_csv(FileType):
    filetype: Literal["empalc.csv"]


class EmpaLC_xlsx(FileType):
    filetype: Literal["empalc.xlsx"]


class EZChrom_dat(FileType):
    filetype: Literal["ezchrom.dat"]


class EZChrom_asc(FileType):
    filetype: Literal["ezchrom.asc"]
    encoding: Optional[str] = "windows-1252"

    @field_validator("encoding")
    @classmethod
    def set_encoding(cls, encoding):
        return encoding or "windows-1252"


class FHI_csv(FileType):
    class Parameters(BaseModel, extra="forbid"):
        timestamp: Timestamps = Field(
            Timestamp(timestamp={"index": 0, "format": "%Y-%m-%d-%H-%M-%S"})
        )

    parameters: Parameters = Field(default_factory=Parameters)
    filetype: Literal["fhimcpt.csv"]


class FHI_vna(FileType):
    filetype: Literal["fhimcpt.vna"]


class Fusion_json(FileType):
    filetype: Literal["fusion.json"]


class Fusion_zip(FileType):
    filetype: Literal["fusion.zip"]


class Fusion_csv(FileType):
    filetype: Literal["fusion.csv"]


class Panalytical_xy(FileType):
    filetype: Literal["panalytical.xy"]


class Panalytical_csv(FileType):
    filetype: Literal["panalytical.csv"]


class PicoLog_tc08(FileType):
    filetype: Literal["picolog.tc08"]


class Panalytical_xrdml(FileType):
    filetype: Literal["panalytical.xrdml"]


class Phi_spe(FileType):
    filetype: Literal["phi.spe"]


class Quadstar_sac(FileType):
    filetype: Literal["quadstar.sac"]


class Tomato_json(FileType):
    filetype: Literal["tomato.json"]


class Touchstone_snp(FileType):
    filetype: Literal["touchstone.snp"]


classlist = []
for name, obj in inspect.getmembers(sys.modules[__name__]):
    if inspect.isclass(obj) and issubclass(obj, FileType) and obj is not FileType:
        classlist.append(obj)
FileTypes = TypeVar("FileTypes", *classlist)


class ExtractorFactory(BaseModel):
    """
    Extractor factory class.

    Given an ``extractor=dict(filetype=k, ...)`` argument, attempts to determine the
    correct :class:`FileType`, parses any additionally supplied parameters for that
    :class:`FileType`, and back-fills defaults such as ``timezone``, ``locale``, and
    ``encoding``.

    The following is the current usage pattern in :mod:`yadg`:

    .. code-block::

        ftype = ExtractorFactory(extractor={"filetype": k}).extractor
    """

    extractor: FileTypes = Field(..., discriminator="filetype")

    @field_validator("extractor")
    @classmethod
    def extractor_set_defaults(cls, v):
        defaults = StepDefaults()
        if v.timezone is None:
            v.timezone = defaults.timezone
        if v.locale is None:
            v.locale = defaults.locale
        if v.encoding is None:
            v.encoding = defaults.encoding
        return v
