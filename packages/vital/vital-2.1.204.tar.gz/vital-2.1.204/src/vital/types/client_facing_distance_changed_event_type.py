# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class ClientFacingDistanceChangedEventType(str, enum.Enum):
    DAILY_DATA_DISTANCE_CREATED = "daily.data.distance.created"
    DAILY_DATA_DISTANCE_UPDATED = "daily.data.distance.updated"

    def visit(
        self,
        daily_data_distance_created: typing.Callable[[], T_Result],
        daily_data_distance_updated: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is ClientFacingDistanceChangedEventType.DAILY_DATA_DISTANCE_CREATED:
            return daily_data_distance_created()
        if self is ClientFacingDistanceChangedEventType.DAILY_DATA_DISTANCE_UPDATED:
            return daily_data_distance_updated()
