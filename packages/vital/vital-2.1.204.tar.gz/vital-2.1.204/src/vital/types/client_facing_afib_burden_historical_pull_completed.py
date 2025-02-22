# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .historical_pull_completed import HistoricalPullCompleted
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class ClientFacingAfibBurdenHistoricalPullCompleted(UniversalBaseModel):
    event_type: typing.Literal["historical.data.afib_burden.created"] = "historical.data.afib_burden.created"
    user_id: str
    client_user_id: str
    team_id: str
    data: HistoricalPullCompleted

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
