# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
import pydantic
from .client_facing_sample_grouping_keys import ClientFacingSampleGroupingKeys
import datetime as dt
from .client_facing_body_temperature_sample_sensor_location import ClientFacingBodyTemperatureSampleSensorLocation
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class ClientFacingBodyTemperatureSample(UniversalBaseModel):
    id: typing.Optional[int] = pydantic.Field(default=None)
    """
    Deprecated
    """

    timezone_offset: typing.Optional[int] = pydantic.Field(default=None)
    """
    Time zone UTC offset in seconds. Positive offset indicates east of UTC; negative offset indicates west of UTC; and null indicates the time zone information is unavailable at source.
    """

    type: typing.Optional[str] = pydantic.Field(default=None)
    """
    The reading type of the measurement. This is applicable only to Cholesterol, IGG, IGE and InsulinInjection.
    """

    unit: typing.Literal["°C"] = "°C"
    grouping: typing.Optional[ClientFacingSampleGroupingKeys] = None
    timestamp: dt.datetime = pydantic.Field()
    """
    Depracated. The start time (inclusive) of the interval.
    """

    start: dt.datetime = pydantic.Field()
    """
    The start time (inclusive) of the interval.
    """

    end: dt.datetime = pydantic.Field()
    """
    The end time (exclusive) of the interval.
    """

    value: float = pydantic.Field()
    """
    The recorded value for the interval.
    """

    sensor_location: typing.Optional[ClientFacingBodyTemperatureSampleSensorLocation] = pydantic.Field(default=None)
    """
    Location of the temperature sensor.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
