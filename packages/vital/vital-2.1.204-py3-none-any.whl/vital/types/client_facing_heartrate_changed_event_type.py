# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class ClientFacingHeartrateChangedEventType(str, enum.Enum):
    DAILY_DATA_HEARTRATE_CREATED = "daily.data.heartrate.created"
    DAILY_DATA_HEARTRATE_UPDATED = "daily.data.heartrate.updated"

    def visit(
        self,
        daily_data_heartrate_created: typing.Callable[[], T_Result],
        daily_data_heartrate_updated: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is ClientFacingHeartrateChangedEventType.DAILY_DATA_HEARTRATE_CREATED:
            return daily_data_heartrate_created()
        if self is ClientFacingHeartrateChangedEventType.DAILY_DATA_HEARTRATE_UPDATED:
            return daily_data_heartrate_updated()
