# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import datetime as dt
import typing
from .client_facing_provider import ClientFacingProvider
from .client_facing_sport import ClientFacingSport
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class WorkoutV2InDb(UniversalBaseModel):
    timestamp: dt.datetime
    data: typing.Dict[str, typing.Optional[typing.Any]]
    provider_id: str
    user_id: str
    source_id: int
    priority_id: typing.Optional[int] = None
    id: str
    sport_id: int
    source: ClientFacingProvider
    sport: ClientFacingSport

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
