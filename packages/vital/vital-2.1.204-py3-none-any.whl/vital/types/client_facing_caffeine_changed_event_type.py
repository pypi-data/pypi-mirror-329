# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class ClientFacingCaffeineChangedEventType(str, enum.Enum):
    DAILY_DATA_CAFFEINE_CREATED = "daily.data.caffeine.created"
    DAILY_DATA_CAFFEINE_UPDATED = "daily.data.caffeine.updated"

    def visit(
        self,
        daily_data_caffeine_created: typing.Callable[[], T_Result],
        daily_data_caffeine_updated: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is ClientFacingCaffeineChangedEventType.DAILY_DATA_CAFFEINE_CREATED:
            return daily_data_caffeine_created()
        if self is ClientFacingCaffeineChangedEventType.DAILY_DATA_CAFFEINE_UPDATED:
            return daily_data_caffeine_updated()
