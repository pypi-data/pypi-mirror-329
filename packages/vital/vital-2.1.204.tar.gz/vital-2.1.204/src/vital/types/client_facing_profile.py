# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import pydantic
import typing
from .client_facing_source import ClientFacingSource
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class ClientFacingProfile(UniversalBaseModel):
    user_id: str = pydantic.Field()
    """
    User id returned by vital create user request. This id should be stored in your database against the user and used for all interactions with the vital api.
    """

    id: str
    height: typing.Optional[int] = None
    source: ClientFacingSource

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
