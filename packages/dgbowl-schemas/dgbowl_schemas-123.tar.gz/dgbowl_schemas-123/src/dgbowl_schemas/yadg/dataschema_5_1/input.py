from pydantic import BaseModel, Field
from typing import Optional, Sequence, List
import os


class Input(BaseModel, extra="forbid", populate_by_name=True):
    """Specification of input files/folders to be processed by the :class:`Step`."""

    files: Sequence[str] = Field(alias="folders")
    """Files, or folders to be searched for matching files."""

    prefix: Optional[str] = None
    """Prefix of the filenames to be matched."""

    suffix: Optional[str] = None
    """Suffix of the filenames to be matched."""

    contains: Optional[str] = None
    """A string the matched filenames must contain."""

    exclude: Optional[str] = None
    """A string the matched filenames must not contain."""

    def paths(self) -> List[str]:
        """Returns a list of files to be processed by the :class:`Step`."""
        ret = []
        for item in sorted(self.files):
            if os.path.isdir(item):
                paths = [os.path.join(item, fn) for fn in sorted(os.listdir(item))]
            else:
                paths = [item]
            for path in paths:
                tail = os.path.basename(path)
                inc = True
                if self.prefix is not None and not tail.startswith(self.prefix):
                    inc = False
                if self.suffix is not None and not tail.endswith(self.suffix):
                    inc = False
                if self.contains is not None and self.contains not in tail:
                    inc = False
                if self.exclude is not None and self.exclude in tail:
                    inc = False
                if inc:
                    ret.append(path)
        return ret
