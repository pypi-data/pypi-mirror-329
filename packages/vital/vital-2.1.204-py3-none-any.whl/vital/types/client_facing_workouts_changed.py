# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
from .client_facing_workouts_changed_event_type import ClientFacingWorkoutsChangedEventType
from .client_facing_workout import ClientFacingWorkout
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import typing
import pydantic


class ClientFacingWorkoutsChanged(UniversalBaseModel):
    event_type: ClientFacingWorkoutsChangedEventType
    user_id: str
    client_user_id: str
    team_id: str
    data: ClientFacingWorkout

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
