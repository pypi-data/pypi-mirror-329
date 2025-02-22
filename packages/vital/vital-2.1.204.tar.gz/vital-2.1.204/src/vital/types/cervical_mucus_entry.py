# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
from .cervical_mucus_entry_quality import CervicalMucusEntryQuality
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import typing
import pydantic


class CervicalMucusEntry(UniversalBaseModel):
    date: str
    quality: CervicalMucusEntryQuality

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
