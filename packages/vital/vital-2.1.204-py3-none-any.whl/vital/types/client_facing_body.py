# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import pydantic
import datetime as dt
import typing
from .client_facing_source import ClientFacingSource
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class ClientFacingBody(UniversalBaseModel):
    user_id: str = pydantic.Field()
    """
    User id returned by vital create user request. This id should be stored in your database against the user and used for all interactions with the vital api.
    """

    id: str
    date: dt.datetime = pydantic.Field()
    """
    Date of the specified record, formatted as ISO8601 datetime string in UTC 00:00. Deprecated in favour of calendar_date.
    """

    calendar_date: str = pydantic.Field()
    """
    Date of the summary in the YYYY-mm-dd format.
    """

    weight: typing.Optional[float] = pydantic.Field(default=None)
    """
    Weight in kg::kg
    """

    fat: typing.Optional[float] = pydantic.Field(default=None)
    """
    Total body fat percentage::perc
    """

    water_percentage: typing.Optional[float] = pydantic.Field(default=None)
    """
    Water percentage in the body::perc
    """

    muscle_mass_percentage: typing.Optional[float] = pydantic.Field(default=None)
    """
    Muscle mass percentage in the body::perc
    """

    visceral_fat_index: typing.Optional[float] = pydantic.Field(default=None)
    """
    Visceral fat index::scalar
    """

    bone_mass_percentage: typing.Optional[float] = pydantic.Field(default=None)
    """
    Bone mass percentage in the body::perc
    """

    source: ClientFacingSource

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
