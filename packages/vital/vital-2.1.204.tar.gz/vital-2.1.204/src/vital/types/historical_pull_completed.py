# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import datetime as dt
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import typing
import pydantic


class HistoricalPullCompleted(UniversalBaseModel):
    user_id: str
    start_date: dt.datetime
    end_date: dt.datetime
    is_final: bool
    provider: str

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
