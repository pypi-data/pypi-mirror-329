# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
from .client_facing_water_changed_event_type import ClientFacingWaterChangedEventType
from .grouped_water import GroupedWater
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import typing
import pydantic


class ClientFacingWaterChanged(UniversalBaseModel):
    event_type: ClientFacingWaterChangedEventType
    user_id: str
    client_user_id: str
    team_id: str
    data: GroupedWater

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
