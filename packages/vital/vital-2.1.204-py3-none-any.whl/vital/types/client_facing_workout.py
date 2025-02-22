# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import pydantic
import typing
import datetime as dt
from .client_facing_sport import ClientFacingSport
from .client_facing_workout_map import ClientFacingWorkoutMap
from .client_facing_source import ClientFacingSource
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class ClientFacingWorkout(UniversalBaseModel):
    user_id: str = pydantic.Field()
    """
    User id returned by vital create user request. This id should be stored in your database against the user and used for all interactions with the vital api.
    """

    id: str
    title: typing.Optional[str] = pydantic.Field(default=None)
    """
    Title given for the workout
    """

    timezone_offset: typing.Optional[int] = pydantic.Field(default=None)
    """
    Timezone offset from UTC as seconds. For example, EEST (Eastern European Summer Time, +3h) is 10800. PST (Pacific Standard Time, -8h) is -28800::seconds
    """

    average_hr: typing.Optional[int] = pydantic.Field(default=None)
    """
    Average heart rate during workout::bpm
    """

    max_hr: typing.Optional[int] = pydantic.Field(default=None)
    """
    Max heart rate during workout::bpm
    """

    distance: typing.Optional[float] = pydantic.Field(default=None)
    """
    Distance travelled during workout::meters
    """

    calendar_date: str = pydantic.Field()
    """
    Date of the workout summary in the YYYY-mm-dd format. This generally matches the workout start date.
    """

    time_start: dt.datetime = pydantic.Field()
    """
    Start time of the workout::time
    """

    time_end: dt.datetime = pydantic.Field()
    """
    End time of the workout::time
    """

    calories: typing.Optional[float] = pydantic.Field(default=None)
    """
    Calories burned during the workout::kCal
    """

    sport: typing.Optional[ClientFacingSport] = pydantic.Field(default=None)
    """
    Sport's name
    """

    hr_zones: typing.Optional[typing.List[int]] = pydantic.Field(default=None)
    """
    Time in seconds spent in different heart rate zones <50%, 50-60%, 60-70%, 70-80%, 80-90%, 90%+. Due to rounding errors, it's possible that summing all values is different than the total time of the workout. Not available for all providers::seconds
    """

    moving_time: typing.Optional[int] = pydantic.Field(default=None)
    """
    Time spent active during the workout::seconds
    """

    total_elevation_gain: typing.Optional[float] = pydantic.Field(default=None)
    """
    Elevation gain during the workout::meters
    """

    elev_high: typing.Optional[float] = pydantic.Field(default=None)
    """
    Highest point of elevation::meters
    """

    elev_low: typing.Optional[float] = pydantic.Field(default=None)
    """
    Lowest point of elevation::meters
    """

    average_speed: typing.Optional[float] = pydantic.Field(default=None)
    """
    Average speed during workout in m/s::meters/sec
    """

    max_speed: typing.Optional[float] = pydantic.Field(default=None)
    """
    Max speed during workout in m/s::meters/sec
    """

    average_watts: typing.Optional[float] = pydantic.Field(default=None)
    """
    Average watts burned during exercise::watts
    """

    device_watts: typing.Optional[float] = pydantic.Field(default=None)
    """
    Watts burned during exercise::watts
    """

    max_watts: typing.Optional[float] = pydantic.Field(default=None)
    """
    Max watts burned during exercise::watts
    """

    weighted_average_watts: typing.Optional[float] = pydantic.Field(default=None)
    """
    Weighted average watts burned during exercise::watts
    """

    steps: typing.Optional[int] = pydantic.Field(default=None)
    """
    Number of steps accumulated during this workout::count
    """

    map_: typing.Optional[ClientFacingWorkoutMap] = pydantic.Field(alias="map", default=None)
    """
    Map of the workout
    """

    provider_id: str = pydantic.Field()
    """
    Provider ID given for that specific workout
    """

    source: ClientFacingSource = pydantic.Field()
    """
    Source the data has come from.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
