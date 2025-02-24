from pydantic import BaseModel, Field, field_validator
from typing import Optional, Tuple, Union
import locale
import tzlocal


class StepDefaults(BaseModel, extra="forbid"):
    """Configuration of defaults applicable for all steps."""

    timezone: str = Field("localtime", validate_default=True)
    """Global timezone specification.

    .. note::

        This should be set to the timezone where the measurements have been
        performed, as opposed to the timezone where :mod:`yadg` is being executed.
        Otherwise timezone offsets may not be accounted for correctly.

    """

    locale: Union[Tuple[str, str], str, None] = Field(None, validate_default=True)
    """Global locale specification. Will default to current locale."""

    encoding: Optional[str] = None
    """Global filetype encoding. Will default to ``None``."""

    @field_validator("timezone")
    @classmethod
    def timezone_resolve_localtime(cls, v):
        if v == "localtime":
            v = tzlocal.get_localzone_name()
        return v

    @field_validator("locale")
    @classmethod
    def locale_set_default(cls, v):
        if v is None:
            for loc in (locale.getlocale(), locale.getlocale(locale.LC_NUMERIC)):
                try:
                    v = ".".join(loc)
                    break
                except TypeError:
                    pass
            else:
                v = "en_GB.UTF-8"
        return v
